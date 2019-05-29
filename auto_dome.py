#!/usr/bin/python3

#--------------------------------------------------------------------
# Automation of Stickney Observatory pt 2                           -
# auto_dome.py - A program written to allow the use of a user       -
#  interface to control the dome's motion.                          -
# Author(s): Amanda Bacon, Anna McNiff, Emma Salazar, Josie Bunnell -
#--------------------------------------------------------------------

# Import stuff for our program
import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

# UI import stuff
from flask import Flask, request, abort, jsonify, url_for, redirect, render_template
import json

# create an instance of Flask and tie it to this python program
app = Flask(__name__)

# Set our notch counter to start at 0
notches = 0


#GPIO Setup

#set warnings to false
GPIO.setwarnings(False)

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

#Buttons Setup
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP) #counter clockwise button
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home button
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) #e stop button
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #clockwise button

#IR Sensors Setup
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP) #notch count IR sensor
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home IR sensor

#Relays Setup
power_relays = (11,16,18)
directional_relays = (13,15)
not_pushed_relays = (11,13,15,16,18)
GPIO.setup(11, GPIO.OUT) #R0,R00 relay
GPIO.setup(13, GPIO.OUT) #R1 relay
GPIO.setup(15, GPIO.OUT) #R2 relay
GPIO.setup(16, GPIO.OUT) #R3 relay
GPIO.setup(18, GPIO.OUT) #R4 relay


#Functions

# IR Sensor Counting Notches Function (which returns the notch count and does not print anything)
def notch_counter(input):
    input = GPIO.input(36)
    direction_relay = GPIO.input(13) # Emma: I added this variable by chosing an arbitrary relay that goes high or low depending on the direction so we can count based on the direction the dome is moving
    global notches
    if input != 0 and direction_relays == False: # the sensor is in a notch hole, and the dome is moving clockwise
        notches = notches + 1
    if input != 0 and direction_relay == True: # the sensor is in a notch hole, and the dome is moving counter clockwise
        notches = notches - 1 # thereby subtracting from the notch count
GPIO.add_event_detect(36, GPIO.BOTH, callback = notch_counter) # waits for the sensor to sense a change in input

#E stop button--completely quits program instead of rebooting (need to put in /etc/rc.local file)
def restart(e_stop):
    e_stop = GPIO.input(22)
    print("Set relays to low")
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(18, GPIO.LOW) #R4
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(16, GPIO.LOW) #R3
    os.system("sudo shutdown -r now") #sudo reboot
#GPIO.add_event_detect(22, GPIO.FALLING, callback = restart)

#Motor functions
#clockwise movement
def go_clockwise():
#    print("Moving clockwise.")
    GPIO.output(11, GPIO.HIGH) #R0,R00
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(16, GPIO.HIGH) #R3
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(18, GPIO.HIGH) #R4

#counter clockwise movement
def go_counter_clockwise():
#    print("Moving counter clockwise.")
    GPIO.output(13, GPIO.HIGH) #R1
    GPIO.output(15, GPIO.HIGH) #R2
    time.sleep(0.1)
    GPIO.output(16, GPIO.HIGH) #R3
    GPIO.output(18, GPIO.HIGH) #R4
    GPIO.output(11, GPIO.HIGH) #R0,R00

#stop the motor
def stop_motor():
    print("Stopping motor.")
    GPIO.output(11, GPIO.LOW) #R0,R00
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(16, GPIO.LOW) #R3
    GPIO.output(18, GPIO.LOW) #R4

# Get our azimuth
def get_azimuth(user_input):
    user_azimuth = user_input * (494/360)
    return user_azimuth

# Go to our first location given user input from an html page
@app.route("/next-location", methods=['POST'])
def go_location():
    go_location_string = '<html>\n <head><title>Welcome to the Stickney Observatory Dome Control</title>\n </head>\n <body>\n \n Hello user. What azimuth is the telescope going to?\n <form action="http://raspberrypi23.local:5000/next-location" method="POST">\n <br>\n Azimuth:\n <input type="number" name="azimuth">\n <input type="submit" name="go" value="Go">\n <br>\n Do you want to go home?\n <input type="submit" name="home" value="Go Home">\n <br>\n Are you finished using the dome?\n <input type="submit" name="shutdown" value="Shut Down System">\n <br>\n Emergency Stop\n <input type="submit" name="estop" value="Emergency Stop">\n <br>\n \n </form>\n </body>\n </html>'
    if request.method == 'POST':
        if request.form['go'] == 'Go':
            try:
                azimuth_value = int(request.form['azimuth'])
                if azimuth_value > 360:
                    bad = "That azimuth is too big, please go back and try again."
                    return bad
                elif azimuth_value <= 0:
                    bad = "That azimuth is too small, please go back and try again."
                    return bad
                else:
                    azimuth = int(get_azimuth(azimuth_value))
                    global notches
                    if(notches < azimuth):
                        while notches < azimuth:
                            go_clockwise()
                    elif(notches > azimuth):
                        while notches > azimuth:
                            go_counter_clockwise()
                    elif(notches == azimuth): # Emma: I was nervous about the else statement not catching it when it equals the azimuth, so i put this in as a duplicate to be safe?
                        stop_motor()
                        print("Dome moved and motor stopped.")
                        return go_location_string
                    else:
                        stop_motor()
            except ValueError:
                bad = "You gave me a string, not an integer. Please go back and try again."
                return bad
        elif request.form['home'] == 'Go Home':
#            home_sensor = GPIO.input(35)
#            while home_sensor != 0:
#                go_clockwise()
#            stop_motor()
            return "At home position."
        elif request.form['shutdown'] == 'Shut Down System':
#            GPIO.output(11, GPIO.LOW) #R0,R00
#            GPIO.output(13, GPIO.LOW) #R1
#            GPIO.output(15, GPIO.LOW) #R2
#            GPIO.output(16, GPIO.LOW) #R3
#            GPIO.output(18, GPIO.LOW) #R4
            return "Stopping motor. Shutting down."
        elif request.form['estop'] == 'Emergency Stop':
#            GPIO.output(11, GPIO.LOW) #R0,R00
#            GPIO.output(13, GPIO.LOW) #R1
#            GPIO.output(15, GPIO.LOW) #R2
#            GPIO.output(16, GPIO.LOW) #R3
#            GPIO.output(18, GPIO.LOW) #R4
            return "Everything has shut down."

# Go home
#def go_home():
#    if request.form['home'] == 'Go Home':
#        home_sensor = GPIO.input(35)
#        while home_sensor != 0:
#            go_clockwise()
#        print ("At home position.")
#        stop_motor()

#Or shut the system down
#def shut_down():
#    if request.form['shut_down'] == 'Shut Down System':
#        GPIO.output(11, GPIO.LOW) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(16, GPIO.LOW) #R3
#        GPIO.output(18, GPIO.LOW) #R4
#        return "Stopping motor. Shutting down."

#def go_location_test():
#    azimuth = int(get_azimuth(4))
#    input = GPIO.input(36)
#    global notches
#    if(notches < azimuth):
#        while notches < azimuth:
#            print("Going clockwise.")
#            go_clockwise()
#    elif(notches > azimuth):
#        while notches > azimuth:
#            print("Going counter clockwise.")
#            go_counter_clockwise()
#    else:
#        stop_motor()
#    stop_motor()


#try:
#    while True:
#        pass

#except KeyboardInterrupt:
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(18, GPIO.LOW) #R4
#    GPIO.output(11, GPIO.LOW) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(16, GPIO.LOW) #R3
#    GPIO.cleanup()

#GPIO.cleanup()
