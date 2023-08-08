"""
 reverse the specified log file lines and
 save into a temperary rlog.txt file
 so that the most recent data entries (up to 100)
 are displayed in reverse chronological order

 Modified 7/15/2023
 by Jin Zhu
"""

from os import path
import os

def reverselog(logfile_name):
    with open(logfile_name) as f1:
       with open('rlog.txt','w') as f2:
          first_line = f1.readline()  
          f2.write(first_line)
          #print(first_line)
       with open('rlog.txt','a') as f2:
          lines = f1.readlines()
          reversedlines=lines[::-1]
          if full==False :
          if len(reversedlines)>100:
              f2.writelines(reversedlines[0:99])
          else:
              f2.writelines(reversedlines)
