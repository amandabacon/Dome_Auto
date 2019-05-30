# Final for Hardware Hacking Spring 2019

This program is geared towards being used by Stickney Observatory users as a means to automate the observatory dome. This repository contains logic for movement of the dome via buttons (clockwise and counter clockwise) that control six relays (two are safety relays), an emergency stop button that sets relays that control the motor to low and restarts the script, a home button that uses IR beam break sensors to count gear teeth notches and finds the home position based on interference from a spring on the dome.

This system works in conjunction with the already present motor switch, allowing for automated or manual mode. Soon, the user will be able to type in an azimuth and the dome will go to that azimuth.

# Installation

In order to use this script, you must first download/purchase all of the dependencies: Raspberry Pi, beefcake relays, IR beam break sensors, and LED buttons.

This model is run and tested on Mac and Linux OS.

# Hardware (see pinout.py for more information)
-SparkFun Beefcake Relay: https://www.sparkfun.com/products/13815

-IR Beam Break Sensors (3mm and 5mm): https://www.adafruit.com/product/2167

-LED Buttons: https://www.amazon.com/Ulincos-Momentary-Stainless-Suitable-Mounting/dp/B01N1F8OEQ/ref=sr_1_2?qid=1559047861&refinements=p_n_feature_seven_browse-bin%3A5485702011&s=industrial&sr=1-2

# Need To Do:
-Figure out issues with relay R2 (counter clockwise motion). For now it is commented out in the code.

-Error handling for IR sensors.

-Flask html page that asks for a user input (azimuth) and moves the dome to the point using the IR beam break sensor notch count.  

# How to Run Flask for Auto-Dome: (Note: this code is not working right now. Only the first page loads. Thank you and goodbye)
-In terminal, ssh'd into the pi, type:
```
    export FLASK_APP=auto_dome.py
```
then type: 
```
    flask run --host=0.0.0.0
```
then go to chrome and type in http://domecontrol.bennington.edu:5000/static/go-dome.html (if you are on Bennington Secure)

-or-

go to chrome and type in http://raspberrypi22.local:5000/static/go-dome.html (if you are not on Bennington Secure)

Sincerely, 

:rage: :dancer: :snail: :dog: 

:mortar_board:
