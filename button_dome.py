#!/usr/bin/python3

#--------------------------------------------------------------------
# Automation of Stickney Observatory pt 1                           -
# button_dome.py - A program written to allow the use of buttons    -
#  to control the dome's motion.				    -
# Author(s): Amanda Bacon, Emma Salazar, Anna McNiff, Josie Bunnell -
#--------------------------------------------------------------------

# Import modules for our program
import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

print("restart test")

# UI import
from flask import Flask, request, abort, jsonify
import json

# Create an instance of Flask and tie it to this python program
app = Flask(__name__)

print("restart test")

# Set our notch counter to start at 0
notches = 0

#GPIO Setup
# We have many event detects, and also a while True: pass, so we include a GPIO.cleanup() to initially cleanup the program
GPIO.cleanup()

# Set warnings to false
GPIO.setwarnings(False)

# Set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

# Buttons Setup
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP) #counter clockwise button
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home button
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) #e stop button
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #clockwise button

# IR Sensors Setup
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP) #notch count IR sensor
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home IR sensor

# Relays Setup
pin_list = [11,13,15,16,18] # create list of relay GPIO pins

# Set up GPIO pin list for relays
for i in pin_list:
	GPIO.setup(i, GPIO.OUT)

power_relays = (11,16,18) # allows for simultaneous pin manipulation, where 'power' means dome movement 
directional_relays = (13,15) # allows for simultaneous pin manipulation, where 'directional' means setup of relays
#GPIO.setup(11, GPIO.OUT) # R0,R00 relay
#GPIO.setup(13, GPIO.OUT) # R1 relay
#GPIO.setup(15, GPIO.OUT) # R2 relay
#GPIO.setup(16, GPIO.OUT) # R3 relay
#GPIO.setup(18, GPIO.OUT) # R4 relay

# IR Sensor notch count function (prints the beam state and notch count)
def print_IR_state(input):
    input = GPIO.input(36)
    print("This is the input", input) # 0 for interference, 1 for solid
    global notches # set notches as a global variable
    if input != 0: # if the sensor is not blocked; i.e., is in a notch hole,
        print("Solid") # print "solid," indicative of no interference
        notches = notches + 1 # add to our counter,
        print(notches) # then print the current notch value
    else: # otherwise, if the sensor is blocked,
        print("Beam interference") # print that there is an interference.
#GPIO.add_event_detect(36, GPIO.BOTH, callback = print_IR_state)

# IR Sensor notch count function (returns the notch count and does not print anything)
def notch_counter(input):
    input = GPIO.input(36)
    direction_relay = GPIO.input(13) # use this variable after chosing an arbitrary relay that goes high or low depending on the direction. We count based on the direction the dome is moving
    global notches
    if input != 0 and direction_relay == False: # the sensor is in a notch hole, and the dome is moving clockwise
        notches = notches + 1
        print(notches)
    elif input != 0 and direction_relay == True: # the sensor is in a notch hole, and the dome is moving counter clockwise
        notches = notches - 1 #thereby subtracting from the notch count
        print(notches)
GPIO.add_event_detect(36, GPIO.BOTH, callback = notch_counter) #waits for the sensor to sense a change in input

# When e stop button is pressed, set the relays to low and restart the code
def emergency_stop(e_stop):
    e_stop = GPIO.input(22)
    print("Stopping all systems.")
    GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
    time.sleep(0.1) # allow for directional relays to switch before power_relays
    GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    print("Restarting the program.")
    python = sys.executable
#    os.execl(python, python, *sys.argv)
    os.execl(python, os.path.abspath(__file__), *sys.argv)
#    os.system('python "~/Dome/button_dome.py"')
    sys.exit(0)	
GPIO.add_event_detect(22, GPIO.FALLING, callback = emergency_stop)

# Error handling with buttons:
def error_handle():
    button_status_c = GPIO.input(7)
#    button_status_cc = GPIO.input(8)
    button_status_home = GPIO.input(10)
    e_stop = GPIO.input(22)
#    if button_status_c == False and button_status_cc == False: # Error handling. User cannot push both buttons. Dome will not move.
#        print("Not allowed to press both clockwise and counterclockwise. Not moving.")
#        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
#        time.sleep(0.1) # allow for directional relays to switch before power_relays
#        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    if button_status_c == False and button_status_home == False: # Error handling. User cannot push both buttons. Dome will not move.
        print("Not allowed to press both clockwise and home. Not moving.")
        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
        time.sleep(0.1) # allow for directional relays to switch before power_relays
        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
#    if button_status_cc == False and button_status_home == False: # Error handling. User cannot push both buttons. Dome will not move.
#        print("Not allowed to press both counterclockwise and home. Not moving.")
#        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
#        time.sleep(0.1) # allow for directional relays to switch before power_relays
#        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    if button_status_c == False and e_stop == False: # Error handling. User cannot push both buttons. Dome will not move.
        print("Not allowed to press both clockwise and e stop. Not moving.")
        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
        time.sleep(0.1) # allow for directional relays to switch before power_relays
        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
