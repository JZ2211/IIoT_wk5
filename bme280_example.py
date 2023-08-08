"""
Implementation of BME280/BME680 interfacing with Raspberry Pi
data are saved in a log file named after the date 
when the data are collected

Jin Zhu created 5/18/2023
"""

import time
from datetime import datetime
import re
import sys
import board
from adafruit_bme280 import basic as BME280
from savedata import savedata_locally as document
##uncomment next link if upload the data to a remote server via paramiko
#from savedata import savedata_remotely as upload

#BME280 setup
i2cbus = board.I2C() #use default raspberry pi board SCL and SDA for I2C
mybme280=BME280.Adafruit_BME280_I2C(i2cbus,0x77)  #the default I2C address is 0x77 for adafruit BME280 board.
#use BME280(i2cbus, 0x76) instead if the I2C address is 0x76 


datatype = "Date, Time, Temperature(C), Pressure(hPa), Humidity(%)"
extra=[]
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
      output = timestamp + ", {0:.2f}, {1:.2f}, {2:.2f}".format(temperature, pressure, humidity)

      print(output)  #display results in the terminal
      document(output, datatype)  #save data into a local text file
      ##uncomment next line if you also need to upload the data to a remote server via paramiko
      #extra = upload(output, datatype, extra)
      time.sleep(29.85) #data are collected roughly every 30 second

except KeyboardInterrupt:
      print("Interrupted by User")
      sys.exit(0)
