"""
 Check if the requested sensor data log is available.
 Return True (i.e. broken) if the folder/file does not exist.

 Revised 3/4/2024
 by Jin Zhu
"""

import os

def broken(sensor_id):
    return not os.path.isdir(sensor_id)

def brokenDate(date, sensor_id =""):
    if (sensor_id==""):   #if not sensor_id is provided, assume log files are stored directly under homepath
        return not os.path.isfile("log_"+date+".txt")
    elif os.path.isdir(sensor_id):  #otherwise check if the sensor_id directory exists
        return not os.path.isfile(sensor_id+"/"+sensor_id+"_log_"+date+".txt")
    else:
        return True
