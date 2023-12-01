from flask import Flask, render_template, Response
import cv2
import numpy as np
import pose_class as pm

app = Flask(__name__, template_folder='template')

def gen_frames():  
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

            # Draw count on the image
            cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 5)

        ret, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
