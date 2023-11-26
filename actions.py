# -*- coding:utf-8 -*-
"""
@Time:    2023/11/26 21:30
@Author:  Evan Wong
@File:    actions.py
@Project: NAOGolf
@Description: Some basic actions to achieve the goal.
"""

import time
import math

import almath
import cv2

from motion_basis import MotionBasis
from golf_ball_detect import GolfBallDetect
from stick_detect import StickDetect
from landmark_detect import LandMarkDetect


class Actions(MotionBasis):
    """
    Some basic actions to achieve the goal.
    """

    def __init__(self, ip, port=9559):
        """
        Initialization.

        :arg:
            :param ip: the ip address of a NAO robot
            :type ip: str
            :param port: the port to connect NAO robot (9559, default)
            :type port: int
        :return: None
        """
        super(Actions, self).__init__(ip, port)
        self.max_speed_fraction = 0.05

        self.ball_detector = GolfBallDetect(ip, port)
        self.stick_detector = StickDetect(ip, port)
        self.landmark_detector = LandMarkDetect(ip, port)

    def move_head_searching(self, find_ball=True):
        """
        Move NAO robot's head to search for the golf ball.

        :arg:
            :param find_ball: True means ball found in the frame,
                              there are two set of arguments, one for found and one not.
            :type find_ball: bool
        :return: None
        """
        for i in range(1):
            names = ['HeadPitch', 'HeadYaw']
            targe_tangles = [-13.7 * almath.TO_RAD, 1.0 * almath.TO_RAD]
            self.motionProxy.angleInterpolationWithSpeed(names, targe_tangles, self.max_speed_fraction)
            self.ball_detector.update_ball_data(client='xxx')
            [x, y, angle] = self.ball_detector.ball_data
            if not x == 0 and not y == 0 and not angle == 0:
                break

            name = ["HeadYaw"]
            target_angle = 40.3 * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, target_angle, self.max_speed_fraction)
            # time.sleep(0.5)
            self.ball_detector.update_ball_data(client='xxx')
            [x, y, angle] = self.ball_detector.ball_data
            if not x == 0 and not y == 0 and not angle == 0:
                break

            target_angle = 1.0 * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, target_angle, self.max_speed_fraction)
            time.sleep(1.0)
            fraction = -45.2
            if find_ball:
                fraction = -51.2
            target_angle = fraction * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, target_angle, self.max_speed_fraction)
            self.ball_detector.update_ball_data(client='xxx')
            [x, y, angle] = self.ball_detector.ball_data
            if not x == 0 and not y == 0 and not angle == 0:
                break
        self.look_down()

    def search_golf_ball(self):
        """
        Method to let NAO robot to search the golf ball.

        :return: None
        """
        # Define some constants
        MAX_X = 0.4
        MAX_Y = 0.4
        MAX_ANGLE = 10 * math.pi / 180

        # Define a function to move the robot to the ball
        def move_to_ball(__x, __y, __angle):
            if __x > 1.0 or __y > 1.0 or __y < -1.0:
                self.motionProxy.moveTo(0, 0, __angle / 2, self.moveConfig)
                self.motionProxy.moveTo(__x / 2, 0, 0, self.moveConfig)
                time.sleep(2.0)
            else:
                self.motionProxy.moveTo(0, 0, __angle, self.moveConfig)
                self.motionProxy.moveTo(__x / 2, 0, 0, self.moveConfig)
                time.sleep(2.0)

        # Start searching the ball
        self.move_head_searching()
        [x, y, angle] = self.ball_detector.ball_data
        print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
        cv2.waitKey(0)
        self.look_down()

        while x > MAX_X or y > MAX_Y or y < -MAX_Y or \
                angle > MAX_ANGLE or angle < -MAX_ANGLE:
            move_to_ball(x, y, angle)
            self.move_head_searching()
            [x, y, angle] = self.ball_detector.ball_data
            print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
            cv2.waitKey(0)
            self.look_down()

        if x == 0 and y == 0 and angle == 0:
            self.move_head_searching(False)
            [x, y, angle] = self.ball_detector.ball_data
            print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
            cv2.waitKey(0)
            if x == 0 and y == 0 and angle == 0:
                self.look_down()
                self.motionProxy.moveTo(0, 0, angle, self.moveConfig)
                self.motionProxy.moveTo(x, 0, 0, self.moveConfig)
                time.sleep(2.0)
                self.motionProxy.moveTo(0.2, 0, 0, self.moveConfig)
            else:
                self.look_down()
                self.motionProxy.moveTo(0, 0, angle, self.moveConfig)
                self.motionProxy.moveTo(x - 0.3, 0, 0, self.moveConfig)
