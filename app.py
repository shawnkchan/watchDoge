from flask import Flask, request, render_template, jsonify, render_template, stream_with_context, Response
import requests
from flask_cors import CORS
from motors import rotate, test
import cv2
import numpy
from cameraCode import VideoCamera
import threading

pi_camera = VideoCamera(flip=False)
app = Flask(__name__)
cors = CORS(app)

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/")
def hello_world():
    test.test()
    return render_template('index.html')

@app.route("/motor")
def run_motor():
    rotate.rotate_motor()
    # return render_template('rotate.html')

@app.route("/api")
def api_test():
    response_body = {
        'name': 'test',
        'context': 'this is a test api call'
    }
    return jsonify(response_body)

@app.route('/video_feed')
def video_feed():
    #returns a HTTP response to the client when this API is called
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video')
def stop_video():
    pi_camera.__del__()
    response_body = {'success'}
    return jsonify(response_body)

def start_camera_stream():
    camera_thread = threading.Thread(target=gen, args=(pi_camera))
    camera_thread.daemon = True
    camera_thread.start()


if __name__ == '__main__':
    start_camera_stream()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)