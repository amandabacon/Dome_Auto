#!/usr/bin/python3

#------------------------------------
#Author(s): Emma the best coder ever            -
#Emma is always right -
#------------------------------------

import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

GPIO.cleanup()

#set warnings to false
GPIO.setwarnings(False)

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#current = GPIO.input(36)
notches = 0

def print_state(input):
	input = GPIO.input(36)
	print(input)
	global notches
	if input != 0:
		print("solid")
		notches = notches + 1
		print(notches)
	else:
		print("interfere")

GPIO.add_event_detect(36, GPIO.BOTH, callback = print_state)

while True:
	pass
