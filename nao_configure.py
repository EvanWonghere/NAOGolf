# -*- coding: utf-8 -*-
"""
@Time    : 2023/11/22 16:41
@Author  : Evan Wong
@File    : nao_configure.py
@Project : NAOGolf
@Description: Basic class for NAO, to store the proxies
"""

from naoqi import ALProxy


class NAOConfigure(object):
    def __init__(self, ip, port=9559):
        """
        Basic NAO robot class with some proxies
        :arg:
            :param ip: the ip address of a NAO robot
            :type ip: str
            :param port: the port to connect NAO robot (9559, default)
            :type port: int
        :returns: None
        :raise: ConnectionError
        """
        self.ip = ip
        self.port = port

        try:
            self.ttsProxy = ALProxy("ALTextToSpeech", self.ip, self.port)
            self.memoryProxy = ALProxy("ALMemory", self.ip, self.port)
            self.cameraProxy = ALProxy("AVideoDevice", self.ip, self.port)
            self.motionProxy = ALProxy("ALMotion", self.ip, self.port)
            self.postureProxy = ALProxy("ALRobotPosture", self.ip, self.port)
            self.landmarkProxy = ALProxy("ALLandMarkDetection", self.ip, self.port)
        except Exception, e:
            print("Error when configuring the NAO!")
            print(str(e))
            exit(1)
