
from flask import Flask,render_template,Response,request
import cv2
import mediapipe as mp
from curls import curls_fn
from squats import squats_fn
from pull_ups import pullups_fn
from push_ups import pushups_fn



app=Flask(__name__)
camera=cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def curls():
    counter=0
    stage="down"
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ## read the camera frame
            success,frame=camera.read()
            if not success:
                print("Error in reading camera frame.")
                break
            else:

                frame,counter,stage=curls_fn(counter,frame,pose,stage)
                # print(counter)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def squats():

    counter = 0
    rep_started = False
    rep_completed = False
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ## read the camera frame
            success,frame=camera.read()
            if not success:
                print("Error in reading camera frame.")
                break
            else:

                frame,counter,rep_started,rep_completed=squats_fn(counter,rep_started,rep_completed,frame,pose)
                # print(counter)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def pullups():
    counter = 0
    is_counting = False
    rep_completed = False
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ## read the camera frame
            success,frame=camera.read()
            if not success:
                print("Error in reading camera frame.")
                break
            else:

                frame, counter,is_counting,rep_completed=pullups_fn(counter,is_counting,rep_completed,frame,pose)
                # print(counter)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def pushups():
    counter = 0
    is_counting = False
    rep_completed = False
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while camera.isOpened():
            ## read the camera frame
            success,frame=camera.read()
            if not success:
                print("Error in reading camera frame.")
                break
            else:

                frame, counter,is_counting,rep_completed=pushups_fn(counter,is_counting,rep_completed,frame,pose)
                # print(counter)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/curl')
def curl():
    return Response(curls(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pushup')
def pushup():
    return Response(pushups(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pullup')
def pullup():
    return Response(pushups(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squat')
def squat():
    return Response(pushups(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-function', methods=['POST'])
def run_function():
    selected_function = request.form['function-select']
    
    if selected_function == 'pushup':
        render_template('pushup.html', counter=selected_function)
    elif selected_function == 'pullup':
        render_template('pullup.html', counter=selected_function)
    elif selected_function == 'squat':
        render_template('squat.html', counter=selected_function)

    return render_template('curl.html', counter=selected_function)


if __name__=="__main__":
    app.run(debug=True)
    print("Running")