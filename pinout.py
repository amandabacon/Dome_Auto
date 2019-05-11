#!/usr/bin/python3

#--------------------------------------------------------
#Author(s): Amanda Bacon	    			-
#Automation of Stickney Observatory--pinout information -
#--------------------------------------------------------

#Relays (6 total) Require GND,VCC,CNTRL
#Two for hardware safety
GPIO_pin_relays = [8,10,12,16,18,22]

#LED buttons (4 total) Require GND,VCC (3.3 V)
#Backward--
#Forward--
#Home--
#E-Stop--
GPIO_pin_buttons = [11,13,15,19]

#IR Beam Break Sensor (2 total) Require GND,VCC,GPIO (signal)
#Object needs to block IR light (metal)
#Transmittor (black) has 2 wires (GND,VCC)
#Receiver (clear) has 3 wires (signal,GND,VCC)
#Need 10 K Ohm resistor
#One for position location
#One for home location
GPIO_pin_IR = [7,21]