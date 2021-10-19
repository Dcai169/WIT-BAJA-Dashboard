from flask import Flask, send_file
from random import randint
import json

app = Flask(__name__)


def generate_mock_data(lower, upper):
    return randint(lower, upper)


@app.route("/")
def root():
    return send_file("index.html")


@app.route("/styles.css")
def styles():
    return send_file("styles.css")


@app.route("/scripts.js")
def scripts():
    return send_file("scripts.js")


@app.route("/api/v1/status")
def status():
    return app.response_class(
        response=json.dumps({"status": "ok"}),
        mimetype="application/json",
    )


@app.route("/api/v1/systems/all")
def systems():
    return app.response_class(
        response=json.dumps({
            "gps": {
                "lock": True,
                "latitude": 42.3601,
                "longitude": -71.0589,
                "altitude": 100,
                "speed": generate_mock_data(0, 70),
                "heading": generate_mock_data(0, 360)
            },
            "fuel": {
                "level": generate_mock_data(0, 100),
                "estimate": generate_mock_data(0, 60)
            },
            "time": {
                "elapsed": generate_mock_data(0, 60000),
            },
            "other": {
                "diff-lock": False,
                "start-mode": False
            }
        }),
        mimetype="application/json"
    )


@app.route("/api/v1/systems/gps")
def gps():
    return {
        "lock": True,
        "latitude": 42.3601,
        "longitude": -71.0589,
        "altitude": 100,
        "speed": generate_mock_data(0, 70),
        "heading": generate_mock_data(0, 360)
    }


@app.route("/api/v1/systems/fuel")
def fuel():
    return {
        "level": generate_mock_data(0, 100),
        "estimate": generate_mock_data(0, 60)
    }


@app.route("/api/v1/systems/time")
def time():
    return {
        time: {
            "elapsed": generate_mock_data(0, 60000),
        }
    }


@app.route("/api/v1/systems/other")
def other():
    return {
        "diff_lock": False,
        "start_mode": False
    }
