import os
import sys
import requests
import ConfigParser
import datetime
import time
import schedule
import logging
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
logging.basicConfig(filename='history.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

api_key = 'maoUyv52tVfNoR4OoUZLCvyVgYcyP2ic'
# City code for Bagalore where it always rain: 188760
# City code for Tegucigalpa: 188046
city = 188046

# GPIO  pin
water_gpio = 26 # Led light #1
l2 = 18 #led light #2
leds_list = [water_gpio, l2]

# Watering time
watering_time = 60

# Precipitation threshold is the maximum forecast of rain expected where watering would still happen.
max_preci = 20

for led in leds_list:
	GPIO.setup(led, GPIO.OUT)

GPIO.output(water_gpio, GPIO.HIGH)
GPIO.output(l2, GPIO.LOW)

def watering():
    	GPIO.output(water_gpio, GPIO.LOW)
    	time.sleep(watering_time)
    	GPIO.output(water_gpio, GPIO.HIGH)
    	time.sleep(0.25)

def standbyBlick(led):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        time.sleep(2)

def quickBlick(led):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.25)

print("Watering starting")
watering()
print("Watering finished")
