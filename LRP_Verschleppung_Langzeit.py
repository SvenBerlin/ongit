# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 08:50:51 2021

@author: sbergmann
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:06:34 2021

@author: sbergmann
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob as glob
import os as os
import numpy as np
import matplotlib.dates as mdates
from matplotlib import rcParams
from datetime import datetime,timedelta
rcParams.update({'figure.autolayout': True})
#matplotlib.use('agg')

path = r'C:\Users\sbergmann\Desktop\Verschleppung\Langzeit_36mm'
path = os.path.abspath(path)

cuev = os.path.basename(path)
files = glob.glob(path+'\\*.csv')
columns = ['Timestamp',
           'LABEL',
           'TRIGGER',
           'STATUS',
           'ERROR',
           'MESS_V_NULL',
           'MESS_V_LED1',
           'MESS_V_LED2',
           'NULLWERT_LED1',
           'NULLWERT_LED2',
           'MESSWERT_LED1',
           'MESSWERT_LED2',
           'EXT_LED1',
           'EXT_LED2',
           'EXT_DIFF',
           ]

df = pd.DataFrame()
vlines = []
line = 0
data = {'Nullung':None, 'Messung': None}
for key in data.keys():
    f = files[[n for n,x in enumerate(files) if key in x][0]]
    temp = pd.read_csv(f,sep=';')
    temp.columns = [x.replace(' ','') for x in temp.columns]
    temp['Timestamp'] = pd.to_datetime(temp['Timestamp'])
    temp['LABEL'] = temp['LABEL'].apply(lambda x: x.replace(' ',''))
    temp.insert(2,'VAAxxx',[key]*len(temp))
    h = temp[(temp['LABEL']=='Messung') | (temp['LABEL']=='Nullung')]
    df = pd.concat([df,h],ignore_index=True)
    vlines.append(line)
    line += len(h)
    data[key] = [f,temp]

title = f'Verschleppungsanalyse {cuev} {str(data["Nullung"][1]["Timestamp"][0])}'

colors = ['firebrick','tab:olive',]#'tab:cyan',]

mydpi=96
fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
ax2 = ax1.twinx()
# lns1 = ax1.plot(df['EXT_LED1'], label='EXT_LED1',color='firebrick', alpha=0.5)
for n,key in enumerate(data.keys()):
    temp = df[df['VAAxxx']==key]
    # z = np.polyfit(temp["EXT_LED1"].index,temp["EXT_LED1"], 1)
    # p = np.poly1d(z)

    # lns4 = ax1.plot(temp["EXT_LED1"].index, p(temp["EXT_LED1"].index), 'lightblue',label='Trend')
    # ax1.text(temp["EXT_LED1"].index[-1],p(temp["EXT_LED1"].index[-1]), f'{p}')
    # num = int(len(temp)/10)
    # start = temp.index[0]
    # for n in range(num):
    # x = np.arange(0,len(temp),1)
    x = temp.Timestamp
    y = temp["EXT_LED1"]
    # ax1.scatter(x,y, color=colors[n],s=6, label=key) 
    ax1.scatter(x,y, color=colors[n],s=6, label=key) 
        # lns2 = ax1.plot(x,[y.median()]*10, linestyle='--', color='k', label='$\~x$')
        # # lns2 = ax1.plot(x,[y.mean()]*10, linestyle='--', color='k', label='$\overline{x}$')
        # up = [y.median()+3*np.std(y)]*10
        # down = [y.median()-3*np.std(y)]*10        
        # up = [y.mean()+3*np.std(y)]*10
        # down = [y.mean()-3*np.std(y)]*10        
        # lns3 = ax1.plot(x,up, linestyle='--', color='forestgreen', label='$3*\sigma$')
        # ax1.plot(x,down, linestyle='--', color='forestgreen')
        # locs, labels = plt.xticks() 
        # ax1.boxplot(y, positions=[x[4]+0.5],widths=10)
        # plt.xticks(locs)
        # ax1.text(start, up[0]*1.01, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=0,fontsize='small')
        # start += 10
    
# ax1.set_xticks(df.Timestamp-df.Timestamp[0])
# lns1 = ax1.plot(df['EXT_LED1'], label='EXT_LED1',color='mediumseagreen')
# lns2 = ax1.plot(df['EXT_LED2'], label='EXT_LED2',color='steelblue')
ymin,ymax = ax1.get_ylim()
# ax1.vlines(vlines,ymin=ymin,ymax=ymax,colors='red',linestyles='dotted',label='Test')
# for n in range(len(vlines)):
#     ax1.text(vlines[n]+0.1,(ymax+ymin)/2,list(data.keys())[n],rotation=90)
# lns3 = ax2.plot(df['HEATER_TEMP_ACTUAL'], label='HEATER_TEMP_ACTUAL',color='firebrick')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
dur = str(df["Timestamp"].iloc[-1]-df["Timestamp"].iloc[0]).split(' ')[-1]
textstr = f'Nullung und Messung mit VE Wasser\nMessungen im Abstand von 10s\nTestdauer: {dur}'
# textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\overline{x} \pm 3*\sigma$'
ax1.text(0.75, 0.9, textstr, transform=ax1.transAxes,
        verticalalignment='top', bbox=props)

ax1.set_xlabel('Messpunkt')
ax1.set_ylabel('Extinktion E')
# zeitliche Achse nicht verwendet
# ax2.set_ylabel('Temperatur °C')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
dt = timedelta(minutes=5)
ax1.set_xlim(df['Timestamp'][0]- dt,df['Timestamp'].iloc[-1]+ dt)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
# ax1.xaxis.set_tick_params(rotation=90)
# #    ax1.set_aspect('equal')
# #    ax1.locator_params(axis='y',tight=True,nbins=10)
# ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
# ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
#    ax2.locator_params(axis='y', nbins=10)
#    ax2.locator_params(axis='x', nbins=10)
ax1.set_title(title)
ax1.grid()
# lns = lns1#+lns2+lns3+lns4
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
ax1.legend()
fname = f'{title.replace(" ","_").replace(":","-")}.png'
fig.savefig(f'{path}\\{fname}')

    

