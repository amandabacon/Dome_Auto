#!/usr/bin/python3

#------------------------------------
#Author(s): Amanda Bacon            -
#Automation of Stickney Observatory -
#------------------------------------

import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
GPIO.setup(18, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#IR 
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
test = GPIO.input(16)
def my_callback(test):
    try:
        test = GPIO.input(16)
        if test == 0:
            print("interfere")
#            notch_ir = test
#            return notch_ir
        if test != 0:
            print("solid")
#            notch_ir = test
#            return notch_ir
        GPIO.add_event_detect(16, GPIO.BOTH, callback = my_callback)
        while True:
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()
my_callback(test)

#This one breaks the loop if e-stop pressed, then continues on to whatever is next. In this case, test.
#try:
#    while True:
#        button_status_s = GPIO.input(7)
#        button_status_c = GPIO.input(8)
#        button_status_cc = GPIO.input(10)
#        if button_status_s == False:
#            print("ESTOP")
#            break
#except KeyboardInterrupt:
#    GPIO.cleanup()

#print("test")

#prints restart as long as all three buttons are pushed--not ideal
#while True:
#    button_status_s = GPIO.input(7)
#    button_status_c = GPIO.input(8)
#    button_status_cc = GPIO.input(10)
#    if button_status_s == False and button_status_c == False and button_status_cc == False:
#        print("restart")

#Closer. Now breaks loop and prints restart
#while True:
#    button_status_s = GPIO.input(7)
#    button_status_c = GPIO.input(8)
#    button_status_cc = GPIO.input(10)
#    if button_status_s == False and button_status_c == False and button_status_cc == False:
#        break

#print("restart")




#WORK ON THIS CASE
#https://stackoverflow.com/questions/16143842/raspberry-pi-gpio-events-in-python
#https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#button_status_s = GPIO.input(7)
#def e_stop(button_status_s):
#    button_status_s = GPIO.input(7)
#    if button_status_s == False:
#        print("Pressed")
##        GPIO.add_event_detect(7, GPIO.FALLING, callback = e_stop)
#GPIO.add_event_detect(7, GPIO.FALLING, callback = e_stop)
#while True: #need this part to wait for signal...
#    pass

#e_stop(button_status_s)
#WORK ON THIS CASE

#print("rr")

#WORK ON THIS CASE
#button_status_s = GPIO.input(7)
#button_status_c = GPIO.input(8)
#button_status_cc = GPIO.input(10)
#def t(button_status_s,button_status_c,button_status_cc):
#    button_status_s = GPIO.input(7)
#    button_status_c = GPIO.input(8)
#    button_status_cc = GPIO.input(10)
#    if button_status_s == False and button_status_c == False and button_status_cc == False:
#        print("restart")
#GPIO.add_event_detect(7, GPIO.FALLING, callback = t)
#GPIO.add_event_detect(8, GPIO.FALLING, callback = t)
#GPIO.add_event_detect(10, GPIO.FALLING, callback = t)
#while True:
#    pass

#t(button_status_s,button_status_c,button_status_cc)
#if __name__ == '__main__':
#    t(button_status_s,button_status_c,button_status_cc)
#    os.execv(sys.executable, ['python3'] + sys.argv)
#    os.execv(__file__, sys.argv)
#WORK ON THIS CASE

#GOOOOOOODDDDDDDDD
#button_status = GPIO.input(10)
#def loop(button_status):
#    try:
#        button_status = GPIO.input(10)
#        if button_status == 1:
#            GPIO.output(7, GPIO.HIGH)
#        if button_status == 0:
#            GPIO.output(7, GPIO.LOW)
#        GPIO.add_event_detect(10, GPIO.BOTH, callback = loop)
#        while True:
#                pass

#    except KeyboardInterrupt:
#        GPIO.cleanup()
#loop(button_status)
#GOOOOOOOOODDDDDDDD
