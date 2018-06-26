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

def job():
	try:
		HISTORY_API_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{town}/historical/24?apikey={key}&language=en-us&details=true'
   		yesterday_weather = requests.get(HISTORY_API_URL.format(town=city, key=api_key))
   		yesterday_rainfall = yesterday_weather.json()[0]['PrecipitationSummary']['Past24Hours']['Metric']['Value']
   		logging.info('It rained {yesterday_rainfall} mm of water'.format(yesterday_rainfall=yesterday_rainfall))

		FORECAST_API_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{town}?apikey={key}&details=true&metric=true'
		todays_weather_forecast = requests.get(FORECAST_API_URL.format(town=city, key=api_key))
		todays_rainfall_forecast = todays_weather_forecast.json()['DailyForecasts'][0]['Day']['Rain']['Value']
    		logging.info('Forecast is {todays_rainfall_forecast} mm of rain'.format(todays_rainfall_forecast=todays_rainfall_forecast))

   	 	rainfall_48_hours = yesterday_rainfall + yesterday_rainfall
   	 	logging.info('Between yesterday and today expect {rainfall_48_hours} mm of rain'.format(rainfall_48_hours=rainfall_48_hours))

   	 	if rainfall_48_hours <= max_preci:
       			print("Watering starting.")
			watering()
			logging.info("Watering finished.")
			print("Watering finished")
   	 	else:
			logging.info("We are not watering this time. We will get more than {threshold} mm water.".format(threshold=max_preci))
	except KeyboardInterrupt:
        	logging.info(" Quit")
        	GPIO.cleanup()


schedule.every(2).days.at('06:30').do(job)

#TODO A log file would be great


# uncomment line below for testing lights

while True:
    schedule.run_pending()
    standbyBlick(l2)
