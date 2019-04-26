#!/usr/bin/python3

#------------------------------------
#Author(s): Amanda Bacon	    -
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
	GPIO.output(i, GPIO.HIGH)
time.sleep(2)

try:
	GPIO.output(17, GPIO.LOW)
	time.sleep(2)
	GPIO.output(32, GPIO.LOW)
	time.sleep(2)
	GPIO.cleanup()
except KeyboardInterrupt:
	print('Quit')

while True:
	# Turn all relays ON
	GPIO.output(17, GPIO.HIGH)
	GPIO.output(32, GPIO.HIGH))
	sleep(5) 
	# Turn all relays OFF
	GPIO.output(17, GPIO.LOW)
	GPIO.output(32, GPIO.LOW)
	sleep(5)

#reset GPIO settings
GPIO.cleanup()

#pseudo-code of dome operation

Mode = enum("Stand","Track")

#Raised exception when trying to slew to an invalid azimuth angle
class InvalidPositionException():
	#takes this from telescope keypad
	#string? int? Telescope pad: “Outside Safe Zone, Slewing canceled...”
	print("Error: invalid azimuth angle.")

class InvalidHorizonException():
	#takes from telescope
	#“Object Below Horizon Limit. Altitude:[Value]”.
	print("Object Below Horizon Limit. Altitude: ", value)

#Initial start-up position of dome
class Dome():
	#park position coordinates
	#timeouts

	#Query if the dome is currently slewing
	def isSlewing(self):
		#return True if the dome is slewing, False otherwise.
		#above is a boolean

	#get the dome's current position
	def currentPosition(self, position):
		#return coordinates in degrees, lon/lat

#synchronization with the 16" telescope
class DomeTelescope(Dome):
	#sync dome with telescope
	def beginSync(self):

	#dome-telescope synchronization complete		
	def completeSync(self):
	
	#synchronized tracking with telescope	
	def track(self):
	
	#check dome is tracking
	def isTracking(self):
		#returns True if dome is tracking, False otherwise
		#above is a boolean

	#dome only move when asked
	def stall(self):
	
	#If dome is tracking with telescope, sync dome position with scope position
	def TelescopePos(self):
	
	#get status of dome
	def domeStatus(self):
		#return if dome is Stall or tracking or in dome mode

	#get azimuth (Az)
	def getAz(self):
		#return dome's current azimuth in decimal degrees

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
