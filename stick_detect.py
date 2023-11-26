# -*- coding: utf-8 -*-
"""
@Time    : 2023/11/23 10:13
@Author  : Evan Wong
@File    : stick_detect.py
@Project : NAOGolf
@Description: To detect the yellow stick at golf hole
"""

import cv2
import numpy as np
import vision_definitions as vd

from visual_basis import VisualBasis


class StickDetect(VisualBasis):
    """
    A class to detect the stick at golf hole, inherits from VisualBasis class.
    """
    class Stick:
        """
        Simple class for stick.
        """
        def __init__(self):
            self.boundRect = []
            self.cropKeep = 1
            self.stickAngle = 0.0  # rad

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
        """
        super(StickDetect, self).__init__(ip, port, camera_id, resolution)
        self.stick = self.Stick()
        self.is_write = is_write

    def __get_preprocessed_image(self, min_hsv, max_hsv, crop_keep):
        """
        Get pre-processed binary image from the HSV image (transformed from BGR image).

        :arg:
            :param min_hsv: Lower threshold for yellow stick
            :type min_hsv: np.ndarray
            :param max_hsv: Higher threshold for yellow stick
            :type max_hsv: np.ndarray
            :param crop_keep: crop ratio of image (>= 0.5)
            :type crop_keep: float
        :return:
            pre-processed binary image
            :rtype: np.ndarray
        """
        self.stick.cropKeep = crop_keep
        frame_array = self.frame_array
        height = self.frameHeight

        try:
            cropped_frame = frame_array[int((1 - crop_keep) * height):, :]
        except IndexError:
            print "Error occurred when cropping the image"
        else:
            hsv_img = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
            bin_img = cv2.inRange(hsv_img, min_hsv, max_hsv)

            kernel_size = (9, 9)
            kernel = np.ones((5, 5), np.uint8)
            sigma_x = 0

            closed_frame = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
            opened_frame = cv2.morphologyEx(closed_frame, cv2.MORPH_OPEN, kernel)
            blured_frame = cv2.GaussianBlur(opened_frame, kernel_size, sigma_x)
            # cv2.imshow("stick bin", frameBin)
            # cv2.waitKey(20)
            return blured_frame

    def __find_stick(self, preprocessed_img, min_perimeter, min_area, min_aspect_ratio):
        """
        Find the stick at golf hole using some strategy.

        :arg:
            :param preprocessed_img: Pre-processed image to be detected
            :type preprocessed_img: np.ndarray
            :param min_perimeter: minimum perimeter of detected stick
            :type min_perimeter: float
            :param min_area: minimum area of detected stick
            :type min_area: float
            :param min_aspect_ratio: minimum aspect ratio of detected stick
            :type min_aspect_ratio: float
        :return:
            Detected stick marked with rectangle or [].
            :rtype: np.ndarray
        """
        rects = []
        contours, _ = cv2.findContours(preprocessed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0:
            return rects

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)

            if perimeter > min_perimeter and area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                rects.append([x, y, w, h])
        if len(rects) == 0:
            return rects

        rects = [rect for rect in rects if (1.0 * rect[3] / rect[2]) > min_aspect_ratio]
        if len(rects) == 0:
            return rects

        rects = np.array(rects)
        rect = rects[np.argmax(1.0 * (rects[:, -1]) / rects[:, -2]), ]
        rect[1] += int(self.frameHeight * (1 - self.stick.cropKeep))

        return rect

    def update_stick_data(self, client="test", crop_keep=0.75,
                          min_hsv=np.array([27, 55, 115]),
                          max_hsv=np.array([45, 255, 255]),
                          min_aspect_ratio=0.8):
        """
        Detect and update the data of stick.

        :arg:
            :param client: client name
            :type client: str
            :param crop_keep: crop ratio of image (>= 0.5)
            :type crop_keep: float
            :param min_hsv: Lower threshold for yellow stick
            :type min_hsv: np.ndarray
            :param max_hsv: Higher threshold for yellow stick
            :type max_hsv: np.ndarray
            :param min_aspect_ratio: minimum aspect ratio of detected stick
            :type min_aspect_ratio: float
        :return: None
        """
        self.update_frame(client)
        min_perimeter = self.frameHeight / 8.0
        min_area = self.frameHeight * self.frameWidth / 1000.0
        self._gray_frame = self.__get_preprocessed_image(min_hsv, max_hsv, crop_keep)
        gray_frame = self.gray_frame

        rect = self.__find_stick(gray_frame, min_perimeter, min_area, min_aspect_ratio)
        if not rect:
            self.stick.boundRect = []
            self.stick.stickAngle = 0.0
        else:
            self.stick.boundRect = rect
            center_x = rect[0] + rect[2] / 2
            self.stick.stickAngle = (1.0 * self.frameWidth / 2 - center_x) / self.frameWidth * self.cameraYawRange
            camera_position = self.motionProxy.getPosition("Head", 2, True)  # 为何与之前的不同？
            camera_y = camera_position[5]
            self.stick.stickAngle += camera_y

    def show_stick_position(self):
        """
        Show the stick position in the current frame.

        :return: None
        """
        if not self.stick.boundRect:
            # print "No stick detected!"
            cv2.imshow("Stick Position", self.frame_array)
        else:
            [x, y, w, h] = self.stick.boundRect
            frame = self.frame_array
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow("Stick Position", frame)

    def slider(self, client):
        """
        Slider for stick detection in HSV color space.

        :arg:
            :param client: client name
            ":type client: str
        :return: None
        """
        def __nothing():
            pass

        window_name = "Slider for Stick Detection"
        cv2.namedWindow(window_name)
        cv2.createTrackbar("minH", window_name, 27, 45, __nothing)
        cv2.createTrackbar("minS", window_name, 55, 75, __nothing)
        cv2.createTrackbar("minV", window_name, 115, 150, __nothing)
        cv2.createTrackbar("maxH", window_name, 45, 70, __nothing)

        while True:
            self.update_frame(client)
            min_h = cv2.getTrackbarPos("minH", window_name)
            min_s = cv2.getTrackbarPos("minS", window_name)
            min_v = cv2.getTrackbarPos("minV", window_name)
            max_h = cv2.getTrackbarPos("maxH", window_name)
            min_hsv = np.array([min_h, min_s, min_v])
            max_hsv = np.array([max_h, 255, 255])
            min_aspect_ratio = 0.8
            crop_keep = 0.75
            self.update_stick_data(client, crop_keep, min_hsv, max_hsv, min_aspect_ratio)
            cv2.imshow(window_name, self.gray_frame)
            self.show_stick_position()
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
