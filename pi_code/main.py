#!/usr/bin/python3

#--------------------------------------------------------------------
#Authors: Amanda Bacon, Anna McNiff, Emma Salazar and Josie Bunnell -
#Test python document with important setup to test functions        -
#--------------------------------------------------------------------

import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

#set warnings to false
GPIO.setwarnings(False)

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

#Button setup
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#IR setup
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Relay setup
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
