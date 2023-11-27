import vision_definitions as vd

from golf_ball_detect import GolfBallDetect
from stick_detect import StickDetect
from landmark_detect import LandMarkDetect
from motion_basis import MotionBasis
from actions import Actions

if __name__ == '__main__':
    ip = "192.168.30.223"

    # MotionController = MotionBasis(ip)
    # MotionController.autonomousLifeProxy.setState('disabled')
    # MotionController.postureProxy.goToPosture("StandInit", 1.0)
    # MotionController.grab_club()
    # MotionController.hit_ball(0.8)

    Actor = Actions(ip)
    
    Actor.autonomousLifeProxy.setState('disabled')
    Actor.postureProxy.goToPosture("StandInit", 1.0)
    #Actor.look_down()

    Actor.search_golf_ball()
    # GolfBallDetector = GolfBallDetect(ip)
    # GolfBallDetector.autonomousLifeProxy.setState('disabled')
    # client = 'test112312643'
    # GolfBallDetector.slider_hsv(client)

    # stickDetector = StickDetect(ip, camera_id=vd.kBottomCamera)
    # stickDetector.autonomousLifeProxy.setState('disabled')
    # client = 'test13221'
    # stickDetector.slider(client)

    #landmarkDetector = LandMarkDetect(ip, camera_id=vd.kBottomCamera)
    #landmarkDetector.autonomousLifeProxy.setState('disabled')
    #client = 'test12138'
    #while True:
    #    landmarkDetector.update_frame(client)
    #    landmarkDetector.show_frame()
    #    landmarkDetector.update_landmark_data()
    #    landmarkDetector.show_landmark_data()
