from flask import Flask, request, render_template, jsonify
import requests
from flask_cors import CORS
from motors import rotate, test

app = Flask(__name__)
cors = CORS(app)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)