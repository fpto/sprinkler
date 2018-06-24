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

# Method to access forecast
def get_precip_forecast(config):
  API_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{town}?apikey={key}/&details=true&metric=true'
  rf = requests.get(API_URL.format(key=config['api_key'],
                                  town=config['town']))
  rainfall_forecast = None
  if rf.ok:
    try:
      rainfall_forecast = float(r.json()['DailyForecasts'][0]['Day']['Rain']['Value'])
    except Exception as ex:
      rainfall_forecast = None
  return rainfall_forecast, rf


# Given the response of the WU API, puts hourly rainfall data into two
# lists - one containing time in seconds ago from now,
# and the other containing rainfall in inches/second
# def get_rainfall(r):
#     obs = r.json()['history']['observations']
#     dates = [obs[i]['date'] for i in range(len(obs))]
#     vals = [float(obs[i]['precipi']) for i in range(len(obs))]
#     vals = [val if val >= 0 else 0 for val in vals]
#     vals = [val / 3600.0 for val in vals]  # -> inches / second
#     dts = [datetime.datetime(year=int(dates[i]['year']),
#                              month=int(dates[i]['mon']),
#                              day=int(dates[i]['mday']),
#                              hour=int(dates[i]['hour']),
#                              minute=int(dates[i]['min'])) for i in range(len(dates))]
#     now = datetime.datetime.now()
#     t = [(dts[i] - now).total_seconds() for i in range(len(dates))]
#     return t, vals

# Integrates rainfall history using the trapezoid rule
# def integrate(t, vals):
#     total = 0.0
#     for i in range(len(vals) - 1):
#         r = 0.5 * (vals[i] + vals[i + 1]) * (t[i + 1] - t[i])
#         if r > 0: # sanity check in case of bad vals
#             total += r
#     return total

# Calls weather underground history api
# def get_wu_history(config, day):
#     API_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{town}?apikey={key}/&details=true&metric=true'
#     return requests.get(API_URL.format(key=config['api_key'],
#                                        day=day,
#                                        state=config['state'],
#                                        town=config['town']))
#
#     rainfall_forecast = None
#     if r.ok:
#       try:
#         rainfall = float(r.json()[0]['PrecipitationSummary']['Past24Hours']['Metric']['Value'])
#       except Exception as ex:
#         rainfall = None
#     return rainfall, r

# Gets recent rainfall using weather underground API
# By default estimates rainfall in past 24 hours
# to get something different use a different time_win
# (Note this doesn't go further back than yesterday)
def get_precip_in_window(config):
    get_precip_yesterday(config)
    get_precip_forecast(config)

        # Get observations for today and yesterday
    try:
        r_yesterday = rainfall
    except Exception as ex:
        return None

    try:
        r_today = rainfall_forecast
    except Exception as ex:
        return None

    try:
        total = r_yesterday + r_today

    except Exception as ex:
        raise ex
        total = 0.0
    return total

# Returns current time in format yyyy-mm-dd HH:MM:SS
def now():
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Runs sprinkler
def run_sprinkler(config):
  pin = int(config['gpio_starter'])
  led = int(config['gpio_led1'])
  runtime = float(config['runtime_min'])
  with open(config['log_file'],'a') as log_file:
    try:
      GPIO.setup((pin, led), GPIO.OUT)
      log_file.write('%s: Starting sprinkler\n' % now())
      GPIO.output((pin,led), GPIO.HIGH)
      sleep(runtime * 60)
      log_file.write('%s: Stopping sprinkler\n' % now())
      GPIO.output((pin,led), GPIO.LOW)
    except Exception as ex:
      log_file.write('%s: An error has occurred: %s \n' % (now(), ex.message))
      GPIO.output((pin,led), GPIO.LOW)

# Main method
#   1.  Reads config file
#   2.  Checks past 24 hours of rainfall
#   3.  Runs sprinkler if rainfall falls below threshold
def main():
  # Load configuration file
  config = load_config()

  with open(config['log_file'],'a') as log_file:
    # Get past 24 hour precip
    rainfall = get_precip_in_window(config)
    if rainfall is None:
      log_file.write('%s: Error getting rainfall amount, setting to 0.0 in\n' % current_time)
      rainfall = 0.0
    else:
      log_file.write('%s: Rainfall: %f in\n' % (now(), rainfall))

  # If this is less than RAIN_THRESHOLD_IN run sprinkler
  if rainfall <= float(config['rain_threshold_in']):
    run_sprinkler(config)

# Test API access
def test_api():
  config = load_config()
  rainfall, r = get_precip_today_in(config)
  if rainfall is None:
    print "Unable to access API"
    print "Request info: "
    print r.text
    return

  total = get_precip_in_window(load_config())
  if total is None:
    print "API works but unable to get history.  Did you sign up for the right plan?"
    return
  print "API seems to be working with past 24 hour rainfall=%f" % (total)

# Runs without checking rainfall
def force_run():
  config = load_config()
  run_sprinkler(config)

# Sets all GPIO pins to GPIO.LOW.  Should be run when the
# raspberry pi starts.
def init():
    config = load_config()
    pin = int(config['gpio_starter'])
    led = int(config['gpio_led1'])
    GPIO.setup((pin, led), GPIO.OUT)
    GPIO.output((pin,led), GPIO.LOW)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    # Standard mode
    main()
  elif len(sys.argv) == 2 and sys.argv[1] == 'test':
    # Tests connection to API
    # Make sure you run as root or this won't work
    test_api()
  elif len(sys.argv) == 2 and sys.argv[1] == 'force':
    # Runs sprinkler regardless of rainfall
    force_run()
  elif len(sys.argv) == 2 and sys.argv[1] == 'init':
    # Sets pin and led GPIOs to GPIO.LOW
    init()
  else:
    print "Unknown inputs", sys.argv
