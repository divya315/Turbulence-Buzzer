#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel2 = 40
led=8
variab=""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel2, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)


def active(led):
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.5)
def callback(channel2):
    global variab
    if GPIO.input(channel2):
        print("Obstacle Detected!")
        variab="Obstacle infront Detected"
        active(led)



GPIO.add_event_detect(channel2, GPIO.RISING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel2, callback)  # assign function to GPIO PIN, Run function on change


try:
    while True:
        time.sleep(0.5)
  
except KeyboardInterrupt:
        GPIO.cleanup()