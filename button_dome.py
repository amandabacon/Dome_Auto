#!/usr/bin/python3

#--------------------------------------------------------------------
# Automation of Stickney Observatory pt 1                           -
# button_dome.py - A program written to allow the use of buttons    -
#  to control the dome's motion.                                   -
# Author(s): Amanda Bacon, Anna McNiff, Emma Salazar, Josie Bunnell -
#--------------------------------------------------------------------

# Import modules for our program
import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

# UI import
from flask import Flask, request, abort, jsonify
import json

# create an instance of Flask and tie it to this python program
app = Flask(__name__)

# Set our notch counter to start at 0
notches = 0

#GPIO Setup
# Because we have many event detects, and also a while True: pass, we include a GPIO.cleanup() here to initially cleanup the program
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
power_relays = (11,16,18)
directional_relays = (13,15)
not_pushed_relays = (11,13,15,16,18)
GPIO.setup(11, GPIO.OUT) #R0,R00 relay
GPIO.setup(13, GPIO.OUT) #R1 relay
GPIO.setup(15, GPIO.OUT) #R2 relay
GPIO.setup(16, GPIO.OUT) #R3 relay
GPIO.setup(18, GPIO.OUT) #R4 relay

#IR Sensor counting notches function (prints the beam state and notch count)
def print_IR_state(input):
    input = GPIO.input(36)
    print("This is the input", input) #0 for interference, 1 for solid
    global notches #set notches as a global variable
    if input != 0: #if the sensor is not blocked; i.e., is in a notch hole,
        print("Solid") #print "solid," indicative of no interference
        notches = notches + 1 #add to our counter,
        print(notches) #then print the current notch value
    else: #otherwise, if the sensor is blocked,
        print("Beam interference") #print that there is an interference.
#GPIO.add_event_detect(36, GPIO.BOTH, callback = print_IR_state)

#IR Sensor counting notches function (returns the notch count and does not print anything)
def notch_counter(input):
    input = GPIO.input(36)
    direction_relay = GPIO.input(13) #Use this variable after chosing an arbitrary relay that
    #goes high or low depending on the direction so we can count based on the direction the dome is moving
    global notches
    if input != 0: #and direction_relay == False:--the sensor is in a notch hole, and the dome is moving clockwise
        notches = notches + 1
#    if input != 0 and direction_relay == True:--the sensor is in a notch hole, and the dome is moving counter clockwise
#        notches = notches - 1 #thereby subtracting from the notch count
GPIO.add_event_detect(36, GPIO.BOTH, callback = notch_counter) #waits for the sensor to sense a change in input

#E stop button--completely quits program instead of rebooting (need to put in /etc/rc.local file)
#When e stop button is pressed, set the relays to low and restart the code
def restart(e_stop):
    e_stop = GPIO.input(22)
    print("Set relays to low")
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(18, GPIO.LOW) #R4
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(16, GPIO.LOW) #R3
    os.system("sudo shutdown -r now") #sudo reboot
GPIO.add_event_detect(22, GPIO.FALLING, callback = restart)

#Alternative e stop code
#When e stop button is pressed, set the relays to low and restart the code
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


#Motor functions:
#clockwise movement, set specific relays to high and low
def go_clockwise():
    print("Moving clockwise.")
#    GPIO.output(11, GPIO.HIGH) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(16, GPIO.HIGH) #R3
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(18, GPIO.HIGH) #R4

#counter clockwise movement, set all relays to high
def go_counter_clockwise():
    print("Moving counter clockwise.")
#    GPIO.output(15, GPIO.HIGH) #R2
#    GPIO.output(18, GPIO.HIGH) #R4
#    GPIO.output(11, GPIO.HIGH) #R0,R00
#    GPIO.output(13, GPIO.HIGH) #R1
#    GPIO.output(16, GPIO.HIGH) #R3

#stop the motor, set all relays to low
def stop_motor():
    print("Stopping motor.")
#    GPIO.output(11, GPIO.LOW) #R0,R00
#    GPIO.output(13, GPIO.LOW) #R1
#    GPIO.output(15, GPIO.LOW) #R2
#    GPIO.output(16, GPIO.LOW) #R3
#    GPIO.output(18, GPIO.LOW) #R4

#Home button:
#When the user presses the home button, it will move in the clockwise direction
#until the beam is broken, indicating home position has been reached
def go_home(button_status_home):
    button_status_home = GPIO.input(10)
    if button_status_home == False: #if button has been pressed,
        print("Home button pressed. Going home.")
        
#Once the dome is in home position
def at_home(home_sensor): 
    home_sensor = GPIO.input(35)
    if home_sensor != 0: #if there is no intereference,
        go_clockwise() #move the dome in the clockwise direction
    if home_sensor == 0: #if there is interference,
        print ("At home position.") 
        stop_motor()
GPIO.add_event_detect(10, GPIO.FALLING, callback = go_home, bouncetime = 100) #bouncetime adds a debounce to the buttons
GPIO.add_event_detect(35, GPIO.FALLING, callback = at_home)

#True = 1, False = 0
#Button clockwise and counter clockwise logic
def moving(button_status_cc):
    button_status_cc = GPIO.input(8)
    button_status_c = GPIO.input(7)
    if button_status_c == False: #if the clockwise button is pressed, print status and set relays to high and low
        print("Clockwise button pressed. Moving clockwise.")
        GPIO.output(directional_relays, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(power_relays, GPIO.HIGH)
#        GPIO.output(11, GPIO.HIGH) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(16, GPIO.HIGH) #R3
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(18, GPIO.HIGH) #R4
        print_IR_state(input) #call the IR notch count function to obtain counts
    elif button_status_cc == False: #if the counterclockwise button is pressed, print the status and set all relays to high.
        print("Counter clockwise button pressed. Moving counter clockwise.")
        GPIO.output(directional_relays, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(power_relays, GPIO.HIGH)
#        GPIO.output(15, GPIO.HIGH) #R2
#        GPIO.output(18, GPIO.HIGH) #R4
#        GPIO.output(11, GPIO.HIGH) #R0,R00
#        GPIO.output(13, GPIO.HIGH) #R1
#        GPIO.output(16, GPIO.HIGH) #R3
        print_IR_state(input) #call the IR notch count function to obtain counts
    elif button_status_c == True and button_status_cc == True: #if both clockwise and counter clockwise are not pressed,
        #dome is not moving
        print("Not moving.")
        GPIO.output(not_pushed_relays, GPIO.LOW)
#        GPIO.output(11, GPIO.LOW) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(16, GPIO.LOW) #R3
#        GPIO.output(18, GPIO.LOW) #R4
    if button_status_c == False and button_status_cc == False: #Error handling. User cannot push both buttons. Dome will not move.
        print("Not allowed to press both buttons. Not moving.")
        GPIO.output(not_pushed_relays, GPIO.LOW)
#        GPIO.output(11, GPIO.LOW) #R0,R00
#        GPIO.output(13, GPIO.LOW) #R1
#        GPIO.output(15, GPIO.LOW) #R2
#        GPIO.output(16, GPIO.LOW) #R3
#        GPIO.output(18, GPIO.LOW) #R4
time.sleep(0.25) #adds to the debounce of buttons
GPIO.add_event_detect(8, GPIO.FALLING, callback = moving, bouncetime = 100) #bouncetime adds a debounce to the buttons
GPIO.add_event_detect(7, GPIO.FALLING, callback = moving, bouncetime = 100) #bouncetime adds a debounce to the buttons

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

