# -*- coding:utf-8 -*-
"""
@Time:    2023/11/23 14:31
@Author:  Evan Wong
@File:    landmark_detect.py
@Project: NAOGolf
@Description: To detect the landmark
"""

import time

import math
import almath
import numpy as np
import vision_definitions as vd

from visual_basis import VisualBasis


class LandMarkDetect(VisualBasis):
    """
    The class to detect NAO landmark, inherits from VisualBasis class
    """
    class Landmark:
        """
        Simple class for landmark
        """
        def __init__(self, landmark_size):
            """
            Initialization
            :arg:
                :param landmark_size: the size of NAO landmark
                :type landmark_size: float
            :return: None
            """
            self.landmark_size = landmark_size
            self.dis_x = 0
            self.dis_y = 0
            self.dist = 0
            self.yawAngle = 0

    def __init__(self, ip, port=9559, camera_id=vd.kTopCamera, landmark_size=0.105):
        """
        Initialization
        :arg:
            :param ip: the ip address of a NAO robot
            :type ip: str
            :param port: the port to connect NAO robot (9559, default)
            :type port: int
            :param camera_id bottom camera (1,default) or top camera (0).
            :type camera_id: int
            :param landmark_size: size of NAO landmark
            :type landmark_size: float
        :return: None
        """
        super(LandMarkDetection, self).__init__(ip, port, camera_id)
        self.landmark = self.Landmark(landmark_size)
        self.cameraID = camera_id
        self.cameraName = "CameraTop" if camera_id == vd.kTopCamera else "CameraBottom"
        self.cameraProxy.setActiveCamera(self.cameraID)

    def update_landmark_data(self, client="landMark"):
        """
        Update NAO landmark information
        :arg:
            :param client: client name
            :type client: str
        :return: None
        """
        if self.cameraProxy.getActiveCamera() != self.cameraID:
            self.cameraProxy.setActiveCamera(self.cameraID)
            time.sleep(1)

        self.landmarkProxy.subscribe(client)
        landmark_data = self.memoryProxy.getData("LandmarkDetected")
        self.cameraProxy.unsubscribe(client)

        if landmark_data is None or len(landmark_data) == 0:
            self.landmark.dis_x = 0
            self.landmark.dis_y = 0
            self.landmark.dist = 0
            self.landmark.yawAngle = 0
        else:
            # landmark_data:
            #   [TimeStampField, MarkInfo[N], CameraPoseInFrameTorso, CameraPoseInFrameRobot, CurrentCameraName]
            #       - MarkInfo = [ShapeInfo, MarkID]
            #           - ShapeInfo = [1, alpha, beta, sizeX, sizeY, heading]
            #               - `alpha` and `beta` represent the location of the NaoMark’s center
            #                 in terms of camera angles in radian.
            #               - `sizeX` and `sizeY` are the mark’s size in camera angles.
            #               - the `heading` angle describes how the Nao mark is oriented about the vertical axis
            #                 in regard to the robot’s head.
            wzCamera = landmark_data[1][0][0][1]  # alpha
            wyCamera = landmark_data[1][0][0][2]  # beta
            angularSize = landmark_data[1][0][0][3]  # sizeX
            distCameraToLandmark = self.landmark.landmark_size / (2 * math.tan(angularSize / 2))
            # 变形而来，原式为：
            # tan(angularSize / 2) = (self.landmark.landmark_size / 2) / distCameraToLandmark
            transform = self.motionProxy.getTransform(self.cameraName, 2, True)  # 2 means FRAME_ROBOT
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)
            cameraToLandmarkRotTrans = almath.Transform_from3DRotation(0, wyCamera, wzCamera)
            cameraToLandmarkTranslationTrans = almath.Transform(distCameraToLandmark, 0, 0)
            robotToLandmark = robotToCamera * cameraToLandmarkRotTrans * cameraToLandmarkTranslationTrans
            self.landmark.dis_x = robotToLandmark.r1_c4
            self.landmark.dis_y = robotToLandmark.r2_c4
            self.landmark.dist = np.sqrt(self.landmark.dis_x ** 2 + self.landmark.dis_y ** 2)
            self.landmark.yawAngle = math.atan2(self.landmark.dis_x, self.landmark.dis_y)

        """
        这段代码的主要目的是更新NAO机器人的地标信息。它首先检查当前活动的相机是否是预设的相机，如果不是，就将预设的相机设置为活动相机。
        然后，它订阅地标代理，从内存代理中获取地标检测数据，最后取消订阅地标代理。

        如果没有检测到地标（`landmark_data` 为空或长度为0），那么地标的各项参数（`dis_x`, `dis_y`, `dist`, `yawAngle`）都会被设置为0。

        如果检测到了地标，那么会进行一系列的计算来确定地标相对于机器人的位置。
        首先，从 `landmark_data` 中提取出地标的角度信息（`alpha`, `beta`, `sizeX`）。
        然后，使用这些信息计算出相机到地标的距离 `distCameraToLandmark`。

        接下来，使用 `motionProxy.getTransform` 方法获取机器人到相机的变换矩阵 `robotToCamera`。
        这个变换矩阵描述了相机相对于机器人的位置和方向。

        然后，创建两个变换矩阵 `cameraToLandmarkRotTrans` 和 `cameraToLandmarkTranslationTrans`，
        分别表示相机到地标的旋转变换和平移变换。
        `cameraToLandmarkRotTrans` 是根据地标在相机视野中的角度（`wyCamera`, `wzCamera`）创建的，
        `cameraToLandmarkTranslationTrans` 是根据相机到地标的距离（`distCameraToLandmark`）创建的。

        最后，将这三个变换矩阵相乘，得到机器人到地标的总变换矩阵 `robotToLandmark`。这个矩阵描述了地标相对于机器人的位置和方向。
        从这个矩阵中，可以提取出地标在机器人坐标系中的x和y坐标（`dis_x`, `dis_y`），以及地标到机器人的距离（`dist`）和偏航角（`yawAngle`）。
        """

    def get_landmark_data(self):
        """
        Get landmark information
        :return: None
        """
        return [self.landmark.dis_x, self.landmark.dis_y, self.landmark.dist, self.landmark.yawAngle]

    def show_landmark_data(self):
        """
        Show landmark information that detected.
        :return: None
        """
        print("disX = ", self.landmark.dis_x)
        print("disY = ", self.landmark.dis_y)
        print("dis = ", self.landmark.dist)
        print("yaw angle = ", self.landmark.yawAngle * 180.0 / np.pi)
