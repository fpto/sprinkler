
import os
import sys
import requests
import ConfigParser
import datetime
import time
from datetime import datetime
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
water_gpio = 26
sprinkler_gpio= 19
 
l1 = 14 # Led light #1
l2 = 18 #led light #2
leds_list = [water_gpio, l1,  l2, sprinkler_gpio]

# Watering time
watering_time = 60
sprinkler_time = 10

# Precipitation threshold is the maximum forecast of rain expected where watering would still happen.
max_preci = 20

for led in leds_list:
	GPIO.setup(led, GPIO.OUT)

GPIO.output(water_gpio, GPIO.HIGH)
GPIO.output(l2, GPIO.LOW)
GPIO.output(sprinkler_gpio, GPIO.HIGH)

def watering():
       print("Watering starting", str(datetime.now()))
       #print("Now sprinkling", str(datetime.now()))
       #GPIO.output(sprinkler_gpio, GPIO.LOW)
       #time.sleep(sprinkler_time)
       #GPIO.output(sprinkler_gpio, GPIO.HIGH)
       #time.sleep(0.25)
       print("Now watering balcony", str(datetime.now()))
       GPIO.output(water_gpio, GPIO.LOW)
       time.sleep(watering_time)
       GPIO.output(water_gpio, GPIO.HIGH)
       time.sleep(0.25)
       print("Watering finished", str(datetime.now()))
def standbyBlick(led):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.5)

def quickBlick(led):
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.25)

watering()

#schedule.every().minute.do(watering)

#TODO A log file would be great


# uncomment line below for testing lights

# while True:
#    schedule.run_pending()
#    standbyBlick(l1)

