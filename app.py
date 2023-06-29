from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>HELLO WORLD</p>"
