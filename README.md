# Final for Hardware Hacking Spring 2019

This program is geared towards being used by Stickney Observatory users as a means to automate the observatory dome.

# Installation

In order to use this script, you must first download/purchase all of the dependencies: Raspberry Pi, beefcake relays, IR beam break sensors, and LED buttons.

This model is run and tested on Mac and Linux OS.

# Hardware (see pinout.py for more information)
-SparkFun Beefcake Relay: https://www.sparkfun.com/products/13815

-IR Beam Break Sensors (3mm and 5mm): https://www.adafruit.com/product/2167

-LED Buttons: https://www.amazon.com/Ulincos-Momentary-Stainless-Suitable-Mounting/dp/B01N1F8OEQ/ref=sr_1_2?qid=1559047861&refinements=p_n_feature_seven_browse-bin%3A5485702011&s=industrial&sr=1-2

# Need To Do:
-Figure out issues with R2 (counter clockwise motion). For now it is commented out in the code

-Error handling for IR sensors

# How to Run Flask for Auto-Dome:
-In terminal, ssh'd into the pi type:
```
    export FLASK_APP=auto_dome.py
```
then type: 
```
    flask run --host=0.0.0.0
```
then go to chrome and type in http://raspberrypi##.local:5000/static/go-dome.html

