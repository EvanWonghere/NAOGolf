import cv2
import naoqi
from golf_ball_detect import GolfBallDetect

if __name__ == '__main__':
    ip = "192.168.30.151"

    GolfBallDetector = GolfBallDetect(ip)
    client = 'test1'
    GolfBallDetector.slider_hsv(client)
