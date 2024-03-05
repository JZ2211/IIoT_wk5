"""
 Use Flask to implement a WSGI server
 to display numerica values obtained in the sensor.
 Data are updated every 5 seconds
 Allow the user to download the data as a file under the name log_yyyy_mm_dd.csv

 revised 7/15/2023  
 revised 3/4/2024
 by Jin Zhu
"""

from datetime import datetime
import re
import sys
import os
import subprocess
from subprocess import PIPE
import broken
from reverselog import reverselog
from flask import Flask, render_template, send_file

#Assume IIoT_wk5 is cloned under the HOMEPATH and data are store under HOMEPATH.
#If it is not, please modify the HOMEPATH accordingly
HOMEPATH='/home/pi/'

#template for the html file
html_file = HOMEPATH+'IIoT_wk5/LocalSite/templates/index.html'

app = Flask(__name__)

def add_download(link, name, html_file):
    filename = html_file
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as f:
        for line in f:
            if '<meta charset="utf-8" />' in line:
                print('<meta charset="utf-8" /><style>.btn{background-color: DodgerBlue;color:white;cursor: pointer;font-size: 20px;}</style><a href="'+link+'" download="'+name+'"><button class="btn"> Download the CSV File Here</button></a>',end='\n')
            else:
                print(line,end='')

#numberics display for today's data
#up to 100 most recent entries in reverse chronological order
@app.route('/')
def check():
    date = str(datetime.now().date())
    date = re.sub('-','_', date)
    filename = "log_"+date+".txt"
    pathname = HOMEPATH  #assume the log files are stored under homepath
    reverselog(pathname+filename)
    with open("rlog.txt", "r") as f:
       content = f.read()
    return render_template("update.html", content=content, name = filename)

#numberic display for a given date (all entries in chronological order)
@app.route("/<string:date>/")
def past_numbers(date):
    date = re.sub('-','_', date)
    if broken.brokenDate(date):
        return render_template("broken.html")
    else:
        filename = "log_" + date + ".txt"
        link = "/download/" + date
        name = "log_" + date + ".csv"
        add_download(link, name, html_file)
        with open(HOMEPATH+filename, "r") as f:
            content = f.read()
        return render_template("index.html", content=content, name = filename)

#this is for the download link
@app.route("/download/<string:sensor_id>/<string:dates>/")
def download(sensor_id,dates):
    filename = sensor_id + '_log_' + dates + '.txt'
    return send_file(HOMEPATH + sensor_id + '/' + filename) 
### blocks for plots end


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True ) #To disable the debug mode using: debug = False 

