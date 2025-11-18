import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
fot = 6
state = 0
GPIO.setup(fot, GPIO.IN)
while True:
    GPIO.output(led, not (GPIO.input(fot)))