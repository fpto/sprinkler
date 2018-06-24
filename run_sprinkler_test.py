import os
import sys
import requests
import ConfigParser
import datetime
from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Loads configuration file
def load_config(filename='config'):
  config = ConfigParser.RawConfigParser()
  this_dir = os.path.abspath(os.path.dirname(__file__))
  config.read(this_dir + '/' + filename)
  if config.has_section('SprinklerConfig'):
      return {name:val for (name, val) in config.items('SprinklerConfig')}
  else:
      print 'Unable to read file %s with section SprinklerConfig' % filename
      print 'Make sure a file named config lies in the directory %s' % this_dir
      raise Exception('Unable to find config file')

# Method to access accu weather current conditions API and return
# the value field.  Weather Underground API is not free anymore.
#
def get_precip_yesterday(config):
  API_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{town}/historical/24?apikey={key}&language=en-us&details=true'
  r = requests.get(API_URL.format(key=config['api_key'],
                                  town=config['town']))
  rainfall = None
  if r.ok:
    try:
      rainfall = float(r.json()[0]['PrecipitationSummary']['Past24Hours']['Metric']['Value'])
    except Exception as ex:
      rainfall = None
  return rainfall, r

get_precip_yesterday(config)
print(rainfall)
