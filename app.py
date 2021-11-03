from flask import Flask, send_file
import json
import time

# Constants
UPDATE_FREQUENCY = 10 # Hz

LEFT_BUTTON_PIN = 17
CENTER_BUTTON_PIN = 27
RIGHT_BUTTON_PIN = 22
READY_START_PIN = 23

DIFF_SWITCH_PIN = 25
FUEL_SENSE_PIN = 24
TOTAL_FUEL_VOLUME = 5680  # mL

mode = 'live'
uart = None
gps = None

fuel_sensor = None
ready_button = None
diff_switch = None

ready_state = False
diff_state = False

gps_heading = 0
gps_speed = 0 # kts
gps_lock = False

# TODO: persist data over power cycles

current_fuel_volume = 0  # mL

best_time = 0 # milliseconds
prev_time = 0 # milliseconds
latest_lap_epoch = 0 # milliseconds

# Update functions
def update_gps():
    global gps_heading, gps_speed, gps_lock, gps
    gps.update()
    gps_lock = gps.has_fix
    gps_heading = round(gps.track_angle_deg) if gps.track_angle_deg is not None else 0
    gps_speed = round(gps.speed_knots) if gps.speed_knots is not None else 0
    gps.update()

def update_fuel_volume():
    global current_fuel_volume
    if current_fuel_volume >= 2.5:
        current_fuel_volume -= 2.5


def update_ready_state():
    global ready_state
    ready_state = not ready_state


try:
    # from gpiozero import Button
    import serial
    import adafruit_gps
    from threading import Timer

    # ready_button = Button(READY_START_PIN)
    # fuel_sensor = Button(FUEL_SENSE_PIN)

    # ready_button.when_pressed = update_ready_state
    # fuel_sensor.when_pressed = update_fuel_volume

    # Initialize GPS
    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

    gps.update()

    Timer(1/UPDATE_FREQUENCY, update_gps).start()

except ImportError:
    print("GPIO modules could not be imported, running in test mode.")
    mode = 'test'

    from math import sin

app = Flask(__name__)

@app.before_request
def check_mode():
    if mode == 'test':
        global gps_heading, gps_speed, gps_lock, ready_state, diff_state, current_fuel_volume
        ready_state = sin(time.time()) >= 0
        diff_state = sin(time.time()) >= 0

        gps_heading = round((sin(time.time()) + 1)/2 * 360) 
        gps_speed = round((sin(time.time()) + 1)/2 * 45) 
        gps_lock = True

        current_fuel_volume = round((sin(time.time()) + 1)/2 * TOTAL_FUEL_VOLUME)


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
        response=json.dumps({
            "status": "ok",
            "mode": mode
        }),
        mimetype="application/json",
    )


@app.route("/api/v1/systems/all")
def systems():
    return app.response_class(
        response=json.dumps({
            "gps": gps_data(),
            "fuel": fuel_data(),
            "time": timing_data(),
            "other": other_data()
        }),
        mimetype="application/json"
    )


@app.route("/api/v1/systems/gps")
def gps_data():
    return {
        "lock": gps_lock,
        "speed": gps_speed,
        "heading": gps_heading
    }


@app.route("/api/v1/systems/fuel")
def fuel_data():
    return {
        "level": round(current_fuel_volume/TOTAL_FUEL_VOLUME*100),
        "volume": current_fuel_volume
    }


@app.route("/api/v1/systems/time")
def timing_data():
    return {
        "timimg": {
            "elapsed": 0,
        }
    }


@app.route("/api/v1/systems/other")
def other_data():
    return {
        "diff_lock": diff_state,
        "start_mode": ready_state
    }
