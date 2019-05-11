#!/usr/bin/python3

#------------------------------------
#Author(s): Amanda Bacon	    -
#Automation of Stickney Observatory -
#------------------------------------

#import modules below
import time
from datetime import datetime
import RPi.GPIO as GPIO
import smbus

#set up mode for GPIO
GPIO.setmode(GPIO.BOARD)

#Azimuth information from 16" dome telescope
site_longitude = 73.2416 #west
site_latitude = 42.9207 #north

#radius of dome--diameter 10'6" or 126"
dome_radius = 1.6002 #meters, or 63"

#limit angles: 0 (north), 90 (east), 180 (south), 270 (west), 360 (north)
min_azimuth = 0
max_azimuth = 360

#set relay pins (6 relays--each need VCC,GRND,CNTRL)
pin_list = [8,10,12,16,18,22]

for i in pin_list:
	GPIO.setup(i, GPIO.OUT) #should this be IN?
	GPIO.output(i, GPIO.HIGH)
time.sleep(1)

try:
	GPIO.output(8, GPIO.LOW)
	time.sleep(1)
	GPIO.output(10, GPIO.LOW)
	time.sleep(1)
	GPIO.output(12, GPIO.LOW)
	time.sleep(1)
	GPIO.output(16, GPIO.LOW)
	time.sleep(1)
	GPIO.output(18, GPIO.LOW) #hardware safety relay
	time.sleep(1)
	GPIO.output(22, GPIO.LOW) #hardware safety relay
	time.sleep(1)
except KeyboardInterrupt:
	print('Quit')
	GPIO.cleanup()

while True:
	# Turn all relays ON
	GPIO.output(8, GPIO.HIGH)
	GPIO.output(10, GPIO.HIGH)
	GPIO.output(12, GPIO.HIGH)
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(18, GPIO.HIGH) #hardware safety relay
	GPIO.output(22, GPIO.HIGH) #hardware safety relay
	sleep(2) 
	# Turn all relays OFF
	GPIO.output(8, GPIO.LOW)
	GPIO.output(10, GPIO.LOW)
	GPIO.output(12, GPIO.LOW)
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW) #hardware safety relay
	GPIO.output(22, GPIO.LOW) #hardware safety relay
	sleep(2)

#reset GPIO settings
GPIO.cleanup()

#NOT TESTED
#toggle switch
#GPIO.setup(23, GPIO.IN)
#GPIO.setup(24, GPIO.IN)

#while True:
#	if GPIO.input(23) == 1:
#		print("Switch on the left")
#	if GPIO.input(24) == 1:
#		print("Switch on the right")
#	else:
#		print("Switch in center")
#	time.sleep(1)
#END OF NOT TESTED

#Need four of these: manual, automate, STOP, home: 11,13,15,19
#LED buttons--tested and work--need GRND and 3.3 V
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status = GPIO.input(11)
		if button_status == False:
			print("Pressed")
			time.sleep(0.2)
		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#LED buttons other option--tested and work--need GRND and 3.3 V
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try:
	while True:
		button_status = GPIO.input(11)
		if button_status == GPIO.HIGH:
			print("Not pressed")
		else:
			print("Pressed")
		
except:
	GPIO.cleanup()

#NOT TESTED
#IR beam break--object needs to block IR light--receiver with 3 wires,
#transmitter two wires--need 10K Ohm resistor, ground, and VCC
#GPIO.setup(7, GPIO.IN)
#	while True:
#		if(GPIO.input(7) == 1):
#			print("Beam inteference")
#		if(GPIO.input(7) == 0):
#			print("solid")

#logic for IR beam break---teeth
#try:
#	notches = 0
#	while notches < 361:
#		if(GPIO.input(21) == False):
#		#if(GPIO.input(21) == 1):
#			notches == notches + 1
#			print(notches)
#		else:
#			notches = notches
#
#except KeyboardInterrupt:
#	GPIO.cleanup()

#logic for IR beam break--home
#initial_positon = [0]
#final_position = [359]
#try:
#	if(initial_position != 0):
#		print("Not in home position. Going to home position")
#	else:
#		print("In home position")
#
#except:
#END OF NOT TESTED

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
