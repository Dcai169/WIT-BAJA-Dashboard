from csv import DictWriter
from os import close, wait
from flask import Flask, send_file
from subprocess import call
import json
import time
import gps_util
import numpy as np

# Constants
UPDATE_FREQUENCY = 10 # Hz

LEFT_BUTTON_PIN = 4 # All buttons are active low
CENTER_BUTTON_PIN = 17
RIGHT_BUTTON_PIN = 27
READY_START_PIN = 22

NEOPIXEL_PIN = 18
POWER_BUTTON_PIN = 26
GPS_FIX_PIN = 25

DIFF_SWITCH_PIN = 23
FUEL_SENSE_PIN = 24 # Fuel sensor is active high

SPI_MOSI = 10
SPI_MISO = 9
SPI_SCLK = 11
SPI_CE0 = 8

TOTAL_FUEL_VOLUME = 5680  # mL
GRACE_PERIOD = 600# Ms
gps = 'NULL'
wait_period = 0
mode = 'live'

fuel_sensor = None
ready_button = None
diff_switch = None

start_set = False
ready_state = False
diff_state = False

# TODO: persist data over power cycles

current_fuel_volume = 0  # mL

best_time = 0 # milliseconds
prev_time = 0 # milliseconds
latest_lap_epoch = 0 # milliseconds
total_time = 0  # milliseconds
lapnum = 0


log_file = None
log_writer = None

# Update functions

def update_fuel_volume():
    global current_fuel_volume
    if current_fuel_volume >= 2.5:
        current_fuel_volume -= 2.5

def update_ready_state():
    global ready_state
    ready_state = not ready_state

def write_log():
    global log_writer, current_fuel_volume
    log_writer.writerow({'timestamp': time.time(), 'gps_lock': gps.get_lock, 'gps_location': gps.get_location, 'heading': gps.get_heading, 'speed': gps.gps_speed, 'fuel_volume': current_fuel_volume})

def shutdown(): # TODO: implement
    global log_file
    log_file.close()
    call('sudo shutdown -h now', shell=True)
def timer_init():
    global gps
    if(gps.get_lock):
        gps.set_start
        ready_state = True
def timer():
    global gps, wait_period
    if(gps.get_speed < 1):    
        wait_period += 1
        if (wait_period > GRACE_PERIOD):
            if(np.isclose(gps.get_location(), gps.get_start(), rtol = 0.00002)):
                pass
                #lap_num += 1
        




from threading import Timer
from csv import DictWriter
    ##INIT GPS OBJ` `, CHECK FOR ERROR, RETURN TEST MODE
gps = gps_util.gps_util()
if(gps.test_mode == True):
    mode = "test"
    print("continuing in testmode")
else:
    ## IF TEST MODE is NOT Triggered, Start Log System and GPS udate Loope
    # Log Writer
    #log_file.open('log.csv', 'w')
    #log_writer = DictWriter(log_file, fieldnames=['timestamp', 'gps_lock', 'latitude', 'longitude', 'heading', 'speed', 'fuel_volume'])
    #log_writer.writeheader()

    # ready_button = Button(READY_START_PIN)
    # fuel_sensor = Button(FUEL_SENSE_PIN)

    # ready_button.when_pressed = update_ready_state
    # fuel_sensor.when_pressed = update_fuel_volume
    # GPS Update Clock
    Timer(1/UPDATE_FREQUENCY, gps.update_gps()).start() 
        # Log Update Clock  
    #Timer(1/UPDATE_FREQUENCY, write_log).start()

from math import isclose, sin

app = Flask(__name__)

@app.before_request
def check_mode():
    if mode == 'test':
        global ready_state, diff_state, current_fuel_volume
        ready_state = sin(time.time()) >= 0
        diff_state = sin(time.time()) >= 0
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
        "lock": gps.get_lock(),
        "speed": gps.get_speed(),
        "heading":gps.get_heading()
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
