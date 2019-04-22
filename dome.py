#!/usr/bin/python3

#------------------------------------
#Author(s): Amanda Bacon			-
#Automation of Stickney Observatory -
#------------------------------------

import time
from datetime import datetime
import RPi.GPIO as GPIO

#set up mode for GPIO
GPIO.setmode(GPIO.board)

#Azimuth information from 16" dome telescope
site_longitude = 73.2416 #west
site_latitude = 42.9207 #north

#radius of dome
#dome_radius = 

#limit angles: 0 (north), 90 (east), 180 (south), 270 (west), 360 (north)
min_azimuth = 0
max_azimuth = 270

#get azimuth information from telescope


#set relay information
pin_list = [17,32]

for i in pin_list:
	GPIO.setup(i, GPIO.OUT)
#	GPIO.output(i, GPIO.HIGH)
time.sleep(2)

try:
	GPIO.output(17, GPIO.LOW)
	time.sleep(2)
	GPIO.output(32. GPIO.LOW)
	time.sleep(2)
	GPIO.cleanup()
except KeyboardInterrupt:
	print('Quit')

#while True:
	# Turn all relays ON
#	GPIO.output(17, GPIO.HIGH)
#	GPIO.output(32, GPIO.HIGH))
#	sleep(5) 
	# Turn all relays OFF
#	GPIO.output(17, GPIO.LOW)
#	GPIO.output(32, GPIO.LOW)
#	sleep(5)

#reset GPIO settings
GPIO.cleanup()
#==========================================================================
#For book keeping purposes
#Get time
dt = datetime.now()
print("Today's date:", dt)

#Get universal time
utc = datetime.utcnow()
print("UTC time:", utc)

#get how long program has been running
start_time = time.time()
program_execution = (time.time()-start_time)

#remind user about Ohio parking lot lights
try:
	count = 0
	while(count < 3):
		time.sleep(3600)
		count = count + 1
		print("Turn off Ohio parking lot lights!")
except KeyboardInterrupt:
	print('interrupted')
#==========================================================================

#main
#book keeping info.
print("program run time:", program_execution, "seconds")
print("program run time:", program_execution*(1/60.), "minutes")
print("program run time:", program_execution*(1/60.)*(1/60.), "hours")