#    if button_status_cc == False and e_stop == False: # Error handling. User cannot push both buttons. Dome will not move.
#        print("Not allowed to press both counter clockwise and e stop. Not moving.")
#        GPIO.output(directional_relays, GPIO.LOW) # set relays R1 and R2 to low simultaneously
#        time.sleep(0.1) # allow for directional relays to switch before power_relays
#        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    if button_status_home == False and e_stop == False: # Error handling. User cannot push both buttons. Dome will not move.
        print("Not allowed to press both home and e stop. Not moving.")
        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
        time.sleep(0.1) # allow for directional relays to switch before power_relays
        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously

# Motor functions:
# Dome clockwise movement, set specific relays to high and low
def go_clockwise():
    GPIO.output(directional_relays, GPIO.LOW) # set relays R1 and R2 to low simultaneously
    time.sleep(0.2) # allow for directional relays to switch before power_relays
    GPIO.output(power_relays, GPIO.HIGH) # set relays R0,R00,R3,R4 to high simultaneously
    print("Moving clockwise.")

# Dome counter clockwise movement, set all relays to high
#def go_counter_clockwise():
#    GPIO.output(directional_relays, GPIO.HIGH)  #set relays R1 and R2 to high simultaneously
#    time.sleep(0.2) #allow for directional relays to switch before power_relays
#    GPIO.output(power_relays, GPIO.HIGH) # set relays R0,R00,R3,R4 to high simultaneously
#    print("Moving counter clockwise.")

# Stop the motor, set all relays to low
def stop_motor():
    GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
    time.sleep(0.2) # allow for directional relays to switch before power_relays
    GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    print("Stopping motor.")

# Home button:
# When the user presses the home button, it will move in the clockwise direction until the beam is broken, indicating home position has been reached
def go_home(button_status_home):
    button_status_home = GPIO.input(10)
    home_sensor = GPIO.input(35)
    if button_status_home == False: # if button has been pressed,
        print("Home button pressed. Going home.")
    if home_sensor != 0: # if there is no intereference,
        go_clockwise() # move the dome in the clockwise direction
    if home_sensor == 0: # if there is interference,
        print ("At home position.")
        stop_motor()
time.sleep(0.3) # adds to the debounce of buttons
GPIO.add_event_detect(10, GPIO.BOTH, callback = go_home, bouncetime = 300) # bouncetime adds a debounce to the buttons
GPIO.add_event_detect(35, GPIO.FALLING, callback = go_home, bouncetime = 300)

# True = 1, False = 0
# Button clockwise and counter clockwise logic
def moving(button_status_cc):
    button_status_cc = GPIO.input(8)
    button_status_c = GPIO.input(7)
    button_status_home = GPIO.input(10)
    e_stop = GPIO.input(22)
    if button_status_c == False: # if the clockwise button is pressed, print status and set relays to high and low
        print("Clockwise button pressed. Moving clockwise.")
        GPIO.output(directional_relays, GPIO.LOW) # set relays R1 and R2 to low simultaneously
        time.sleep(0.2) # allow for directional relays to switch before power_relays
        GPIO.output(power_relays, GPIO.HIGH) # set relays R0,R00,R3,R4 to high simultaneously
        print_IR_state(input) # call the IR notch count function to obtain counts
#    elif button_status_cc == False: # if the counterclockwise button is pressed, print the status and set all relays to high.
#        print("Counter clockwise button pressed. Moving counter clockwise.")
#        GPIO.output(directional_relays, GPIO.HIGH)  #set relays R1 and R2 to high simultaneously
#        time.sleep(0.2) #allow for directional relays to switch before power_relays
#        GPIO.output(power_relays, GPIO.HIGH) # set relays R0,R00,R3,R4 to high simultaneously
#        print_IR_state(input) # call the IR notch count function to obtain counts
    elif button_status_c == True and button_status_cc == True: # if both clockwise and counter clockwise are not pressed, dome is not moving
        print("Not moving.")
        GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
        time.sleep(0.2) # allow for directional relays to switch before power_relays
        GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
# Error handling with buttons:
        error_handle()
time.sleep(0.3) # adds to the debounce of buttons
GPIO.add_event_detect(8, GPIO.BOTH, callback = moving, bouncetime = 300) # bouncetime adds a debounce to the buttons
GPIO.add_event_detect(7, GPIO.BOTH, callback = moving, bouncetime = 300) # bouncetime adds a debounce to the buttons

try:
    while True:
        pass

except KeyboardInterrupt:
    GPIO.output(directional_relays, GPIO.LOW)  # set relays R1 and R2 to low simultaneously
    time.sleep(0.1) # allow for directional relays to switch before power_relays
    GPIO.output(power_relays, GPIO.LOW) # set relays R0,R00,R3,R4 to low simultaneously
    GPIO.cleanup()

GPIO.cleanup()
