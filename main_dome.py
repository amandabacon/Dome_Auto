#!/usr/bin/python3

#------------------------------------------------------------------------
#Author(s): Amanda Bacon, Anna McNiff, Emma Salazar, Josie Bunnell      -
#Automation of Stickney Observatory                                     -
#------------------------------------------------------------------------

import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus
import sys
import os

notches = 0

GPIO.cleanup()

#set warnings to false
GPIO.setwarnings(False)

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

#Buttons
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP) #counter clockwise
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) #e stop
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #clockwise

#IR
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP) #notch count
GPIO.setup(35, GPIO.IN, pull_up_down = GPIO.PUD_UP) #home sensor
#notches = 0

#Relays
GPIO.setup(11, GPIO.OUT) #R0,R00
GPIO.setup(13, GPIO.OUT) #R1
GPIO.setup(15, GPIO.OUT) #R2
GPIO.setup(16, GPIO.OUT) #R3
GPIO.setup(18, GPIO.OUT) #R4

#IR SENSOR
def print_state(input):
    input = GPIO.input(36)
    print("This is the input", input) #0 for interference, 1 for solid
    global notches
    if input != 0:
        print("Solid")
        notches = notches + 1
        print(notches)
    else:
        print("Beam interference")
GPIO.add_event_detect(36, GPIO.BOTH, callback = print_state)

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

#Motor functions
#clockwise movement
def go_clockwise():
    print("Moving clockwise.")
    GPIO.output(11, GPIO.HIGH) #R0,R00
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(16, GPIO.HIGH) #R3
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(18, GPIO.HIGH) #R4  

#counter clockwise movement
def go_counter_clockwise():
    print("Moving counter clockwise.")
    GPIO.output(15, GPIO.HIGH) #R2
    GPIO.output(18, GPIO.HIGH) #R4
    GPIO.output(11, GPIO.HIGH) #R0,R00
    GPIO.output(13, GPIO.HIGH) #R1
    GPIO.output(16, GPIO.HIGH) #R3

#stop the motor
def stop_motor():
    print("Stopping motor.")
    GPIO.output(11, GPIO.LOW) #R0,R00
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(16, GPIO.LOW) #R3
    GPIO.output(18, GPIO.LOW) #R4

#Home button
def go_home(button_status_home):
    button_status_home = GPIO.input(10)
    home_sensor = GPIO.input(35)
    if button_status_home == False:
        print ("Home button pressed. Going home.")
        if home_sensor != 0: 
            print ("Not at home position. Going home.")      
            go_clockwise()
        if home_sensor == 0:
            print ("At home position.")
            stop_motor()
GPIO.add_event_detect(10, GPIO.FALLING, callback = go_home)
    
#True = 1, False = 0
#Button clockwise and counter clockwise
def moving(button_status_cc):
    button_status_cc = GPIO.input(8)
    button_status_c = GPIO.input(7)
    if button_status_c == False:
        print("Clockwise button pressed. Moving clockwise.")
        GPIO.output(11, GPIO.HIGH) #R0,R00
        GPIO.output(13, GPIO.LOW) #R1
        GPIO.output(16, GPIO.HIGH) #R3
        GPIO.output(15, GPIO.LOW) #R2
        GPIO.output(18, GPIO.HIGH) #R4  
        print_state(input)
    elif button_status_cc == False:
        print("Counter clockwise button pressed. Moving counter clockwise.")
        GPIO.output(15, GPIO.HIGH) #R2
        GPIO.output(18, GPIO.HIGH) #R4
        GPIO.output(11, GPIO.HIGH) #R0,R00
        GPIO.output(13, GPIO.HIGH) #R1
        GPIO.output(16, GPIO.HIGH) #R3
        print_state(input)
    elif button_status_c == True and button_status_cc == True:
        print("Not moving.")
        GPIO.output(11, GPIO.LOW) #R0,R00
        GPIO.output(13, GPIO.LOW) #R1
        GPIO.output(15, GPIO.LOW) #R2
        GPIO.output(16, GPIO.LOW) #R3
        GPIO.output(18, GPIO.LOW) #R4
    if button_status_c == False and button_status_cc == False: #where False = pushing button
        print("Not allowed to press both buttons. Not moving.")
        GPIO.output(11, GPIO.LOW) #R0,R00
        GPIO.output(13, GPIO.LOW) #R1
        GPIO.output(15, GPIO.LOW) #R2
        GPIO.output(16, GPIO.LOW) #R3
        GPIO.output(18, GPIO.LOW) #R4
time.sleep(0.25)
GPIO.add_event_detect(8, GPIO.FALLING, callback = moving, boucetime = 100)    
GPIO.add_event_detect(7, GPIO.FALLING, callback = moving, bouncetime = 100)

try:
    while True:
        pass
    
except KeyboardInterrupt:
    GPIO.output(15, GPIO.LOW) #R2
    GPIO.output(18, GPIO.LOW) #R4
    GPIO.output(11, GPIO.LOW) #R0,R00
    GPIO.output(13, GPIO.LOW) #R1
    GPIO.output(16, GPIO.LOW) #R3
    GPIO.cleanup()

#NOT TESTED BELOW
            
#Azimuth location
def go_location(azimuth, notches):
    while notches < azimuth:
        go_clockwise()
        stop_motor()

def go_new_location(azimuth, notches):
    if(notches < azimuth):
        go_clockwise()
    elif(notches > azimuth):
        go_counterwise()
    else:
        stop_motor()





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
