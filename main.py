import cv2
import vision_definitions as vd

from golf_ball_detect import GolfBallDetect
from stick_detect import StickDetect
from landmark_detect import LandMarkDetect
from actions import Actions

if __name__ == '__main__':
    ip = "192.168.30.151"
    # GolfBallDetector = GolfBallDetect(ip)
    # # GolfBallDetector.autonomousLifeProxy.setState('disabled')
    # GolfBallDetector.postureProxy.goToPosture("StandInit", 0.2)
    # client = 'test1123126qw'
    # GolfBallDetector.slider_hsv(client)

    stickDetector = StickDetect(ip)
    # stickDetector.autonomousLifeProxy.setState('disabled')
    # stickDetector.postureProxy.goToPosture("StandInit", 0.2)
    client = 'test13221'
    # stickDetector.slider(client)
    while True:
        stickDetector.update_stick_data(client)
        cv2.imshow("window_name", cv2.cvtColor(stickDetector.frame_array, cv2.COLOR_HSV2BGR_FULL))
        stickDetector.show_stick_position()
        stickDetector.show_gray_frame()
        cv2.waitKey(10)

    # landmarkDetector = LandMarkDetect(ip, camera_id=vd.kBottomCamera)
    # # landmarkDetector.autonomousLifeProxy.setState('disabled')
    # client = 'test12138'
    # while True:
    #     landmarkDetector.update_frame(client)
    #     landmarkDetector.show_frame()
    #     landmarkDetector.update_landmark_data()
    #     landmarkDetector.show_landmark_data()

    # client = 'tests'
    # actions = Actions(ip)
    # actions.autonomousLifeProxy.setState('disabled')
    # actions.postureProxy.goToPosture("StandInit", 0.2)
    # actions.search_golf_ball(client)
