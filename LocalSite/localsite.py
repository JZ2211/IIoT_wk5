# Use Flask to implement a WSGI server
# to display numerica values obtained in the sensor
#
# Modified 7/15/2023
# by Jin Zhu

from datetime import datetime
import re
import sys
import os
import subprocess
from subprocess import PIPE
import broken
from reverselog import reverselog
from flask import Flask, render_template, send_file
##comment next line if plotly and pandas are not installed
from create_plots import creat_plots, add_download

#Assume IIoT_Case1 is installed under the HOMEPATH and data are store under HOMEPATH/sensor_id.
#If it is not, please modify the HOMEPATH accordingly
HOMEPATH='/home/pi/'

#template file for plots
html_file = HOMEPATH+'IIoT_Case1/LocalSite/templates/plots_logfile.html'

app = Flask(__name__)

@app.route('/')
def check():
    return render_template("start.html")

#numberics display for today's data (up to 100 most recent entries)
@app.route("/<string:sensor_id>/")
def numbers(sensor_id):
    #print(sensor_id)
    date = str(datetime.now().date())
    date = re.sub('-','_', date)
    if broken.broken(sensor_id):
        return render_template("brokenID.html")
    else:
        if broken.brokenDate(sensor_id, date):
            return render_template("broken.html")
        else:
            name = sensor_id +"_log_"+date+".txt"
            description = "Sensor: "+ sensor_id
            pathname = HOMEPATH + sensor_id +'/'
            filename = sensor_id + "_log_" + date + ".txt"
            reverselog(pathname+filename)
            with open("rlog.txt", "r") as f:
                content = f.read()
            return render_template("default.html", content=content, name = name, description=description)
        

#numberic display for a given date (all entries in chronological order)
@app.route("/<string:sensor_id>/<string:dates>/")
def past_numbers(sensor_id,dates):
    if broken.brokenDate(sensor_id,dates):
        return render_template("broken.html")
    else:
        name = sensor_id +"_log_"+dates+".txt"
        description = "Sensor: "+ sensor_id
        pathname = HOMEPATH + sensor_id +'/'
        filename = sensor_id + "_log_" + dates + ".txt"
        reverselog(pathname+filename)
        with open(pathname+filename, "r") as f:
            content = f.read()
        return render_template("default.html", content=content, name = name, description=description )

### blocks for plots start
### If plotly and pandas are not installed, comment them out 
#this is today's graphs
@app.route('/<string:sensor_id>/plots/')
def plots(sensor_id):
    date = str(datetime.now().date())
    date = re.sub('-','_', date)
    if broken.broken(sensor_id):
        return render_template("brokenID.html")
    else:
        if broken.brokenDate(sensor_id, date):
            return render_template("broken.html")
        else:
            pathname = HOMEPATH + sensor_id+'/'
            filename = sensor_id +'_log_' + date + '.txt'
            plots = creat_plots(pathname+filename,sensor_id,html_file)
            link = "/download/" + sensor_id + "/" + date  #e.g. /download/sensor2/2021_11_19
            name = sensor_id +"_" + date + ".csv"
            add_download(link, name, html_file)
            return render_template('plots_logfile.html')

#this is past graphs
@app.route("/<string:sensor_id>/plots/<string:dates>/")
def past_plots(sensor_id, dates):
    if  broken.brokenDate(sensor_id, dates):
        return render_template("broken.html")
    else:
        pathname = HOMEPATH + sensor_id+'/'
        filename= sensor_id + "_log_"+dates + ".txt"
        plots = creat_plots(pathname+filename, sensor_id, html_file)
        link="/download/"+ sensor_id + "/" + dates
        name= sensor_id + "_" + dates + ".csv"
        add_download(link, name, html_file)
        return render_template('plots_logfile.html')

#this is the download link
@app.route("/download/<string:sensor_id>/<string:dates>/")
def download(sensor_id,dates):
    filename = sensor_id + '_log_' + dates + '.txt'
    return send_file(HOMEPATH + sensor_id + '/' + filename) #, as_attachment=True)
### blocks for plots end


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True ) #disable the debug mode using: debug = False 

