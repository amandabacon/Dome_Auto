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
import sys

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

#set relay pins (6 relays--each need VCC,GND,CNTRL)
#2 safety relays connected to same GPIO pin via molex cable being twisted
pin_list = [13,15,16,18,22] #only need 5--all GPIO only pins

for i in pin_list:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)
time.sleep(1)

try:
	GPIO.output(13, GPIO.LOW)
	time.sleep(1)
	GPIO.output(15, GPIO.LOW)
	time.sleep(1)
	GPIO.output(16, GPIO.LOW)
	time.sleep(1)
	GPIO.output(18, GPIO.LOW)
	time.sleep(1)
	GPIO.output(22, GPIO.LOW) #hardware safety relay--should be same GPIO pin
	time.sleep(1)
except KeyboardInterrupt:
	print('Quit')
	GPIO.cleanup()

while True:
	# Turn all relays ON
	GPIO.output(13, GPIO.HIGH)
	GPIO.output(15, GPIO.HIGH)
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(18, GPIO.HIGH)
	GPIO.output(22, GPIO.HIGH) #hardware safety relay--should be same pin (A split)
	sleep(2) 
	# Turn all relays OFF
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(22, GPIO.LOW) #hardware safety relay--should be same pin (A split)
	sleep(2)

#reset GPIO settings
GPIO.cleanup()

#NOT TESTED
#toggle switch for home position--deprecated
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

#Need four of these: backward,forward,STOP,home: 11,7,8,10 (7,8,10 not solely GPIO)
#HOME button
#LED buttons--tested and work--need GND and 3.3 V
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status = GPIO.input(7)
		if button_status == False:
			print("Pressed")
			time.sleep(0.2)
		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#Counter clockwise button
#LED buttons--tested and work--need GND and 3.3 V
GPIO.setup(8, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status_cc = GPIO.input(8)
		if button_status_cc == False:
			print("Pressed")
			time.sleep(0.2)
		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#Clockwise button
#LED buttons--tested and work--need GND and 3.3 V
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status_c = GPIO.input(10)
		if button_status_c == False:
			print("Pressed")
			time.sleep(0.2)
		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#STOP button
#LED buttons--tested and work--need GND and 3.3 V
#GND is bottom horizontal pin, 3.3 V is horizontal pin above and off to side of it.
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status_STOP = GPIO.input(11)
		if button_status_STOP == True:
			print("Not Pressed")
			time.sleep(0.2)
		if button_status_STOP == False:
			print("Emergency Stop!")
			sys.exit()

except:
	GPIO.cleanup()	

#STOP logic #3
try:
	button_status_STOP = GPIO.input(11)
	button_status = GPIO.input(7)
	button_status_c = GPIO.input(10)
	button_status_cc = GPIO.input(8)
	if button_status_STOP == False:
		print("E-STOP! Relays set to low!")
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
		print("To restart, press home, cc, and c buttons simultaneously")

	if button_status == False and button_status_cc == False and button_status_c == False:
		print("Restart initiated")

except KeyboardInterrupt:
	GPIO.cleanup()

#LED buttons other option--tested and work--need GND and 3.3 V
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

#IR beam break--object needs to block IR light--receiver with 3 wires,
#transmitter two wires--need 10K Ohm resistor (if not using pull_up_down),GND,VCC
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	while True:
		if(GPIO.input(36) == 0):
			print("Beam inteference")
		if(GPIO.input(36) == 1):
			print("solid")

#IR beam break number 2
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	while True:
		if(GPIO.input(37) == 0):
			print("Beam interference #2")
		if(GPIO.input(37) == 1):
			print("solid #2")

notches = ??
#NOT TESTED
# conversion = [notches]/360 #notches/degrees
# def get_azimuth(indigo_data) #converts indigo data to a notch number 
#	azimuth = indigo_data*conversion
#	return azimuth

#def go_clockwise() #sets relays in state B
# 	GPIO.input(15, GPIO.HIGH) #was 12
# 	GPIO.input(18, GPIO.HIGH) #was 18
# 	GPIO.input(22, GPIO.LOW) #was 8
# 	GPIO.input(13, GPIO.LOW) #was 10
# 	GPIO.input(16, GPIO.LOW) #was 16
#
# def go_counterwise() #sets relays in state A
#	GPIO.input(22, GPIO.HIGH) #was 8
# 	GPIO.input(13, GPIO.HIGH) #was 10
# 	GPIO.input(16, GPIO.HIGH) #was 16
# 	GPIO.input(15, GPIO.LOW) #was 12
# 	GPIO.input(18, GPIO.LOW) #was 18
#
#def stop_motor() #sets all Relays to low
#	GPIO.input(22, GPIO.LOW) #was 8
# 	GPIO.input(13, GPIO.LOW) #was 10
# 	GPIO.input(16, GPIO.LOW) #was 16
# 	GPIO.input(15, GPIO.LOW) #was 12
# 	GPIO.input(18, GPIO.LOW) #was 18
#
# #other option function a la go motor 
# def go_location(azimuth)	
# 	go_clockwise() #goes clockwise until notches = azimuth notch data 
#	notches = 0 
#	while notches < azimuth 
#		if(GPIO.input(37) == 0):
#			notches == notches +1 
#			print(notches)
#		else: 
#			notches = notches 
# 	stop_motor()
#	return notches
#
# def go_new_location(azimuth, notches)
#	if(notches<azimuth): 
#		go_clockwise() #goes clockwise until notches = azimuth notch data
#		while notches < azimuth 
#			if(GPIO.input(37) == 0):
#				notches == notches +1 
#				print(notches)
#			else: 
#				notches = notches 
# 		stop_motor()
#	if(notches>azimuth): 
#		go_counterwise() #goes counterwise until notches = azimuth notch data (backwards) 
#		while notches > azimuth 
#			if(GPIO.input(37) == 0):
#				notches == notches -1 
#				print(notches)
#			else: 
#				notches = notches 
# 		stop_motor()

#except KeyboardInterrupt:
#	GPIO.cleanup()

#WHAT IS THIS?
#logic for IR beam break--home
#initial_positon = [0]
#final_position = [359]
#try:
#	if(initial_position != 1):
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