# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 19:59
# @Author  : EvanWong
# @File    : GolfBallDetect.py
# @Project : NAOGolf
import cv2
import numpy as np

from visualBasis import VisualBasis

import vision_definitions as vd


def find_circles(preprocessed_img, min_dist, min_radius, max_radius):
    """
    Detect circles from image
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


def select_circle(circles):
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
    if circles.shape[0] == 0:
        return circles
    return circles[0]


class GolfBallDetect(VisualBasis):
    """
    A class to detect golf ball inherits from VisualBasis class
    """

    class GolfBall:
        """
        Simple class for golf ball
        """

        def __init__(self):
            """
            Initialization
            """
            self.ballData = {"centerX": 0, "centerY": 0, "radius": 0}
            self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            self.ballRadius = 0.025

    def __init__(self, ip, port=9559, camera_id=vd.kBottomCamera, resolution=vd.kVGA, is_write=True):
        super(GolfBallDetect, self).__init__(ip, port, camera_id, resolution)
        self.golfBall = self.GolfBall()
        self.isWrite = is_write

    def __get_preprocessed_image(self, low_min_hsv, low_max_hsv, high_min_hsv, high_max_hsv):
        """
        Get pre-processed binary image from the HSV image (transformed from BGR image)
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
        try:
            hsv_img = cv2.cvtColor(self.frame_array, cv2.COLOR_BGR2HSV)
        except KeyError:
            print "No image detected!"
        else:
            lower_ranged_frame = cv2.inRange(hsv_img, low_min_hsv, low_max_hsv)
            higher_ranged_frame = cv2.inRange(hsv_img, high_min_hsv, high_max_hsv)
            merged_frame = np.maximum(lower_ranged_frame, higher_ranged_frame)

            kernel_size = (9, 9)
            kernel = np.ones((9, 9), np.uint8)
            sigma_x = 1.5

            blured_frame = cv2.GaussianBlur(merged_frame, kernel_size, sigma_x)
            closed_frame = cv2.morphologyEx(blured_frame, cv2.MORPH_CLOSE, kernel)
            opened_frame = cv2.morphologyEx(closed_frame, cv2.MORPH_OPEN, kernel)

            return opened_frame

    def _update_ball_position(self, stand_state):
        """
        Compute and update the ball position with the ball data in frame.
        :arg:
            :param stand_state: Stand state of NAO robot, "standInit" or "standUp"
            :type stand_state: str
        :return: None
        """
        bottomCameraDirection = {"standInit": 49.2, "standUp": 39.7}
        # 摄像机初始俯仰角？
        ballRadius = self.golfBall.ballRadius
        try:
            cameraDirection = bottomCameraDirection[stand_state]
        except KeyError:
            print("Unknown stand state, please check the value of stand state!")
        else:
            if self.golfBall.ballData["radius"] == 0:
                # But... How could it be zero?
                self.golfBall.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                centerX = self.golfBall.ballData["centerX"]
                centerY = self.golfBall.ballData["centerY"]
                # radius = self.golfBall.ballData["radius"]

                cameraPosition = self.motionProxy.getPosition("CameraBottom", 2, True)
                # 2 means FRAME_ROBOT,
                # True means the sensor values will be used to determine the position.
                cameraX = cameraPosition[0]
                cameraY = cameraPosition[1]
                cameraHeight = cameraPosition[2]

                headPitches = self.motionProxy.getAngles("HeadPitch", True)
                headPitch = headPitches[0]  # 偏航角
                headYaws = self.motionProxy.getAngles("HeadYaw", True)
                headYaw = headYaws[0]  # 俯仰角
                # 像素坐标系 -> 图片坐标系 -> 相机坐标系（angle）
                ballPitch = (centerY - 240.0) * self.cameraPitchRange / 480.0  # y (pitch angle)
                ballYaw = (320.0 - centerX) * self.cameraYawRange / 640.0  # x (yaw angle)
                # 应是 (cameraHeight - ballRadius) / Pitch = np.tan(cameraDirection / 180 * np.pi + headPitch + ballPitch)
                # cameraDirection为初始绝对角度，headPitch为运动角度，ballPitch球相对摄像机角度，相加即球相对NAO角度
                # 故dPitch为球到NAO的距离，易得dYaw为球相对摄像机的位置，SA距离
                dPitch = (cameraHeight - ballRadius) / np.tan(cameraDirection / 180 * np.pi + headPitch + ballPitch)
                dYaw = dPitch / np.cos(ballYaw)
                # 投影到NAO坐标系
                ballX = dYaw * np.cos(ballYaw + headYaw) + cameraX
                ballY = dYaw * np.sin(ballYaw + headYaw) + cameraY
                ballYaw = np.arctan2(ballY, ballX)
                self.golfBall.ballPosition["disX"] = ballX
                if stand_state == "standInit":
                    ky = 42.513 * ballX ** 4 - 109.66 * ballX ** 3 + 104.2 * ballX ** 2 - 44.218 * ballX + 8.5526
                    # ky = 12.604*ballX**4 - 37.962*ballX**3 + 43.163*ballX**2 - 22.688*ballX + 6.0526
                    ballY = ky * ballY
                    ballYaw = np.arctan2(ballY, ballX)
                self.golfBall.ballPosition["disY"] = ballY
                self.golfBall.ballPosition["angle"] = ballYaw

    def update_ball_data(self, stand_state="standInit",
                         low_min_hsv=np.array([0, 43, 46]),
                         low_max_hsv=np.array([10, 255, 255]),
                         high_min_hsv=np.array([156, 43, 46]),
                         high_max_hsv=np.array([180, 255, 255])):
        """
        :arg:
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

        self.update_frame()
        gray_frame = self.__get_preprocessed_image(low_min_hsv, low_max_hsv, high_min_hsv, high_max_hsv)
        self._gray_frame = gray_frame.copy()
        circles = find_circles(gray_frame, min_dist, min_radius, max_radius)
        circle = select_circle(circles)

        if circle.shape[0] == 0:
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
        Get golf ball's position
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
        Show ball data in the current frame
        :return: None
        """
        if self.golfBall.ballData["radius"] == 0:
            print "ball position = (" + str(self.golfBall.ballPosition["disX"]) +\
                  ", " + str(self.golfBall.ballPosition["disY"]) + ")"
            cv2.imshow("ball position", self.frame_array)
        else:
            # print "ballX = " + str(self.ballData["centerX"])
            # print "ballY = " + str(self.ballData["centerY"])
            # print "ball position = (" + str(self.golfBall.ballPosition["disX"]) +\
            #                   ", " + str(self.golfBall.ballPosition["disY"]) + ")"
            # print "ball direction = " + str(self.ballPosition["angle"]*180/3.14)
            cv2.circle(self.frame_array, (self.golfBall.ballData["centerX"], self.golfBall.ballData["centerY"]),
                       self.golfBall.ballData["radius"], (250, 150, 150), 2)
            cv2.circle(self.frame_array, (self.golfBall.ballData["centerX"], self.golfBall.ballData["centerY"]),
                       2, (50, 250, 50), 3)
            cv2.imshow("Ball Position", self.frame_array)

    def slider_hsv(self, client):
        """
        :arg:
            :param client: client name
            :type client: str
        :return: None
        """
        def __nothing():
            pass

        windowName = "Slider for Ball Detection"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("minS1", windowName, 43, 60, __nothing)
        cv2.createTrackbar("minV1", windowName, 46, 65, __nothing)
        cv2.createTrackbar("maxH1", windowName, 10, 20, __nothing)
        cv2.createTrackbar("minH2", windowName, 156, 175, __nothing)
        while 1:
            self.update_frame(client)
            minS1 = cv2.getTrackbarPos("minS1", windowName)
            minV1 = cv2.getTrackbarPos("minV1", windowName)
            maxH1 = cv2.getTrackbarPos("maxH1", windowName)
            minH2 = cv2.getTrackbarPos("minH2", windowName)
            minHSV1 = np.array([0, minS1, minV1])
            maxHSV1 = np.array([maxH1, 255, 255])
            minHSV2 = np.array([minH2, minS1, minV1])
            maxHSV2 = np.array([180, 255, 255])
            self.update_ball_data(client,
                                  low_min_hsv=minHSV1,
                                  low_max_hsv=maxHSV1,
                                  high_min_hsv=minHSV2,
                                  high_max_hsv=maxHSV2)
            cv2.imshow(windowName, self._gray_frame)
            self.show_ball_position()
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()
