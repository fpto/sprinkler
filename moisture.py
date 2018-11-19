import RPi.GPIO as GPIO
import time

#GPIO Setup
channel1 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel1, GPIO.IN)

def callback(channel1):
    if GPIO.input(channel1):
        print("No water detected")
    else:
        print("Water detected")

#GPIO.add_event_detect(channel1, GPIO.BOTH, bouncetime=300) # Let us know when pin goes high or low
#GPIO.add_event_callback(channel1, callback) # assign function to GPIO pin, run function on change

#infite loop
#while True:
#      time.sleep(1)



callback(channel1)
