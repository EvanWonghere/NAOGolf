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

import angle_interpolation as ai

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

    def move_head_searching(self, find_ball=True, client='xxx'):
        """
        Move NAO robot's head to search for the golf ball.

        :arg:
            :param find_ball: True means ball found in the frame,
                              there are two set of arguments, one for found and one not
            :type find_ball: bool
            :param client: client name
            :type client: str
        :return: None
        """
        for i in range(1):
            names = ['HeadPitch', 'HeadYaw']
            targe_tangles = [40 * almath.TO_RAD, 1.0 * almath.TO_RAD]
            self.motionProxy.angleInterpolationWithSpeed(names, targe_tangles, self.max_speed_fraction)
            time.sleep(1)
            self.ball_detector.update_ball_data(client=client)
            self.ball_detector.show_ball_position()
            cv2.waitKey(1000)
            [x, y, angle] = self.ball_detector.ball_position
            if not x == 0 and not y == 0 and not angle == 0:
                break

            names = ['HeadPitch', 'HeadYaw']
            targe_tangles = [-10 * almath.TO_RAD, 1.0 * almath.TO_RAD]
            self.motionProxy.angleInterpolationWithSpeed(names, targe_tangles, self.max_speed_fraction)
            time.sleep(2)
            self.ball_detector.update_ball_data(client=client)
            self.ball_detector.show_ball_position()
            cv2.waitKey(1000)
            [x, y, angle] = self.ball_detector.ball_position
            if not x == 0 and not y == 0 and not angle == 0:
                break

            name = ["HeadYaw"]
            target_angle = 40.3 * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, target_angle, self.max_speed_fraction)
            time.sleep(1)
            self.ball_detector.update_ball_data(client=client)
            self.ball_detector.show_ball_position()
            cv2.waitKey(1000)
            [x, y, angle] = self.ball_detector.ball_position
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
            time.sleep(1.0)

            self.ball_detector.update_ball_data(client=client)
            self.ball_detector.show_ball_position()
            cv2.waitKey(1000)
            [x, y, angle] = self.ball_detector.ball_data
            if not x == 0 and not y == 0 and not angle == 0:
                break
        self.look_down()

    def search_golf_ball(self, client):
        """
        Method to let NAO robot to search the golf ball.

        :arg:
            :param client: client name
            :type client: str
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
        self.move_head_searching(client=client)

        [x, y, angle] = self.ball_detector.ball_position
        print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
        self.look_down()

        while x > MAX_X or y > MAX_Y or y < -MAX_Y or \
                angle > MAX_ANGLE or angle < -MAX_ANGLE:
            move_to_ball(x, y, angle)
            self.move_head_searching(client=client)
            [x, y, angle] = self.ball_detector.ball_position

            print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
            self.look_down()

        if x == 0 and y == 0 and angle == 0:
            self.move_head_searching(False)
            [x, y, angle] = self.ball_detector.ball_data
            print "Ball position: x = {}, y = {}, angle = {}".format(x, y, angle)
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

    def init_for_golf(self):
        """
        Let the NAO robot initialized for golf competition.

        :return: None
        """
        names, times, keys = ai.setup_movement()
        self.motionProxy.angleInterpolationBezier(names, times, keys)
        time.sleep(0.5)

    def move_golf(self, x, y, theta):
        """
        This method is used for robot walking while playing golf
        In order to prevent the moveTo method from knocking the club off the robot
        we made the robot walk with zero stiffness of the right hand joint

        :arg:
            :param x: The x-axis coordinate to go
            :type x: float
            :param y: The y-axis coordinate to go
            :type y: float
            :param theta: The angle to turn
            :type theta: float
        :return: None
        """
        self.init_for_golf()
        namesLists = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        self.motionProxy.setStiffnesses(namesLists, 0)
        self.motionProxy.moveTo(x, y, theta)
        time.sleep(0.3)
        self.motionProxy.setStiffnesses(namesLists, 1)
        time.sleep(0.3)

    def ready_for_golf(self):
        names, times, keys = ai.hand_ready()
        self.motionProxy.angleInterpolationBezier(names, times, keys)
        time.sleep(0.5)

    def hit_ball_with_forces(self, ball_hit_force):
        """
        :arg:
            :param ball_hit_force: The force to hit the ball
                    0 - softly
                    1 - medium
                    2 - hardly
                    3 - strongly
            :type ball_hit_force: int
        :return: None
        """
        self.init_for_golf()
        time.sleep(0.5)
        self.ready_for_golf()
        time.sleep(0.5)

        try:
            if ball_hit_force == 0:
                names, times, keys = ai.soft_hit()
                self.motionProxy.angleInterpolationBezier(names, times, keys)
            elif ball_hit_force == 1:
                names, times, keys = ai.medium_hit()
                self.motionProxy.angleInterpolationBezier(names, times, keys)
            elif ball_hit_force == 2:
                names, times, keys = ai.hard_hit()
                self.motionProxy.angleInterpolationBezier(names, times, keys)
            elif ball_hit_force == 3:
                names, times, keys = ai.strong_hit()
                self.motionProxy.angleInterpolationBezier(names, times, keys)
        except ValueError:
            raise ValueError("ball_hit_force must be 0 or 1 or 2 or 3")
        finally:
            time.sleep(0.5)
            names, times, keys = ai.hang_down()
            self.motionProxy.angleInterpolationBezier(names, times, keys)
            time.sleep(0.5)
