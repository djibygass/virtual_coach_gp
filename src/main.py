import cv2
import numpy as np
import time
import PoseModule as pm

detector = pm.poseDetector()
# cap = cv2.VideoCapture('data/squat_video.mp4')
cap = cv2.VideoCapture(0)

count = 0
direction = 0

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (600, 720))
    # img = cv2.imread('data/squat.jpg')

    img = detector.findPose(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        # Partie superieure
        angle1 = detector.findAngle(img, 12, 24, 26)
        percentage1 = np.interp(angle1, (30, 180), (0, 100))
        # Partie inferieure
        angle2 = detector.findAngle(img, 24, 26, 28)
        percentage2 = np.interp(angle2, (180, 310), (0, 100))

        # print(angle2, percentage2)

        if (percentage1 <= 3 and percentage1 >= 0) and (percentage2 >= 96 and percentage2 <= 100):
        # if percentage1 == 0 and percentage2 == 100:
            if direction == 0: # going down
                count += 0.5
                direction = 1
        if (percentage1 >= 96 and percentage1 <= 100) and (percentage2 <= 3 and percentage2 >=0):
        # if percentage1 == 100 and percentage2 == 0:
            if direction == 1: # going up
                count += 0.5
                direction = 0
        # print(percentage1, percentage2)
        print(count)

        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (255, 255, 0), 5)
            

    cv2.imshow('imgage', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break