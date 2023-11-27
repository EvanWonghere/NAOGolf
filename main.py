import vision_definitions as vd

from golf_ball_detect import GolfBallDetect
from stick_detect import StickDetect
from landmark_detect import LandMarkDetect
from actions import Actions

if __name__ == '__main__':
    ip = "192.168.30.223"
    GolfBallDetector = GolfBallDetect(ip)
    # GolfBallDetector.autonomousLifeProxy.setState('disabled')
    GolfBallDetector.postureProxy.goToPosture("StandInit", 0.2)
    client = 'test1123126qw'
    GolfBallDetector.slider_hsv(client)

    # stickDetector = StickDetect(ip, camera_id=vd.kBottomCamera)
    # stickDetector.autonomousLifeProxy.setState('disabled')
    # client = 'test13221'
    # stickDetector.slider(client)

    # landmarkDetector = LandMarkDetect(ip, camera_id=vd.kBottomCamera)
    # landmarkDetector.autonomousLifeProxy.setState('disabled')
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
