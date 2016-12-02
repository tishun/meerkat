
'''
Deals with storing the sensor readings on a remote location
'''
import urllib.parse
import urllib.request
import time

DEVICE_ID = 'fitness'           # Unique identifier of this device

class Transport:

     def send(self, sensor_type, sensor_reading):
        url = 'http://10.23.8.174:8080/stats'
        values = {'DEVICE_ID' : DEVICE_ID,
                  'SENSOR_TYPE' : sensor_type,
                  'SENSOR_READING' : sensor_reading,
                  'TIMESTAMP' : str(round(time.time() * 1000)) }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii') # data should be bytes

        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           the_page = response.read()
           
        print(the_page)
