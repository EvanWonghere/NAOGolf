# -*- coding: utf-8 -*-
"""
@Time    : 2023/11/22 19:59
@Author  : Evan Wong
@File    : golf_ball_detect.py
@Project : NAOGolf
@Description: To detect the red golf ball
"""

import cv2
import numpy as np
import vision_definitions as vd

from visual_basis import VisualBasis


def find_circles(preprocessed_img, min_dist, min_radius, max_radius):
    """
    Detect circles from image.

    :arg:
        :param preprocessed_img: Pre-processed image to be detected
        :type preprocessed_img: np.ndarray
        :param min_dist: minium distance between the center of two circle
        :type min_dist: float
        :param min_radius: minium radius of circles
        :type min_radius: float
        :param max_radius: maximum radius of circles
        :type max_radius: float
    :return:
        an uint16 numpy array shaped circleNum * 3 if circleNum > 0, ([[circleX, circleY,radius]])
        else return None.
        :rtype: np.ndarray
    """
    method = cv2.HOUGH_GRADIENT
    dp = 1
    param1 = 150
    param2 = 15
    circles = cv2.HoughCircles(np.uint8(preprocessed_img), method, dp,
                               min_dist, param1, param2, min_radius, max_radius)

    if circles is None:
        return np.uint16([])
    return np.uint16(np.round(circles[0, ]))


