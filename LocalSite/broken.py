"""
 Check if the requested sensor data log is available.
 Return True (i.e. broken) if the folder/file does not exist.

 Modified 7/15/2023
 by Jin Zhu
"""

import os

def broken(sensor_id):
    return not os.path.isdir(sensor_id)

def brokenDate(sensor_id,date):
    if os.path.isdir(sensor_id):
        return not os.path.isfile(sensor_id+"/"+sensor_id+"_log_"+date+".txt")
    else:
        return True
