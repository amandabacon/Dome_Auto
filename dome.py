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
max_azimuth = 494

#set relay pins (6 relays--each need VCC,GND,CNTRL)
#2 safety relays connected to same GPIO pin via molex cable being twisted
pin_list = [11,13,15,16,18] #only need 5--all GPIO only pins

for i in pin_list:
	GPIO.setup(i, GPIO.OUT)

#reset GPIO settings
#GPIO.cleanup()

#Need four of these: counter clockwise,clockwise,STOP,home: 11,7,8,10 (7,8,10 not solely GPIO)
#HOME button
#LED buttons--tested and work--need GND and 3.3 V
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status_home = GPIO.input(10)
		if button_status_home == False:
			print("Pressed")
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
#			GPIO.input(11, GPIO.HIGH) #R0,R00
# 			GPIO.input(13, GPIO.HIGH) #R1
# 			GPIO.input(16, GPIO.HIGH) #R3
# 			GPIO.input(15, GPIO.LOW) #R2
# 			GPIO.input(18, GPIO.LOW) #R4

		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#Clockwise button
#LED buttons--tested and work--need GND and 3.3 V
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
try: 
	while True:
		button_status_c = GPIO.input(7)
		if button_status_c == False:
			print("Pressed")
#			GPIO.input(15, GPIO.HIGH) #R2
# 			GPIO.input(18, GPIO.HIGH) #R4
# 			GPIO.input(11, GPIO.LOW) #R0,R00
# 			GPIO.input(13, GPIO.LOW) #R1
# 			GPIO.input(16, GPIO.LOW) #R3
		else:
			print("Not pressed")

except:
	GPIO.cleanup()

#STOP button--Logic: exit program completely
#LED buttons--tested and work--need GND and 3.3 V
#GND is bottom horizontal pin, 3.3 V is horizontal pin above and off to side of it.
#GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
#try: 
#	while True:
#		button_status_STOP = GPIO.input(22)
#		if button_status_STOP == True:
#			print("Not Pressed")
#		if button_status_STOP == False:
#			print("Emergency Stop!")
#			sys.exit()

#except:
#	GPIO.cleanup()	

#STOP button--Logic #2: Edge case
#try:
#	GPIO.wait_for_edge(22, GPIO.FALLING) #signal starts to fall towards 0. Counters initial high state.
#except KeyboardInterrupt:
#	GPIO.cleanup()
	
#LED buttons other option--tested and work--need GND and 3.3 V
#GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP) #initial high state
#try:
#	while True:
#		button_status = GPIO.input(22)
#		if button_status == GPIO.HIGH:
#			print("Not pressed")
#		else:
#			print("Pressed")
		
#except:
#	GPIO.cleanup()

#IR beam break--object needs to block IR light--receiver with 3 wires,
#transmitter two wires--need 10K Ohm resistor (if not using pull_up_down),GND,VCC
GPIO.setup(36, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	while True:
		if(GPIO.input(36) == 0):
			print("Beam inteference")
		if(GPIO.input(36) == 1):
			print("solid")

#IR beam break for home test
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	while True:
		if(GPIO.input(37) == 0):
			print("Beam interference #2")
		if(GPIO.input(37) == 1):
			print("solid #2")
			
#this is an attempt at introducing an event to indicate rising/falling transition
#Tested--only acknowledges when there is interference (rise). Seems to count once per interference, which is good.
# option 1
# def my_callback(channel):
#	if GPIO.input(37) == 0:
#		print("Falling edge")
#	if GPIO.input(37) != 0:
#		print("Rising edge")
#	notch_ir = GPIO.input(37)
#	return notch_ir
# then in clockwise and counterwise we have if notch_ir = 1 notches == notches + 1 
# but I dont see how this is different from what we have now? this just seems the same? 
# GPIO.add_event_detect(37, GPIO.BOTH, callback = my_callback)

#Tested--does the same as the above code. Does not acknowledge solid at all.
# option 2
# def my_callback(channel):
#	if GPIO.input(37) == 0:
#		print("Falling edge")
#		notch_ir = 0
#		return notch_ir
#	if GPIO.input(37) != 0:
#		print("Rising edge")
#		notch_ir = 1
#		return notch_ir
# GPIO.add_event_detect(37, GPIO.BOTH, callback = my_callback)

#Not tested
# option 3 
# GPIO.wait_for_edge(37, GPIO.RISING)
# notches == notches + 1
# in a loop? i dont know what the loop would be 

#Not tested
# option 4
# comparison between notch_ir and notch_ir from timestep before

#NOT TESTED
# conversion = max_azimuth/360 #notches/degrees
# def get_azimuth(indigo_data) #converts indigo data to a notch number 
#	azimuth = indigo_data*conversion
#	return azimuth

#def go_clockwise() #sets relays in state B
# 	GPIO.input(15, GPIO.HIGH) #R2
# 	GPIO.input(18, GPIO.HIGH) #R4
# 	GPIO.input(11, GPIO.LOW) #R0,R00
# 	GPIO.input(13, GPIO.LOW) #R1
# 	GPIO.input(16, GPIO.LOW) #R3
#
# def go_counterwise() #sets relays in state A
#	GPIO.input(11, GPIO.HIGH) #R0,R00
# 	GPIO.input(13, GPIO.HIGH) #R1
# 	GPIO.input(16, GPIO.HIGH) #R3
# 	GPIO.input(15, GPIO.LOW) #R2
# 	GPIO.input(18, GPIO.LOW) #R4
#
#def stop_motor() #sets all Relays to low
#	GPIO.input(11, GPIO.LOW) #R0,R00
# 	GPIO.input(13, GPIO.LOW) #R1
# 	GPIO.input(16, GPIO.LOW) #R3
# 	GPIO.input(15, GPIO.LOW) #R2
# 	GPIO.input(18, GPIO.LOW) #R4
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

#logic for IR beam break home position
#initial_positon = [0]
#final_position = [494]
#try:
#	if(initial_position != 494):
#		print("Not in home position. Going to home position")
#	else:
#		print("In home position")
#
#except:
#END OF NOT TESTED

#Raised exception when trying to slew to an invalid azimuth angle
class InvalidPositionException():
	#takes this from telescope keypad
	#string? int? Telescope pad: “Outside Safe Zone, Slewing canceled...”
	print("Error: invalid azimuth angle.")

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

	#dome only move when asked
	def stall(self):
	
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
