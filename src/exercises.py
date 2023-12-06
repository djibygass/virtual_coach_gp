import cv2
import numpy as np
import pose_class as pm

class Exercises:

    def gen_frames_squat(self):  
        detector = pm.poseDetector()
        cap = cv2.VideoCapture(0)

        count = 0
        direction = 0

        while True:
            success, img = cap.read()
            if not success:
                break

            img = detector.findPose(img, draw=False)
            lmlist = detector.findPosition(img, draw=False)

            if len(lmlist) != 0:
                # Partie superieure
                angle1 = detector.findAngle(img, 12, 24, 26)
                percentage1 = np.interp(angle1, (30, 180), (0, 100))
                # Partie inferieure
                angle2 = detector.findAngle(img, 24, 26, 28)
                percentage2 = np.interp(angle2, (180, 310), (0, 100))

                if (percentage1 <= 3 and percentage1 >= 0) and (percentage2 >= 96 and percentage2 <= 100):
                    if direction == 0: # going down
                        count += 0.5
                        direction = 1
                if (percentage1 >= 96 and percentage1 <= 100) and (percentage2 <= 3 and percentage2 >=0):
                    if direction == 1: # going up
                        count += 0.5
                        direction = 0

                cv2.putText(img, str(int(count)), (45, 350), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)

            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            

    def gen_frames_push_up(self):  
        detector = pm.poseDetector()
        cap = cv2.VideoCapture(0)

        count = 0
        direction = 0

        while True:
            success, img = cap.read()
            if not success:
                break

            img = detector.findPose(img, draw=False)
            lmlist = detector.findPosition(img, draw=False)

            if len(lmlist) != 0:
                # Partie superieure
                angle1 = detector.findAngle(img, 15, 13, 11)
                percentage1 = np.interp(angle1, (45, 180), (0, 100))

                if (percentage1 <= 20 and percentage1 >= 0):
                    if direction == 0: # going down
                        count += 0.5
                        direction = 1
                if (percentage1 >= 80 and percentage1 <= 100):
                    if direction == 1: # going up
                        count += 0.5
                        direction = 0

                cv2.putText(img, str(int(count)), (45, 350), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)

            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
