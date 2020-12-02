#!/usr/bin/python
import RPi.GPIO as GPIO
import time
 
#GPIO SETUP
channel2 = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
 
def callback2(channel2):
    print("flame detected")
 
GPIO.add_event_detect(channel2, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel2, callback2)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
        time.sleep(1)