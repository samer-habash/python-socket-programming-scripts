#!/usr/bin/python3
import datetime, sys, time, os, glob
from bokeh.plotting import figure, output_file, show, save
from bokeh.layouts import row
import pandas as pd
from bokeh.models import DatetimeTickFormatter, ColumnDataSource


class style():
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)

if not os.path.exists('templates'):
    os.makedirs('templates')

timestr = time.strftime("%Y%m%d-%H:%M:%S")
output_HTML = 'plot_'+timestr+'.'+'html'

#Import data-->Weight measurements over a period of time [ STUB ]
df = pd.read_csv(sys.argv[1], low_memory=False)
#Define parameters
df["LogTime"] = pd.to_datetime(df["LogTime"])
#df.set_index("LogTime", inplace=True)

df["diff"] = df['column1'] - df['column2']
Max = df["diff"].max()
Min =df["diff"].min()
Average = df["diff"].mean()
count = df["diff"].count()

# making figures from plots bokeh x-y axis
p = figure(title="Figure1", width=800, height=450, background_fill_color='#efefef')
p.xaxis.axis_label = 'Date' "  " + str(datetime.datetime.now().date()) + "    " + \
                     'Max delta is : ' + str(Max) + "    " + 'Min delta is : ' + str(Min) + "    " + \
                     'Average is : ' + str(Average) + "    " 'Message Count : ' + str(count)

p.yaxis.axis_label = 'Tags column1-column2 in Micro Time Frame'
p.xaxis.formatter = DatetimeTickFormatter(hourmin=['%H:%M'], seconds=['%Ss'], microseconds=['%fus'])
p.line(x=df["LogTime"], y=df["diff"], line_width=2)


#Plot 2 column1-column3
df["diff2"] = df['column1'] - df['column3']
Max2 = df["diff2"].max()
Min2 =df["diff2"].min()
Average2 = df["diff2"].mean()
count2 = df["diff2"].count()

p2 = figure(title="Figure2", width=800, height=450, background_fill_color='#efefef')
p2.xaxis.axis_label = 'Date' "  " + str(datetime.datetime.now().date()) + "    " + \
                     'Max delta is : ' + str(Max2) + "    " + 'Min delta is : ' + str(Min2) + "    " + \
                     'Average is : ' + str(Average2) + "    " 'Message Count : ' + str(count2)

p2.yaxis.axis_label = 'Tags column1-column3 in Micro Time Frame'
p2.xaxis.formatter = DatetimeTickFormatter(hourmin=['%H:%M'], seconds=['%Ss'], microseconds=['%fus'])
p2.line(x=df["LogTime"], y=df["diff2"], line_width=2)


#Plot 3 column2-column3
df["diff3"] = df['column2'] - df['column3']
Max3 = df["diff3"].max()
Min3 =df["diff3"].min()
Average3 = df["diff3"].mean()
count3 = df["diff3"].count()

p3 = figure(title="Figure3", width=800, height=450, background_fill_color='#efefef')
p3.xaxis.axis_label = 'Date' "  " + str(datetime.datetime.now().date()) + "    " + \
                     'Max delta is : ' + str(Max3) + "    " + 'Min delta is : ' + str(Min3) + "    " + \
                     'Average is : ' + str(Average3) + "    " 'Message Count : ' + str(count3)

p3.yaxis.axis_label = 'Tags 52-122 in Micro Time Frame'
p3.xaxis.formatter = DatetimeTickFormatter(hourmin=['%H:%M'], seconds=['%Ss'], microseconds=['%fus'])
p3.line(x=df["LogTime"], y=df["diff3"], line_width=2)


output_file(output_HTML, title="Substraction chart")
show(row(p,p2,p3))

print("\n"+"Please download "+output_HTML+" and open it in your local machine"+"\n")

