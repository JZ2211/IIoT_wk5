"""
 create plots for specified sensor data with a download link 
 Function: creat_plots(file_name,sid, html_file)
         where file_name is the text file that contains sensing data (fields are seperated by comma)
               sid is the sensor node ID or hostname for th Raspberry Pi
               html_file the html file that plots will be added
 
 Modified July 2023
 by Jin Zhu
"""

import plotly.graph_objects as go   #to install: pip3 install plotly
from plotly.subplots import make_subplots
import pandas as pd     #to install: pip3 install pandas
import math
import fileinput

def creat_plots(file_name,sid, html_file):

    df=pd.read_csv(file_name)
    cols =df.columns  #the first two columns are 'Date' and ' Time', and rest are sensor data and we will plot each column as a subplot

    n_rows = df.shape[0]
    n_cols = df.shape[1]
    empty =" "
    rows = math.ceil(((n_cols-2)/2))

    #get the correct headers
    subplot_titles=[]
    for col in range(2,n_cols):
        subplot_titles.append(cols[col])

    #get the correct number of rows
    specs = []
    for row in range(rows):
        specs.append([{"type": "scatter"},{"type": "scatter"}])

    #make figure
    fig = make_subplots(
        rows=math.ceil(((n_cols-2)/2)), cols=2,
        shared_xaxes=True,
        vertical_spacing = 0.1,
        subplot_titles=subplot_titles,
        specs = specs)

    for col in range(2,n_cols):
        fig.add_trace(go.Scatter(x=df[cols[1]],y=df[cols[col]],mode="lines",name=cols[col]),row=math.floor(col/2), col=math.ceil(col%2)+1)
        fig.update_yaxes(title_text=cols[col], row=math.floor(col/2), col=math.ceil(col%2)+1)

    fig.update_xaxes(title_text = cols[1], row=3)

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text = "Sensor Monitoring Data from: Sensor "+ str(sid) +" ||  Date: " + df[cols[0]][0] + " || Lastest update:" + df[cols[0]][n_rows-1] + "," + df[cols[1]][n_rows-1],

        )
    #please remember to write the html file to templates directory
    fig.write_html(html_file)

#add a download link into the html file
def add_download(link, name, html_file):
    filename = html_file
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as f:
        for line in f:
            if '<head><meta charset="utf-8" /></head>\n' == line:
                print('<head><meta charset="utf-8" /><style>.btn{background-color: DodgerBlue;color:white;cursor: pointer;font-size: 20px;}</style><a href="'+link+'" download="'+name+'"><button class="btn"> Download the File Here</button></a></head>',end='')
            else:
                print(line,end='')

