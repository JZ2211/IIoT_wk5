#Store sensor data into a local file named after the date: log_yyyy_mm_dd.txt
#Jin Zhu created 5/18/2023

from os import path
import re

def savedata_locally(output, datatype): #output = timestamp and all the data, datatype = field title headings
    logdate = output.split(',')[0]  #obtain the date information for the log file name
    filename = 'log_' + re.sub('-','_', logdate)+ '.txt' #log file will be named as log_yyyy_mm_dd.txt
    """Write to this Rpi locally"""
    if path.exists(filename): #is the file already here?
        #If yes, append the new data to the date log file
        timelog = open(filename, 'a', buffering=1)
        timelog.write(output + "\n")
        timelog.close()     
    else:
        #if not, creat the new file and write the field tilte headings into the date log file first
        timelog = open(filename, 'w', buffering=1)
        timelog.write(datatype + "\n")
        timelog.write(output + "\n")
        timelog.close()
    return
    


