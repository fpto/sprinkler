import os
import sys
import requests
import ConfigParser
import datetime
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

api_key = 'qhjhdK4aGlExSQVWA6jbsAhNntab7Wns'
# City code for Bagalore where it always rain: 188760
# City code for Tegucigalpa: 188046
city = 188760


HISTORY_API_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{town}/historical/24?apikey={key}&language=en-us&details=true'
yesterday_weather = requests.get(HISTORY_API_URL.format(town=city, key=api_key))
yesterday_rainfall = yesterday_weather.json()[0]['PrecipitationSummary']['Past24Hours']['Metric']['Value']
print('It rained {yesterday_rainfall} mm of water'.format(yesterday_rainfall=yesterday_rainfall))

FORECAST_API_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{town}?apikey={key}&details=true&metric=true'
todays_weather_forecast = requests.get(FORECAST_API_URL.format(town=city, key=api_key))
todays_rainfall_forecast = todays_weather_forecast.json()['DailyForecasts'][0]['Day']['Rain']['Value']
print('Forecast is {todays_rainfall_forecast} mm of rain'.format(todays_rainfall_forecast=todays_rainfall_forecast))

rainfall_48_hours = yesterday_rainfall + yesterday_rainfall
print('Between yesterday and today expect {rainfall_48_hours} mm of rain'.format(rainfall_48_hours=rainfall_48_hours))

#TODO A log file would be great

# Led light pin
l = 4
def ledBlick():
    	GPIO.output(l, GPIO.HIGH)
    	time.sleep(0.5)
    	GPIO.output(l, GPIO.LOW)
    	time.sleep(0.5)

while True:
    if todays_rainfall_forecast > 0
        ledBlick()
