from golf_ball_detect import GolfBallDetect

if __name__ == '__main__':
    ip = "192.168.30.223"
    GolfBallDetector = GolfBallDetect(ip)
    GolfBallDetector.autonomousLifeProxy.setState('disabled')
    client = 'test112312643'
    GolfBallDetector.slider_hsv(client)
