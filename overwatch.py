# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 11:12:36 2021

@author: sbergmann
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob as glob
import os as os
import time as time
import numpy as np
from datetime import datetime, timedelta

def update_line(ax, new_data):
    # ax.set_xdata(np.append(ax.get_xdata(), new_data[0]))
    # ax.set_ydata(np.append(ax.get_ydata(), new_data[1]))
    ax.set_xdata(new_data[0])
    ax.set_ydata(new_data[1])
    plt.draw()
    plt.show()

path = r'C:\Users\sbergmann\Desktop\LRP'
datei = r'C:\Users\sbergmann\Desktop\LRP\Verschleppung_36mm_MessungB_VE_20210625.csv'

if not datei:
    
    conditionZero = glob.glob(path+'\\*csv')
    
    while glob.glob(path+'\\*csv') == conditionZero:
        time.sleep(5)
        print('warte auf neue Datei...')
    
    newFiles = glob.glob(path+'\\*csv')
    for f in newFiles:
        if f not in conditionZero:
            datei = f
            break

    print(f'neue Datei gefunden: {datei}')    

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
plt.ion()
plt.show()

# 
dt = timedelta(minutes=2)
while True:
    
    # fdate = os.stat(datei)[8]
    # time.sleep(10)
    # if fdate == os.stat(datei)[8]:
    #     break
    # else:
    #     df = pd.read_csv(datei,sep=';')
    #     df.columns = [x.replace(' ','') for x in df.columns]
    #     df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    #     df['LABEL'] = df['LABEL'].apply(lambda x: x.replace(' ',''))
        

    #     plt.ion()
    #     plt.scatter(df[df['LABEL']=='Messung'].index,df[df['LABEL']=='Messung']['EXT_LED1'] )

    #     fig.canvas.draw()
    #     fig.canvas.flush_events()
        
    
    df = pd.read_csv(datei,sep=';')
    df.columns = [x.replace(' ','') for x in df.columns]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['LABEL'] = df['LABEL'].apply(lambda x: x.replace(' ',''))
    
    xcol = 'Timestamp'
    ycol = 'EXT_LED1'
    x = pd.to_datetime(df[df['LABEL']=='Messung'][xcol])
    y = df[df['LABEL']=='Messung'][ycol]
    plt.scatter(x,y,color='b',s=4 )
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)
    
    ax.set_xlim(x.iloc[0]-dt, x.iloc[-1]+dt)
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))

    fig.canvas.draw()
    fig.canvas.flush_events()
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(5)
    # plt.pause(5)