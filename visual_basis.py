# -*- coding: utf-8 -*-
"""
@Time    : 2023/11/22 17:08
@Author  : Evan Wong
@File    : visual_basis.py
@Project : NAOGolf
@Description: Basic class for visual identity, stored some attributes about frame and camera
"""

import cv2
import time
import numpy as np
import vision_definitions as vd

from nao_configure import NAOConfigure


class VisualBasis(NAOConfigure):
    """
    A basic class for visual identity inherits from NAOConfigure class.
    """

    def __init__(self, ip, port=9559, camera_id=vd.kBottomCamera, resolution=vd.kVGA):
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
        :returns: None
        """
        super(VisualBasis, self).__init__(ip, port)
        self.cameraID = camera_id
        self.resolution = resolution
        self.colorSpace = vd.kHSVColorSpace
        self.fps = 30
        self.frameHeight = 0
        self.frameWidth = 0
        self.frameChannels = 0
        self._frameArray = np.array([])
        self._gray_frame = np.array([])
        self.cameraPitchRange = 47.64 / 180 * np.pi  # 俯仰角范围
        self.cameraYawRange = 60.97 / 180 * np.pi  # 偏航角范围
        self.cameraProxy.setActiveCamera(self.cameraID)

    def update_frame(self, client="python-client"):
        """
        Get a new image from the specific camera and save it in self._frame.

        :arg:
            :param client: client name
            :type client: str
        :return: None
        :raise: IndexError
        """
        if self.cameraProxy.getActiveCamera() != self.cameraID:
            self.cameraProxy.setActiveCamera(self.cameraID)
            time.sleep(1)

        video_client = self.cameraProxy.subscribeCamera(client, self.cameraID,
                                                        self.resolution, self.colorSpace, self.fps)
        frame = self.cameraProxy.getImageRemote(video_client)
        self.cameraProxy.unsubscribe(video_client)
        try:
            self.frameWidth = frame[0]
            self.frameHeight = frame[1]
            self.frameChannels = frame[2]
            self._frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame[1], frame[0], frame[2]])
        except IndexError:
            print "get image failed!"

    @property
    def frame_array(self):
        """
        Get current frame array.

        :return:
            current frame array (empty array if None)
            :rtype: np.ndarray
        """
        return self._frameArray.copy()

    @property
    def gray_frame(self):
        """
        Get preprocessed binary image.

        :return:
            Preprocessed image
            :rtype: np.ndarray
        """
        return self._gray_frame.copy()

    def show_frame(self):
        """
        Show current frame data.

        :return: None
        """
        if self._frameArray.size == 0:
            print "Please get an image from NAO with method update_frame() first"
        else:
            cv2.imshow("Current Frame", cv2.cvtColor(self.frame_array, cv2.COLOR_HSV2BGR_FULL))

    def show_gray_frame(self):
        """
        Show current gray frame data.

        :return: None
        """
        if self._gray_frame.size == 0:
            print "Please get an image from NAO with method update_frame() first"
        else:
            cv2.imshow("Current Frame", self.gray_frame)

    def print_frame_data(self):
        """
        Print current frame data.

        :return: None
        """
        print "Frame Height:   " + str(self.frameHeight)
        print "Frame Width:    " + str(self.frameWidth)
        print "Frame Channels: " + str(self.frameChannels)
        print "Frame Shape:    " + str(self._frameArray.size)

    def save_frame(self, frame_path):
        """
        Save the current frame to the give path.

        :arg:
            :param frame_path: The path to store the current frame
            :type frame_path: str
        :return: None
        """
        cv2.imwrite(frame_path, self._frameArray)
        print "Current frame image saved in " + frame_path
