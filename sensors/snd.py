'''
<<<<<<< HEAD
Reads sound sensor readings and sends them to a remote location to be stored
'''
import RPi.GPIO as GPIO
import time
from .transport import Transport

SENSOR_TYPE = 'SND'             # Sound sensor

SENSOR_CHECK_INTERVAL = 0.1     # Read the sensor every 0.1 seconds
READING_AGGREGATE_COUNT = 50    # Number of readings to collect before sending
REQUIRED_AGGREGATE_COUNT = 25   # Number of readings that need to have positive
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
             currentPositive += 1
       elif i==1:               # When output from motion sensor is HIGH
             GPIO.output(3, 1)  # Turn ON LED

       if currentCount>=READING_AGGREGATE_COUNT:
            if(currentPositive>=REQUIRED_AGGREGATE_COUNT):
                transport.send(SENSOR_TYPE, 1)
            else:
                transport.send(SENSOR_TYPE, 0)
            currentCount = 0;
            currentPositive = 0;

       time.sleep(SENSOR_CHECK_INTERVAL)


             
=======
Created on Dec 1, 2016

@author: tishu
'''
import urllib.parse
import urllib.request
import time

url = 'http://10.23.8.174:8080/stats'
values = {'DEVICE_ID' : 'kitchen_toster',
          'SENSOR_TYPE' : 'MOT',
          'SENSOR_READING' : '1',
          'TIMESTAMP' : str(round(time.time() * 1000)) }

data = urllib.parse.urlencode(values)
data = data.encode('ascii') # data should be bytes

print(values)

req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   
print(the_page)
>>>>>>> eff9ac4726e4d8026ad717e4069cd98c55e9fcb4
