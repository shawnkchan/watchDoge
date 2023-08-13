from urllib import response
from flask import Flask, request, render_template, jsonify, render_template, stream_with_context, Response
from motors import rotate, test
import time
from time import sleep
import cv2
import numpy
from flask_socketio import SocketIO, emit
from cameraCode import Camera
from flask_cors import CORS


app = Flask(__name__)
vc = cv2.VideoCapture(0)
cors = CORS(app, resources={r"/socket.io/*": {"origins": "http://192.168.68.106:3001"}})
socketio = SocketIO(app)

def gen(camera):
    # """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        socketio.emit('video_stream', {'data': frame})


@socketio.on('connect')
def handle_connect():
    print('client connected')

@app.route("/")
def hello_world():
    test.test()
    return render_template('index.html')

@app.route("/motor")
def run_motor():
    rotate.turn_motor()
    return "motor turning"
    # return render_template('rotate.html')

# @app.route("/stopMotor")
# def stop_motor():
#     rotate.rotate_motor(0)
#     return "motor stopped"
#     # return jsonify({'data':'stop motor'})

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
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api2')
def api_test2():
    response_body = {
        'name': 'test2'
    }
    sleep(10)

    return jsonify(response_body)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
if __name__ == '__main__':
    socketio.start_background_task(video_feed)
    socketio.run(app)