# -*- coding:utf-8 -*-
"""
@Time:    2023/11/26 16:41
@Author:  Evan Wong
@File:    motion_basis.py
@Project: NAOGolf
@Description: Basic class for motion control
"""

import time
import math

import almath

from nao_configure import NAOConfigure


class MotionBasis(NAOConfigure):
    """
    Basic class for motion control.
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
        super(MotionBasis, self).__init__(ip, port)

        self.joint_names = ['RShoulderPitch', 'RShoulderRoll', 'RElbowRoll', 'RWristYaw', 'RElbowYaw']
        self.stick_angle = -math.pi / 2
        self.max_speed_fraction = 0.2
        self.max_step_x = 0.04
        self.max_step_y = 0.14
        self.max_step_theta = 0.4
        self.max_step_frequency = 0.6
        self.step_height = 0.02
        self.torso_wx = 0.0
        self.torso_wy = 0.0
        self.moveConfig = [["MaxStepX", self.max_step_x],
                           ["MaxStepY", self.max_step_y],
                           ["MaxStepTheta", self.max_step_theta],
                           ["MaxStepFrequency", self.max_step_frequency],
                           ["StepHeight", self.step_height],
                           ["TorsoWx", self.torso_wx],
                           ["TorsoWy", self.torso_wy]]

    def grab_club(self):
        """
        Let the NAO robot to grab the golf club the time after event "HandRightRightTouched" raised.

        :return: None
        """
        while True:
            FrontTactilTouched = self.memoryProxy.getData("FrontTactilTouched")
            # Raised when the right hand right tactile sensor is touched (by human).
            # return value – 1.0 if right hand right tactile sensor is touched.
            if FrontTactilTouched == 1.0:
                print "touched"
                self.ttsProxy.say("give me a club ")
                targetAngles = [67.7 * almath.TO_RAD, 3.2 * almath.TO_RAD,
                                73.8 * almath.TO_RAD, 6.2 * almath.TO_RAD,
                                93.7 * almath.TO_RAD]
                maxSpeedFraction = 0.2
                self.motionProxy.angleInterpolationWithSpeed(self.joint_names, targetAngles, maxSpeedFraction)

                time.sleep(2.0)

                name = 'RHand'
                targetAngle = 0.68
                self.motionProxy.angleInterpolationWithSpeed(name, targetAngle, maxSpeedFraction)

                time.sleep(5.0)

                targetAngle = 0.14
                self.motionProxy.angleInterpolationWithSpeed(name, targetAngle, maxSpeedFraction)

                time.sleep(2.0)

                break

    def head_touch(self):
        """
        To detect whether the front tactile sensor is touched.

        :return: None
        """
        while True:
            headTouchedButtonFlag = self.memoryProxy.getData("FrontTactilTouched")
            # Raised when the front head tactile sensor is touched (by human).
            # return value – 1.0 if front head tactile sensor is touched.
            if headTouchedButtonFlag == 1.0:
                print "front head tactile touched"
                self.ttsProxy.say("begin the round three")
                break

    def hit_ball(self, ball_hit_speed):
        """
        The method to let NAO robot hit the ball with specific speed and two ways.

        :arg:
            :param ball_hit_speed: The speed to hit the ball
            :type ball_hit_speed: float
        :return: None
        """
        targetList = [[94.0 * almath.TO_RAD, 41.3 * almath.TO_RAD],
                      [-13.0 * almath.TO_RAD, -36.5 * almath.TO_RAD, 2.8 * almath.TO_RAD],
                      [19.3 * almath.TO_RAD, 72.8 * almath.TO_RAD],
                      [8.4 * almath.TO_RAD, -3.5 * almath.TO_RAD, 6.3 * almath.TO_RAD],
                      [88.5 * almath.TO_RAD, 73.7 * almath.TO_RAD, 94.1 * almath.TO_RAD]]

        timeList = [[1.0, 3.0],
                    [1.0, 2.0, 4.0],
                    [1.0, 3.0],
                    [1.0, 2.0, 4.0],
                    [1.0, 2.0, 3.0]]

        isAbsolute = True

        self.motionProxy.angleInterpolation(self.joint_names, targetList, timeList, isAbsolute)

        time.sleep(1.0)

        if self.stick_angle < 0:
            targetAngle = [67.7 * almath.TO_RAD, 3.2 * almath.TO_RAD, 73.8 * almath.TO_RAD, 48.8 * almath.TO_RAD,
                           93.7 * almath.TO_RAD]
            self.motionProxy.angleInterpolationWithSpeed(self.joint_names, targetAngle, self.max_speed_fraction)

            time.sleep(3.0)

            name = 'RWristYaw'
            targetAngle = -39.1 * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, targetAngle, ball_hit_speed)
        else:
            targetAngle = [67.7 * almath.TO_RAD, 3.2 * almath.TO_RAD,
                           73.8 * almath.TO_RAD, -37.7 * almath.TO_RAD,
                           93.7 * almath.TO_RAD]
            self.motionProxy.angleInterpolationWithSpeed(self.joint_names, targetAngle, self.max_speed_fraction)

            time.sleep(3.0)

            name = 'RWristYaw'
            targetAngle = 34.7 * almath.TO_RAD
            self.motionProxy.angleInterpolationWithSpeed(name, targetAngle, ball_hit_speed)

    def adjust_position(self, turn_data):
        """
        The method to adjust NAO robot's position using the give data.

        :arg:
            :param turn_data: The data to let the NAO adjust its position,
                            turn_data = [dist1, dist2, turnAngle1, turnAngle2]
            :type turn_data: list
        :return: None
        """
        [dist1, dist2, turnAngle1, turnAngle2] = turn_data

        self.motionProxy.setMoveArmsEnabled(False, False)
        self.motionProxy.moveTo(0.0, 0.0, turnAngle1, self.moveConfig)
        self.motionProxy.setMoveArmsEnabled(False, False)
        self.motionProxy.moveTo(dist2, 0.0, 0.0, self.moveConfig)
        self.motionProxy.setMoveArmsEnabled(False, False)
        self.motionProxy.moveTo(0.0, 0.0, turnAngle2, self.moveConfig)
        self.motionProxy.setMoveArmsEnabled(False, False)
        self.motionProxy.moveTo(0.0, dist1, 0.0, self.moveConfig)

    def let_go(self):
        """
        To have the NAO robot let go the time after event "RearTactilTouched" raised.

        :return: None
        """
        while True:
            headFlag = self.memoryProxy.getData("RearTactilTouched")
            if headFlag == 1.0:
                self.ttsProxy.say("i will stop !")
                self.motionProxy.openHand('RHand')
                break

    def look_down(self):
        """
        Let the NAO robot look down a bit.

        :return: None
        """
        joint_names = ['HeadPitch', 'HeadYaw']
        target_angle = [-0.4 * almath.TO_RAD, 0.0 * almath.TO_RAD]
        fraction_max_speed = 0.2
        self.motionProxy.angleInterpolationWithSpeed(joint_names, target_angle, fraction_max_speed)
        time.sleep(1.0)
