#!/usr/bin/python3

#------------------------------------------------------------------------
#Author(s): Amanda Bacon, Emma Salazar, Anna McNiff, Josie Bunnell      -
#Automation of Stickney Observatory pinout information                  -
#------------------------------------------------------------------------

#Relays (6 total) require GND,VCC,CNTRL
#Two for hardware safety--one GPIO pin together
GPIO_pin_relays = [11,13,15,16,18] #all GPIO-only pins
#R0,R00 pin 11 (safety relays)
#R1: pin 13
#R2: pin 15
#R3: pin 16
#R4: pin 18

#LED buttons (4 total) require GND,VCC (3.3 V)
#counter clockwise: pin 8
#clockwise: pin 7
#home: pin 10
#e-stop: pin 22
GPIO_pin_buttons = [7,8,10,22] #7,8,10 are I2C and UART

#IR Beam Break Sensor (2 total) require GND,VCC,GPIO (signal)
#Object needs to block IR light (metal)
#Transmittor (black) has 2 wires (GND,VCC)
#Receiver (clear) has 3 wires (signal,GND,VCC)
#Need 10 K Ohm resistor (only if not using pull_up_down)
#One for position location: pin 36
#One for home location: pin 35
GPIO_pin_IR = [36,35] #all GPIO only
