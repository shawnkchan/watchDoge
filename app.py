from flask import Flask, request, render_template
import requests
from flask_cors import CORS
from motors import rotate

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def hello_world():
    return render_template()

@app.route("/motor")
def run_motor():
    rotate.rotate_motor('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)