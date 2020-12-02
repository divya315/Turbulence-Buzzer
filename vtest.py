#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 38
led=8
var=""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setwarnings(False)

def active(led):
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.5)
def callback(channel):
    global var
    if GPIO.input(channel):
        print("Movement Detected!")
        var="Vibration Detected"
        active(led)



GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change


try:
    while True:
        time.sleep(0.5)
  
except KeyboardInterrupt:
        GPIO.cleanup()