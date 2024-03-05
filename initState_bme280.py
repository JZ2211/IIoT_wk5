# implementation of BME280/BME680 interfacing with Raspberry Pi
# data are saved in a file named after the date
# At the same time data is also pushed to Initial State
#
# Created on 08/20/2023
# by Jin Zhu
# 

#Initial State User Setting 
SENSOR = 'sensor5'                      #modify for your sensor node
BUCKET_NAME ='Python Stream Example'    #modify for your project
BUCKET_KEY = 'initial state bucket key'  #modify for your project
ACCESS_KEY = 'initial state access key'  #modify for your project
BUFFER_SIZE = 3
############# Don't change code below this line ####################

import time
from datetime import datetime
import re
import sys
import board
from adafruit_bme280 import basic as BME280
from savedata_locally import savedata_locally as document
from ISStreamer.Streamer import Streamer

#Create an Initial State streamer bucket
istreamer = Streamer(bucket_name = BUCKET_NAME, bucket_key= BUCKET_KEY, access_key = ACCESS_KEY, buffer_size = BUFFER_SIZE)

#BME280 setup
i2cbus = board.I2C() #use default raspberry pi board SCL and SDA for I2C
mybme280=BME280.Adafruit_BME280_I2C(i2cbus,0x77)  #the default I2C address is 0x77 for adafruit BME280 board.
#use BME280(i2cbus, 0x76) instead if the I2C address is 0x76 

datatype = "Date, Time, Temperature(C), Pressure(hPa), Humidity(%)"
try: 
     print("Start reading data from BME280......\n")
     print(datatype)
     while True:
      timestamp = str(datetime.now()) #obtain current time
     
      #BME280 results
      temperature = mybme280.temperature #obtain the ambient temprature in Celsius degree
      pressure = mybme280.pressure  #obtain the pressure in hPa
      humidity = mybme280.humidity  #obtain the relative humidity in percentage        

      timestamp = re.sub(' ',', ', timestamp)
      #timestamp = timestamp.split('.')[0] #omit subseconds time information
      output = timestamp + ", {0:.2f}, {1:.2f}, {2:.2f}".format(temperature, pressure, humidity)
      #timestamp=timestamp.split('.')[0]

      istreamer.log(SENSOR + " bme280 Temperature(C)", temperature)
      istreamer.log(SENSOR + " bme280 Pressure(hPa)", pressure)
      istreamer.log(SENSOR + " bme280 Humidity(%RF)", humidity)

      print(output)  #display results in the terminal
      document(output, datatype)  #save data into a local text file
      time.sleep(4.85) #data are collected roughly every 5 second

except KeyboardInterrupt:
      print("Interrupted by User")
      sys.exit(0)
