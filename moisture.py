# coding: utf-8
import RPi.GPIO as GPIO
import time
import smtplib
import schedule
import logging
import datetime
logging.basicConfig(filename='moisture_checks.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


# start talking to the SMTP server for Gmail
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.ehlo()
# now login as my gmail user
username='rpidefabricio@gmail.com'
password='frambuesita1!'
s.login(username,password)
# the email objects
replyto='rpidefabricio@gmail.com' # where a reply to will go
sendto=['fabricio.puerto@outlook.com'] # list to send to
sendtoShow='Master' # what shows on the email as send to
subject='No water detected on balcony' # subject line
content='Hello,\n \n the sensor has not detected water on the balcony.\nPlease check your watering system\n\nWith love, \nYour raspberry pi' # content 
# compose the email. probably should use the email python module
mailtext='From: '+replyto+'\nTo: '+sendtoShow+'\n'
mailtext=mailtext+'Subject:'+subject+'\n'+content

# send the email
def sendmail():
  s.sendmail(replyto, sendto, mailtext)
  # we’re done
  rslt=s.quit()
  # print the result
  logging.info('Email sent. Sendmail result=' + str(rslt[1]))


#GPIO Setup
sensor1 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1, GPIO.IN)

def moisture_check(sensor):
    if GPIO.input(sensor):
      logging.info("No water detected")
      sendmail()
    else:
      logging.info("Water detected")

def job():
  try:
    moisture_check(sensor1)

  except KeyboardInterrupt:
    logging.info(" Quit")
    GPIO.cleanup()

schedule.every().day.at('09:10').do(job)

while True:
    schedule.run_pending()

