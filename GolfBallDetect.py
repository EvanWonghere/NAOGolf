# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 19:59
# @Author  : EvanWong
# @File    : GolfBallDetect.py
# @Project : NAOGolf
import cv2
import numpy as np

from visualBasis import VisualBasis

import vision_definitions as vd


def __find_circles(preprocessedImg, minDist, minRadius, maxRadius):
    """
    Detect circles from image
    :arg:
        :param preprocessedImg: Pre-processed image to be detected
        :type preprocessedImg: np.ndarray
        :param minDist: minium distance between the center of two circle
        :type minDist: float
        :param minRadius: minium radius of circles
        :type minRadius: float
        :param maxRadius: maximum radius of circles
        :type maxRadius: float
    :return:
        an uint16 numpy array shaped circleNum * 3 if circleNum > 0, ([[circleX, circleY,radius]])
        else return None.
        :rtype: np.ndarray
    """
    method = cv2.HOUGH_GRADIENT
    dp = 1
    param1 = 150
    param2 = 15
    circles = cv2.HoughCircles(np.uint8(preprocessedImg), method, dp,
                               minDist, param1, param2, minRadius, maxRadius)

    if circles is None:
        return np.uint16([])
    return np.uint16(np.round(circles[0, ]))


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

    def __init__(self, IP, port=9559, cameraID=vd.kBottomCamera, resolution=vd.kVGA, isWrite=True):
        super(GolfBallDetect, self).__init__(IP, port, cameraID, resolution)
        self.golfBall = self.GolfBall()
        self.isWrite = isWrite

    def __get_preprocessed_image(self, low_minHSV, low_maxHSV, high_minHSV, high_maxHSV):
        """
        Get pre-processed binary image from the HSV image (transformed from BGR image)
        :arg:
            :param low_minHSV: Lower threshold for lower range red tones
            :type low_maxHSV: np.ndarray
            :param low_maxHSV: Higher threshold for lower range red tones
            :type low_maxHSV: np.ndarray
            :param high_minHSV: Lower threshold for higher range red tones
            :type high_minHSV: np.ndarray
            :param high_maxHSV: Higher threshold for higher range red tones
            :type high_maxHSV: np.ndarray
        :return:
            pre-processed binary image
            :rtype: np.ndarray
        """
        try:
            hsv_img = cv2.cvtColor(self.frame_array, cv2.COLOR_BGR2HSV)
        except:
            print "No image detected!"
        else:
            lower_ranged_frame = cv2.inRange(hsv_img, low_minHSV, low_maxHSV)
            higher_ranged_frame = cv2.inRange(hsv_img, high_minHSV, high_maxHSV)
            merged_frame = np.maximum(lower_ranged_frame, higher_ranged_frame)
            kernel_size = (9, 9)
            sigma_x = 1.5
            blured_frame = cv2.GaussianBlur(merged_frame, kernel_size, sigma_x)

            return blured_frame

    def __select_circle(self, circles):
        """
        Select one circle in list type from all circles detected.
        :arg:
            :param circles: numpy array shaped (N, 3),　N is the number of circles.
            :type circles: np.ndarray
        :return:
            selected circles
            :rtype: np.ndarray
        """

