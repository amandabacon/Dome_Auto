#!/usr/bin/python3

#------------------------------------------------------------------------
#Author(s): Amanda Bacon, Anna McNiff, Emma Salazar, Josie Bunnell	-
#Automation of Stickney Observatory					-
#------------------------------------------------------------------------

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

#Buttons
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#IR
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Relays
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#button_status_cc = GPIO.input(8)
#button_status_c = GPIO.input(7)
def moving(button_status_cc):
    button_status_cc = GPIO.input(8)
    button_status_c = GPIO.input(7)
    if button_status_c == 0:
        print("Clockwise button pressed. Moving counter clockwise.")
        GPIO.output(11, GPIO.HIGH) #R0,R00
        GPIO.output(13, GPIO.LOW) #R1
        GPIO.output(16, GPIO.HIGH) #R3
        GPIO.output(15, GPIO.LOW) #R2
        GPIO.output(18, GPIO.HIGH) #R4  
    elif button_status_cc == 0:
        print("Counter clockwise button pressed. Moving clockwise.")
        GPIO.output(15, GPIO.HIGH) #R2
        GPIO.output(18, GPIO.HIGH) #R4
        GPIO.output(11, GPIO.HIGH) #R0,R00
        GPIO.output(13, GPIO.HIGH) #R1
        GPIO.output(16, GPIO.HIGH) #R3
    elif button_status_c == 1 and button_status_cc == 1:
        print("Not moving.")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
GPIO.add_event_detect(8, GPIO.FALLING, callback = moving)    
GPIO.add_event_detect(7, GPIO.FALLING, callback = moving)
try:
    while True:
        pass
    
except KeyboardInterrupt:
    GPIO.output(15, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    GPIO.cleanup()

GPIO.cleanup()

#IR SENSOR - works
#GPIO.cleanup()
#
#def print_state(input):
#    input = GPIO.input(36)
#    
#    global notches
#
#    if input != 0:
#        print("solid")
#        notches = notches +1
#        print(notches)
#    else:
#        print("interfere")
#
#GPIO.add_event_detect(36, GPIO.BOTH, callback = print_state)
#
#while True:
#    pass


#WORKS SEPARATELY
#CC--sets 0,00,1,3 high (works)
#def counterclockwise():
#    try: 
#        while True:
#            button_status_cc = GPIO.input(8)
#            if button_status_cc == False:
#                print("Counter clockwise button pressed. Moving counter clockwise.")
#                GPIO.output(11, GPIO.HIGH) #R0,R00
#                GPIO.output(13, GPIO.HIGH) #R1
#                GPIO.output(16, GPIO.HIGH) #R3
#                GPIO.output(15, GPIO.LOW) #R2
#                GPIO.output(18, GPIO.LOW) #R4                                        
#            else:
#                print("Stopped moving counter clockwise.")

#    except KeyboardInterrupt:
#        GPIO.output(15, GPIO.LOW)
#        GPIO.output(18, GPIO.LOW)
#        GPIO.output(11, GPIO.LOW)
#        GPIO.output(13, GPIO.LOW)
#        GPIO.output(16, GPIO.LOW)
#        GPIO.cleanup()
#counterclockwise()

#WORKS SEPARATELY
#C--sets relay 2 and 4 high (works)
#def clockwise():
#    try: 
#        while True:
#           button_status_c = GPIO.input(7)
#           if button_status_c == False:
#               print("Clockwise button pressed. Moving clockwise.")
#               GPIO.output(15, GPIO.HIGH) #R2
#               GPIO.output(18, GPIO.HIGH) #R4
#               GPIO.output(11, GPIO.LOW) #R0,R00
#               GPIO.output(13, GPIO.LOW) #R1
#               GPIO.output(16, GPIO.LOW) #R3
#           else:
#               print("Stopped moving clockwise.")

#    except KeyboardInterrupt:
#        GPIO.output(15, GPIO.LOW)
#        GPIO.output(18, GPIO.LOW)
#        GPIO.output(11, GPIO.LOW)
#        GPIO.output(13, GPIO.LOW)
#        GPIO.output(16, GPIO.LOW)
#        GPIO.cleanup()
#clockwise()

#GPIO.cleanup()

#AT THE MOMENT, PUSH E STOP AND THEN RELAYS TO EXIT
#STOP button turns relays low when e_stop pressed 
#button_status_STOP = GPIO.input(22)
#button_status_c = GPIO.input(7)
#button_status_cc = GPIO.input(8)
#def loop(button_status_STOP,button_status_c,button_status_cc):
#    try:
#        button_status_STOP = GPIO.input(22)
#        if button_status_STOP == 1:
#            GPIO.output(15, GPIO.HIGH)
#            GPIO.output(18, GPIO.HIGH)
#            GPIO.output(13, GPIO.HIGH)
#            GPIO.output(16, GPIO.HIGH)
#        if button_status_STOP == 0:
#            GPIO.output(15, GPIO.LOW)
#            GPIO.output(18, GPIO.LOW)
#            GPIO.output(13, GPIO.LOW)
#            GPIO.output(16, GPIO.LOW)
#            GPIO.add_event_detect(22, GPIO.BOTH, callback = loop)
#        while True:
#            button_status_c = button_status_c = GPIO.input(7)
#            button_status_cc = button_status_cc = GPIO.input(8)
#            if button_status_c == False and button_status_cc == False:
#                print("Restart")
#                break

#    except KeyboardInterrupt:
#        GPIO.output(15, GPIO.LOW)
#        GPIO.output(18, GPIO.LOW)
#        GPIO.output(11, GPIO.LOW)
#        GPIO.output(13, GPIO.LOW)
#        GPIO.output(16, GPIO.LOW)
#        GPIO.cleanup()
#loop(button_status_STOP,button_status_c,button_status_cc)
#if __name__ == '__main__':
#    loop(button_status_STOP,button_status_c,button_status_cc)
#    GPIO.cleanup()
#    os.execv(sys.executable, ['python3'] + sys.argv)

#GPIO.cleanup()
