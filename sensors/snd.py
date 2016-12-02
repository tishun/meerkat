'''
<<<<<<< HEAD
Reads sound sensor readings and sends them to a remote location to be stored
'''
import RPi.GPIO as GPIO
import time
from .transport import Transport

SENSOR_TYPE = 'SND'             # Sound sensor

SENSOR_CHECK_INTERVAL = 0.1     # Read the sensor every 0.1 seconds
READING_AGGREGATE_COUNT = 30    # Number of readings to collect before sending
REQUIRED_AGGREGATE_COUNT = 2    # Number of readings that need to have positive
                                # reading for the entire sample to be considered
                                # positive
currentCount = 0
currentPositive = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN)          # Take input from sound detector
GPIO.setup(3, GPIO.OUT)         # Output readings to this pin (LED)

transport = Transport()

while True:
       currentCount += 1
       i=GPIO.input(5)
       if i==0:                 # When output from motion sensor is LOW
             GPIO.output(3, 0)  # Turn OFF LED
       elif i==1:               # When output from motion sensor is HIGH
             GPIO.output(3, 1)  # Turn ON LED
             currentPositive += 1

       if currentCount>=READING_AGGREGATE_COUNT:
            if(currentPositive>=REQUIRED_AGGREGATE_COUNT):
                transport.send(SENSOR_TYPE, 1)
            else:
                transport.send(SENSOR_TYPE, 0)
            currentCount = 0;
            currentPositive = 0;

       time.sleep(SENSOR_CHECK_INTERVAL)
