#!/usr/bin/python3

#--------------------------------------------------------
#Author(s): Amanda Bacon	    			-
#Automation of Stickney Observatory--pinout information -
#--------------------------------------------------------

#Relays (6 total) Require GND,VCC,CNTRL
#Two for hardware safety--one GPIO pin together
GPIO_pin_relays = [11,13,15,16,18] #all GPIO-only pins
#R0,R00 pin 11
#R1 pin 13
#R2 pin 15
#R3 pin 16
#R4 pin 18

#LED buttons (4 total) Require GND,VCC (3.3 V)
#Backward(cc)--8
#Forward(c)--7
#Home--10
#E-Stop--22
GPIO_pin_buttons = [7,8,10,22] #7,8,10 are I2C and UART

#IR Beam Break Sensor (2 total) Require GND,VCC,GPIO (signal)
#Object needs to block IR light (metal)
#Transmittor (black) has 2 wires (GND,VCC)
#Receiver (clear) has 3 wires (signal,GND,VCC)
#Need 10 K Ohm resistor (only if not using pull_up_down)
#One for position location
#One for home location
GPIO_pin_IR = [36,37] #all GPIO only
