'''
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