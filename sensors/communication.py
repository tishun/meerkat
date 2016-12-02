
'''
Created on Dec 1, 2016

@author: tishu
'''
import urllib.parse
import urllib.request
import time
import logging


class Transport:

     def send(device_id, sensor_type, sensor_reading):
        url = 'http://10.23.8.174:8080/stats'
        values = {'DEVICE_ID' : device_id,
                  'SENSOR_TYPE' : sensor_type,
                  'SENSOR_READING' : sensor_reading,
                  'TIMESTAMP' : str(round(time.time() * 1000)) }

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii') # data should be bytes

        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
           if(logging.isDebugEnabled())
                logging.debug('Sending sensor data to ' + url);
                logging.debug('Readings : ' + data);
           the_page = response.read()
           
        logging.debug(the_page)
