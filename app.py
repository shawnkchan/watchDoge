from urllib import response
from flask import Flask, request, render_template, jsonify, render_template, stream_with_context, Response
# import requests
# from flask_cors import CORS
from motors import rotate, test
import time
from time import sleep
import cv2
import numpy
# from cameraCode import VideoCamera
import picamera
import cv2
import socket
import io

# pi_camera = VideoCamera(flip=False)
app = Flask(__name__)
vc = cv2.VideoCapture(0)
# cors = CORS(app)

def gen():
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


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
    # """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api2')
def api_test2():
    response_body = {
        'name': 'test2'
    }

    sleep(10)

    return jsonify(response_body)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)