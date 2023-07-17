from flask import Flask, request, render_template, jsonify, render_template, stream_with_context
import requests
from flask_cors import CORS
from motors import rotate, test
import cv2
import numpy


app = Flask(__name__)
cors = CORS(app)
video = cv2.VideoCapture(0)

def video_stream():
    while True:
        ret,frame=video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route("/")
def hello_world():
    test.test()
    return render_template('index.html')

@app.route("/motor")
def run_motor():
    rotate.rotate_motor()
    # return render_template('index.html')

@app.route("/api")
def api_test():
    response_body = {
        'name': 'test',
        'context': 'this is a test api call'
    }
    return jsonify(response_body)

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame$=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)