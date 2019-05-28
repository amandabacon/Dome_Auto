#!/usr/bin/python3

#--------------------------------------------------------------------
#Author(s): Amanda Bacon, Anna McNiff, Emma Salazar, Josie Bunnell  -
#Automation of Stickney Observatory                                 -
#--------------------------------------------------------------------

# Import stuff for our program
import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

# UI import stuff
from flask import Flask, request, abort, jsonify
import json

# create an instance of Flask and tie it to this python program
app = Flask(__name__)

# Set our notch counter to start at 0
notches = 0


#GPIO Setup

# Because we have so many event detect, and also a while True: pass, we include a GPIO.cleanup() here to initially cleanup
GPIO.cleanup()

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
GPIO.setup(11, GPIO.OUT) #R0,R00 relay
GPIO.setup(13, GPIO.OUT) #R1 relay
GPIO.setup(15, GPIO.OUT) #R2 relay
GPIO.setup(16, GPIO.OUT) #R3 relay
GPIO.setup(18, GPIO.OUT) #R4 relay


#IR Sensor Counting Notches Function (which prints the beam state and notch count)
def print_IR_state(input):
    input = GPIO.input(36)
    print("This is the input", input) #0 for interference, 1 for solid
    global notches # set our notches as a global function
    if input != 0: # if the sensor is not blocked, i.e. is in a notch hole,
        print("Solid") # print "solid,"
        notches = notches + 1 # add to our counter,
        print(notches) # and print the current notch value
    else: # otherwise, if the sensor is blocked,
        print("Beam interference") # print that there is an interference.
#GPIO.add_event_detect(36, GPIO.BOTH, callback = print_IR_state)

# IR Sensor Counting Notches Function (which returns the notch count and does not print anything)
def notch_counter(input):
    input = GPIO.input(36)
    direction_relay = GPIO.input(13) # Emma: I added this variable by chosing an arbitrary relay that goes high or low depending on the direction so we can count based on the direction the dome is moving
    global notches
    if input != 0: #and direction_relay == False: # the sensor is in a notch hole, and the dome is moving clockwise
        notches = notches + 1
#    if input != 0 and direction_relay == True: # the sensor is in a notch hole, and the dome is moving counter clockwise
#        notches = notches - 1 # thereby subtracting from the notch count
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
GPIO.add_event_detect(22, GPIO.FALLING, callback = restart)

# Alternative e stop code
def emergency_stop(e_stop):
    e_stop = GPIO.input(22)
    print("Stopping all systems.")
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(18, GPIO.LOW) #R4
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(16, GPIO.LOW) #R3
    print("Restarting the program.")
    python = sys.executable
    os.execl(python, python, *sys.argv)
#GPIO.add_event_detect(22, GPIO.FALLING, callback = restart)


#Motor functions
#clockwise movement
def go_clockwise():
    return 1
#    print("Moving clockwise.")
#    GPIO.output(11, GPIO.HIGH) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(16, GPIO.HIGH) #R3
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(18, GPIO.HIGH) #R4

#counter clockwise movement
def go_counter_clockwise():
    return 1
#    print("Moving counter clockwise.")
#    GPIO.output(15, GPIO.HIGH) #R2
#    GPIO.output(18, GPIO.HIGH) #R4
#    GPIO.output(11, GPIO.HIGH) #R0,R00
#    GPIO.output(13, GPIO.HIGH) #R1
#    GPIO.output(16, GPIO.HIGH) #R3

#stop the motor
def stop_motor():
    print("Stopping motor.")
#    GPIO.output(11, GPIO.LOW) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(16, GPIO.LOW) #R3
#    GPIO.output(18, GPIO.LOW) #R4

#Home button
def go_home(button_status_home):
    button_status_home = GPIO.input(10)
    if button_status_home == False:
        print("Home button pressed. Going home.")
def at_home(home_sensor):
    home_sensor = GPIO.input(35)
    if home_sensor != 0:
        go_clockwise()
    if home_sensor == 0:
        print ("At home position.")
        stop_motor()
GPIO.add_event_detect(10, GPIO.FALLING, callback = go_home, bouncetime = 100)
GPIO.add_event_detect(35, GPIO.FALLING, callback = at_home)

# Get our azimuth
def get_azimuth(user_input):
    user_azimuth = user_input * (494/360)
    return user_azimuth

# Go to our first location given user input from an html page
@app.route("/next-location", methods=['POST'])
def go_location():
    next_location_string = '<html>\n <head>\n <title>\n Stickney Observatory Dome Control\n </title>\n </head>\n <body>\n What azimuth is the telescope going to next?\n <form action=" " method="POST">\n <br>\n Azimuth:\n <input type="submit" name="azimuth" value="Go">\n <br>\n Or are you finished using the dome?\n <input type="submit" name="shut_down" value="Shut Down System">\n </form>\n </body>\n </html>\n'
    try:
        azimuth_value = int(request.form['azimuth'])
        if azimuth_value > 360:
            bad = "That azimuth is too big, please go back and try again."
            return bad
        elif request.form['azimuth'] <= 0:
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
                return next_location_string
            else:
                stop_motor()
    except ValueError:
        bad = "You gave me a string, not an integer. Please go back and try again."
        return bad

def go_location_test():
    azimuth = int(get_azimuth(4))
    input = GPIO.input(36)
    global notches
    if(notches < azimuth):
        while notches < azimuth:
#            print("Going clockwise.")
            go_clockwise()
    elif(notches > azimuth):
        while notches > azimuth:
#            print("Going counter clockwise.")
            go_counter_clockwise()
    else:
        stop_motor()
    stop_motor()


#True = 1, False = 0
#Button clockwise and counter clockwise
def moving(button_status_cc):
    button_status_cc = GPIO.input(8)
    button_status_c = GPIO.input(7)
    if button_status_c == False:
        print("Clockwise button pressed. Moving clockwise.")
#        GPIO.output(11, GPIO.HIGH) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(16, GPIO.HIGH) #R3
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(18, GPIO.HIGH) #R4
        print_state(input)
    elif button_status_cc == False:
        print("Counter clockwise button pressed. Moving counter clockwise.")
#        GPIO.output(15, GPIO.HIGH) #R2
#        GPIO.output(18, GPIO.HIGH) #R4
#        GPIO.output(11, GPIO.HIGH) #R0,R00
#        GPIO.output(13, GPIO.HIGH) #R1
#        GPIO.output(16, GPIO.HIGH) #R3
        print_state(input)
    elif button_status_c == True and button_status_cc == True:
        print("Not moving.")
#        GPIO.output(11, GPIO.LOW) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(16, GPIO.LOW) #R3
#        GPIO.output(18, GPIO.LOW) #R4
    if button_status_c == False and button_status_cc == False:
        print("Not allowed to press both buttons. Not moving.")
#        GPIO.output(11, GPIO.LOW) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(16, GPIO.LOW) #R3
#        GPIO.output(18, GPIO.LOW) #R4
time.sleep(0.25)
GPIO.add_event_detect(8, GPIO.FALLING, callback = moving, bouncetime = 100)
GPIO.add_event_detect(7, GPIO.FALLING, callback = moving, bouncetime = 100)

try:
    while True:
        pass

except KeyboardInterrupt:
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(18, GPIO.LOW) #R4
#    GPIO.output(11, GPIO.LOW) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(16, GPIO.LOW) #R3
    GPIO.cleanup()

#GPIO.cleanup()

