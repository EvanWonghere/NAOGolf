# -*- coding:utf-8 -*-
"""
@Time:    2023/11/26 21:30
@Author:  Evan Wong
@File:    actions.py
@Project: NAOGolf
@Description: Some basic actions to achieve the goal.
"""

import time

import almath

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



