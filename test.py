# -*- coding:utf-8 -*-
"""
@Time:    2023/11/23 16:52
@Author:  Evan Wong
@File:    test.py
@Project: NAOGolf
@Description: Some test codes for Nao golf visual part.
"""

import os
import time

import cv2
import vision_definitions as vd

from nao_configure import NAOConfigure
from visual_basis import VisualBasis
from golf_ball_detect import GolfBallDetect
from stick_detect import StickDetect
from landmark_detect import LandMarkDetect


if __name__ == '__main__':
    ip = ""
    port = 9559
    cameraID = vd.kTopCamera
    resolution = vd.kVGA

    NAO = NAOConfigure(ip)
    visualBasis = VisualBasis(ip, camera_id=cameraID, resolution=resolution)
    golfBallDetect = GolfBallDetect(ip)
    stickDetect = StickDetect(ip, camera_id=cameraID)
    landmarkDetect = LandMarkDetect(ip)

    # test code
    """
    visualBasis.update_frame()
    visualBasis.show_frame()
    visualBasis.print_frame_data()
    cv2.waitKey(1000)
    """

    # posture initialization
    """
    motionProxy = NAO.motionProxy
    postureProxy = NAO.postureProxy
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.moveToward(0.1, 0.1, 0, [["Frequency", 1.0]])
    motionProxy.moveTo(0.3, 0.2, 0)
    """

    # visualBasis.motionProxy.wakeUp()
    # visualBasis.postureProxy.goToPosture("StandInit", 0.5)
    """
    while True:
        time1 = time.time()
        golfBallDetect.update_ball_data(client="xxxx")
        print golfBallDetect.ball_data
        time2 = time.time()
        print "update data time = ", time2 - time1
        golfBallDetect.show_ball_position()
        cv2.waitKey(1000)
    """

    """
    while True:
        stickDetect.update_stick_data(client="xxx")
        stickDetect.show_stick_position()
        cv2.waitKey(1000)
    """

    """
    while True:
        landmarkDetect.update_landmark_data(client="xxx")
        landmarkDetect.show_landmark_data()
        time.sleep(1)
    """

    """
    print "start collecting..."
    for i in range(10):
        imgName = "stick_" + str(i+127) + ".jpg"
        imgDir = os.path.join("stick_images", imgName)
        visualBasis.update_frame()
        visualBasis.show_frame()
        visualBasis.save_frame(imgDir)
        print "saved in ", imgDir
        time.sleep(5)
    """

    """
    visualBasis.ttsProxy.say("hello world")
    """

    """
    visualBasis.motionProxy.wakeUp()
    """

    """
    dataList = visualBasis.memoryProxy.getDataList("camera")
    print dataList
    """

    """
    visualBasis.motionProxy.setStiffnesses("Body", 1.0)
    visualBasis.motionProxy.moveInit()
    """
