##INITIALIZE USEFUL GLOBALS
import numpy as np


class gps_util:
    
    def __init__(self):
        self.gps_location = {'latitude': 0, 'longitude': 0}
        self.gps_heading = 0
        self.gps_speed = 0 # kts
        self.gps_lock = False
        self.gps_start_location = {'latitude': 0, 'longitude': 0}  
        self.testmode = False
        try:
             from gpiozero import Button
             import serial
             import adafruit_gps
             self.uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
             self.gps = adafruit_gps.GPS(self.uart, debug=False)
             self.gps.send_command("PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")      
        except ImportError:
             import math, numpy as np
             self.gps_heading = 300
             self.gps_speed = 69
             self.test_mode = True
  # /////////////////////////////////////////// #
  # Update GPS
  # A Simple Helper Method for updating 
  #        
    def update_gps(self):
     
        if(self.test_mode == False):
            try:
                self.gps_lock = self.gps.has_fix
                self.gps_location['latitude'] = self.gps.latitude
                self.gps_location['longitude'] = self.gps.longitude
                self.gps_heading = round(self.gps.track_angle_deg) if self.gps.track_angle_deg is not None else 0
                self.gps_speed = round(self.gps.speed_knots * 463 / 900) if self.gps.speed_knots is not None else 0 # 1 knot = 463/900 m/s
            except:
                exit("GPS Failed to Update :(")
        else:
            return self.test_mode
  # /////////////////////////////////////////// #
  # Set Start
  # A Simple Method for marking start/finishline 
  #        
    def set_start(self):
        
        self.update_gps()
        if self.gps_lock:
            self.gps_start_location = self.gps_start_location
        return self.gps_start_location
  # /////////////////////////////////////////// #
  # Set Start
  # A Simple Method for getting start/finishline data  
  #        
    def get_start(self):
        return self.gps_start_location    
    def get_location(self):
        if(self.gps_lock_):
            return self.gps_location
        else:
            return -1
    def get_speed(self):
        return self.gps_speed
    def get_heading(self):
        return self.gps_heading  
    def get_lock(self):
        return self.gps_lock   
        