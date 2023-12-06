from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import pose_class as pm
from exercises import Exercises

app = Flask(__name__, template_folder='templates')

exercises = Exercises()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/select_exercise', methods=['POST'])
def select_exercise():
    exercise = request.form['exercise']
    if exercise == 'squat':
        return render_template('squat.html')
    elif exercise == 'push_up':
        return render_template('push_up.html')
    
@app.route('/video_feed_squat')
def video_feed_squat():
    # Modify gen_frames or create a new function specific to squats
    return Response(exercises.gen_frames_squat(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_push_up')
def video_feed_push_up():
    # Modify gen_frames or create a new function specific to push-ups
    return Response(exercises.gen_frames_push_up(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