class GolfBallDetect(VisualBasis):
    """
    A class to detect golf ball inherits from VisualBasis class.
    """

    class GolfBall:
        """
        Simple class for golf ball.
        """

        def __init__(self):
            """
            Initialization.
            """
            self.ballData = {"centerX": 0, "centerY": 0, "radius": 0}
            self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            self.ballRadius = 0.025

    def __init__(self, ip, port=9559, camera_id=vd.kBottomCamera, resolution=vd.kVGA, is_write=True):
        """
        Initialization.

        :arg:
            :param ip: the ip address of a NAO robot
            :type ip: str
            :param port: the port to connect NAO robot (9559, default)
            :type port: int
            :param camera_id bottom camera (1,default) or top camera (0).
            :type camera_id: int
            :param resolution: kVGA, default: 640*480
            :type resolution: int
            :param is_write: whether write current frame to specific directory, we actually not used it
            :type is_write: bool
        :return: None
        """
        super(GolfBallDetect, self).__init__(ip, port, camera_id, resolution)
        self.golfBall = self.GolfBall()
        self.isWrite = is_write

    def __get_preprocessed_image(self, low_min_hsv, low_max_hsv, high_min_hsv, high_max_hsv):
        """
        Get pre-processed binary image from the HSV image (transformed from BGR image).

        :arg:
            :param low_min_hsv: Lower threshold for lower range red tones
            :type low_max_hsv: np.ndarray
            :param low_max_hsv: Higher threshold for lower range red tones
            :type low_max_hsv: np.ndarray
            :param high_min_hsv: Lower threshold for higher range red tones
            :type high_min_hsv: np.ndarray
            :param high_max_hsv: Higher threshold for higher range red tones
            :type high_max_hsv: np.ndarray
        :return:
            pre-processed binary image
            :rtype: np.ndarray
        """
        hsv_img = self.frame_array
        lower_ranged_frame = cv2.inRange(hsv_img, low_min_hsv, low_max_hsv)
        higher_ranged_frame = cv2.inRange(hsv_img, high_min_hsv, high_max_hsv)
        merged_frame = np.maximum(lower_ranged_frame, higher_ranged_frame)

        kernel_size = (9, 9)
        kernel = np.ones((5, 5), np.uint8)
        sigma_x = 1.5

        closed_frame = cv2.morphologyEx(merged_frame, cv2.MORPH_CLOSE, kernel)
        opened_frame = cv2.morphologyEx(closed_frame, cv2.MORPH_OPEN, kernel)
        blured_frame = cv2.GaussianBlur(opened_frame, kernel_size, sigma_x)

        return blured_frame

    def _update_ball_position(self, stand_state):
        """
        Compute and update the ball position with the ball data in frame.

        :arg:
            :param stand_state: Stand state of NAO robot, "standInit" or "standUp"
            :type stand_state: str
        :return: None
        """
        bottom_camera_direction = {"standInit": 49.2, "standUp": 39.7}
        # 摄像机初始俯仰角？
        ball_radius = self.golfBall.ballRadius
        try:
            camera_direction = bottom_camera_direction[stand_state]
        except KeyError:
            print("Unknown stand state, please check the value of stand state!")
        else:
            if self.golfBall.ballData["radius"] == 0:
                # But... How could it be zero?
                self.golfBall.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                center_x = self.golfBall.ballData["centerX"]
                center_y = self.golfBall.ballData["centerY"]
                # radius = self.golfBall.ballData["radius"]

                camera_position = self.motionProxy.getPosition("CameraBottom", 2, True)
                # 2 means FRAME_ROBOT,
                # True means the sensor values will be used to determine the position.
                camera_x = camera_position[0]
                camera_y = camera_position[1]
                camera_height = camera_position[2]

                head_pitches = self.motionProxy.getAngles("HeadPitch", True)
                head_pitch = head_pitches[0]  # 偏航角
                head_yaws = self.motionProxy.getAngles("HeadYaw", True)
                head_yaw = head_yaws[0]  # 俯仰角
                # 像素坐标系 -> 图片坐标系 -> 相机坐标系（angle）
                ball_pitch = (center_y - 1.0 * self.frameHeight / 2) * self.cameraPitchRange / self.frameHeight
                # y (pitch angle)
                ball_yaw = (1.0 * self.frameWidth / 2 - center_x) * self.cameraYawRange / self.frameWidth
                # x (yaw angle)
                # 应是 (cameraHeight - ballRadius) / Pitch = np.tan(cameraDirection / 180 * np.pi + headPitch + ballPitch)
                # cameraDirection为初始绝对角度，headPitch为运动角度，ballPitch球相对摄像机角度，相加即球相对NAO角度
                # 故dPitch为球到NAO的距离，易得dYaw为球相对摄像机的位置，SA距离
                d_pitch = ((camera_height - ball_radius) /
                           np.tan(camera_direction / 180 * np.pi + head_pitch + ball_pitch))
                d_yaw = d_pitch / np.cos(ball_yaw)
                # 投影到NAO坐标系
                ball_x = d_yaw * np.cos(ball_yaw + head_yaw) + camera_x
                ball_y = d_yaw * np.sin(ball_yaw + head_yaw) + camera_y
                ball_yaw = np.arctan2(ball_y, ball_x)
                self.golfBall.ballPosition["disX"] = ball_x
                if stand_state == "standInit":
                    ky = 42.513 * ball_x ** 4 - 109.66 * ball_x ** 3 + 104.2 * ball_x ** 2 - 44.218 * ball_x + 8.5526
                    # ky = 12.604*ballX**4 - 37.962*ballX**3 + 43.163*ballX**2 - 22.688*ballX + 6.0526
                    ball_y = ky * ball_y
                    ball_yaw = np.arctan2(ball_y, ball_x)
                self.golfBall.ballPosition["disY"] = ball_y
                self.golfBall.ballPosition["angle"] = ball_yaw

    def select_circle(self, circles):
        """
        Select one circle in list type from all circles detected.

        :arg:
            :param circles: numpy array shaped (N, 3),　N is the number of circles.
            :type circles: np.ndarray
        :return:
            selected circles
            :rtype: np.ndarray
        """
        # We do not find it useful so just pass
        if not circles.shape or circles.shape[0] == 0:
            return circles

        if circles.shape[0] == 1:
            centerX = circles[0][0]
            centerY = circles[0][1]
            radius = circles[0][2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if (initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or
                    (initY + 4 * radius) > self.frameHeight or radius < 1):
                return circles

        BGR_frame = cv2.cvtColor(self.frame_array, cv2.COLOR_HSV2BGR_FULL)
        rRatioMin = 1.0
        circleSelected = np.uint16([])
        for circle in circles:
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or (initY + 4 * radius) > self.frameHeight or radius < 1:
                continue
            rectBallArea = BGR_frame[initY:initY + 4 * radius + 1, initX:initX + 4 * radius + 1, :]
            bFlat = np.float16(rectBallArea[:, :, 0].flatten())
            gFlat = np.float16(rectBallArea[:, :, 1].flatten())
            rFlat = np.float16(rectBallArea[:, :, 2].flatten())
            rScore1 = np.uint8(rFlat > 1.0 * gFlat)
            rScore2 = np.uint8(rFlat > 1.0 * bFlat)
            rScore = float(np.sum(rScore1 * rScore2))
            gScore = float(np.sum(np.uint8(gFlat > 1.0 * rFlat)))
            rRatio = rScore / len(rFlat)
            gRatio = gScore / len(gFlat)
            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19) < abs(rRatioMin - 0.19):
                circleSelected = circle
                rRatioMin = rRatio
        return circleSelected

    def update_ball_data(self, client="python-client", stand_state="standInit",
                         low_min_hsv=np.array([0, 43, 46]),
                         low_max_hsv=np.array([10, 255, 255]),
                         high_min_hsv=np.array([156, 43, 46]),
                         high_max_hsv=np.array([180, 255, 255])):
        """
        Detect and update the data of golf ball.

        :arg:
            :param client: client name
            :type client: str
            :param stand_state: Stand state of NAO robot, "standInit" or "standUp"
            :type stand_state: str
            :param low_min_hsv: Lower threshold for lower range red tones
            :type low_max_hsv: np.ndarray
            :param low_max_hsv: Higher threshold for lower range red tones
            :type low_max_hsv: np.ndarray
            :param high_min_hsv: Lower threshold for higher range red tones
            :type high_min_hsv: np.ndarray
            :param high_max_hsv: Higher threshold for higher range red tones
            :type high_max_hsv: np.ndarray
        :return: None
        """
        # low_min_hsv = np.array([0, 43, 46])
        # low_max_hsv = np.array([10, 255, 255])
        # high_min_hsv = np.array([156, 43, 46])
        # high_max_hsv = np.array([180, 255, 255])
        min_dist = int(self.frameHeight / 30.0)
        min_radius = 1
        max_radius = int(self.frameHeight / 10.0)

        self.update_frame(client)
        self._gray_frame = self.__get_preprocessed_image(low_min_hsv, low_max_hsv, high_min_hsv, high_max_hsv)
        circles = find_circles(self.gray_frame, min_dist, min_radius, max_radius)
        circle = self.select_circle(circles)

        if not circle.shape or circle.shape[0] == 0:
            # print "No ball detected"
            self.golfBall.ballData = {"centerX": 0, "centerY": 0, "radius": 0}
            self.golfBall.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        else:
            circle = circle.reshape([-1, 3])
            self.golfBall.ballData = {"centerX": circle[0][0], "centerY": circle[0][1], "radius": circle[0][2]}
            self._update_ball_position(stand_state)

    @property
    def ball_position(self):
        """
        Get golf ball's position.

        :return:
            distance in x-axis, distance in y-axis and direction related to Nao.
            :rtype: list
        """
        return self.golfBall.ballPosition.values()

    @property
    def ball_data(self):
        """
        Get ball information in image.

        :return:
            CenterX, centerY and radius of the red ball.
            :rtype: list
        """
        return self.golfBall.ballData.values()

    def show_ball_position(self):
        """
        Show ball data in the current frame.

        :return: None
        """
        print "ball position = (" + str(self.golfBall.ballPosition["disX"]) + \
                  ", " + str(self.golfBall.ballPosition["disY"]) + ")"
        if self.golfBall.ballData["radius"] == 0:
            cv2.imshow("Ball Position", cv2.cvtColor(self.frame_array, cv2.COLOR_HSV2BGR_FULL))
        else:
            # print "ballX = " + str(self.ballData["centerX"])
            # print "ballY = " + str(self.ballData["centerY"])
            # print "ball position = (" + str(self.golfBall.ballPosition["disX"]) +\
            #                   ", " + str(self.golfBall.ballPosition["disY"]) + ")"
            # print "ball direction = " + str(self.ballPosition["angle"]*180/3.14)
            frame = self.frame_array
            cv2.circle(frame, (self.golfBall.ballData["centerX"], self.golfBall.ballData["centerY"]),
                       self.golfBall.ballData["radius"], (250, 150, 150), 2)
            cv2.circle(frame, (self.golfBall.ballData["centerX"], self.golfBall.ballData["centerY"]),
                       2, (50, 250, 50), 3)
            cv2.imshow("Ball Position", cv2.cvtColor(frame, cv2.COLOR_HSV2BGR_FULL))

    def slider_hsv(self, client):
        """
        Create sliders to change the threshold of HSV.

        :arg:
            :param client: client name
            :type client: str
        :return: None
        """

        def __nothing():
            pass

        window_name = "Slider for Ball Detection"
        cv2.namedWindow(window_name)
        cv2.createTrackbar("minS1", window_name, 43, 60, __nothing)
        cv2.createTrackbar("minV1", window_name, 46, 65, __nothing)
        cv2.createTrackbar("maxH1", window_name, 10, 20, __nothing)
        cv2.createTrackbar("minH2", window_name, 156, 175, __nothing)
        while True:
            self.update_frame(client)
            min_s1 = cv2.getTrackbarPos("minS1", window_name)
            min_v1 = cv2.getTrackbarPos("minV1", window_name)
            max_h1 = cv2.getTrackbarPos("maxH1", window_name)
            min_h2 = cv2.getTrackbarPos("minH2", window_name)
            min_hsv1 = np.array([0, min_s1, min_v1])
            max_hsv1 = np.array([max_h1, 255, 255])
            min_hsv2 = np.array([min_h2, min_s1, min_v1])
            max_hsv2 = np.array([180, 255, 255])
            self.update_ball_data(client,
                                  low_min_hsv=min_hsv1,
                                  low_max_hsv=max_hsv1,
                                  high_min_hsv=min_hsv2,
                                  high_max_hsv=max_hsv2)
            cv2.imshow(window_name, cv2.cvtColor(self.frame_array, cv2.COLOR_HSV2BGR))
            self.show_ball_position()
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

    def is_golf_ball_insight(self):
        """
        Return whether the golf ball is in NAO robot's sight.

        :return:
            True means in sight else not.
            :rtype: bool
        """
        [dis_x, dis_y, angle] = self.ball_position
        return dis_x or dis_y or angle
