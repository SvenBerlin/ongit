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
from datetime import datetime, timedelta
rcParams.update({'figure.autolayout': True})
import matplotlib
from scipy import stats
# matplotlib.use('agg')

path = r'C:\Users\sbergmann\Desktop\Verschleppung\25mm_v1_ohneSpuelen'
path = os.path.abspath(path)

loops = 10
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
data = {'Warmup':None,'Nullung':None, 'MessungA': None, 'MessungProbe': None, 'MessungB': None}
for key in data.keys():
    try:
        f = files[[n for n,x in enumerate(files) if key in x][0]]
        temp = pd.read_csv(f,sep=';')
        temp.columns = [x.replace(' ','') for x in temp.columns]
        temp['Timestamp'] = pd.to_datetime(temp['Timestamp'])
        temp['LABEL'] = temp['LABEL'].apply(lambda x: x.replace(' ',''))
        temp.insert(2,'VAAxxx',[key]*len(temp))
        h = temp[(temp['LABEL']=='Messung') | (temp['LABEL']=='Nullung') | (temp['LABEL']=='Warmup')]
        if key !="Warmup":
            df = pd.concat([df,h],ignore_index=True)
            line += len(h)
        vlines.append(line)
        data[key] = [f,temp]
    except IndexError:
        pass

title = f'Verschleppungsanalyse {cuev} {str(data["Nullung"][1]["Timestamp"][0])}'

colors = ['tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan',
          'tab:orange','tab:green','tab:red','tab:blue','tab:purple',]

mydpi=96
fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
# ax2 = ax1.twinx()
lns1 = ax1.plot(df[df['VAAxxx']!="Warmup"]['EXT_LED1'], label='EXT_LED1',color='firebrick')
for key in list(data.keys())[1:]:
    temp = df[df['VAAxxx']==key]
    try:
        z = np.polyfit(temp["EXT_LED1"].index,temp["EXT_LED1"], 1)
        p = np.poly1d(z)
    # temp = temp[(temp['LABEL']=='Messung') | (temp['LABEL']=='Nullung')]
        lns4 = ax1.plot(temp["EXT_LED1"].index, p(temp["EXT_LED1"].index), 'lightblue',label='Trend')
        ax1.text(temp["EXT_LED1"].index[-1],p(temp["EXT_LED1"].index[-1]), f'{p}')
    except:
        pass
    num = int(len(temp)/10)
    start = temp.index[0]
    for n in range(num):
        x = np.arange(start,start+10,1)
        # x = temp["Timestamp"].loc[start:start+9]
        y = temp["EXT_LED1"].loc[start:start+9]
        ax1.scatter(x,y, color=colors[n]) 
        lns2 = ax1.plot(x,[y.median()]*10, linestyle='--', color='k', label='$\~x$')
        # lns2 = ax1.plot(x,[y.mean()]*10, linestyle='--', color='k', label='$\overline{x}$')
        up = [y.median()+3*np.std(y)]*10
        down = [y.median()-3*np.std(y)]*10        
        # up = [y.mean()+3*np.std(y)]*10
        # down = [y.mean()-3*np.std(y)]*10        
        lns3 = ax1.plot(x,up, linestyle='--', color='forestgreen', label='$3*\sigma$')
        ax1.plot(x,down, linestyle='--', color='forestgreen')
        # locs, labels = plt.xticks() 
        # ax1.boxplot(y, positions=[x[4]+0.5],widths=10)
        # plt.xticks(locs)
        if key != "MessungProbe":
            ax1.text(start, up[0]*1.01, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
        else:
            ax1.text(start, down[0]*0.79, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
        start += 10
# lns1 = ax1.plot(df['EXT_LED1'], label='EXT_LED1',color='mediumseagreen')
# lns2 = ax1.plot(df['EXT_LED2'], label='EXT_LED2',color='steelblue')
ymin,ymax = ax1.get_ylim()
ymax = 0.7
# ax1.set_ylim(ymin, 0.7)   
ax1.vlines(vlines,ymin=ymin,ymax=ymax,colors='red',linestyles='dotted',label='Test')
for n in range(len(vlines)):
    ax1.text(vlines[n]+0.1,(ymax+ymin)/2,list(data.keys())[n],rotation=90)
# lns3 = ax2.plot(df['HEATER_TEMP_ACTUAL'], label='HEATER_TEMP_ACTUAL',color='firebrick')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\~x \pm 3*\sigma$'
# textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\overline{x} \pm 3*\sigma$'
ax1.text(0.7, 0.8, textstr, transform=ax1.transAxes, fontsize='small',
        verticalalignment='top', bbox=props)

# ax1.set_xlim(data['Nullung'][1]['Timestamp'].iloc[0]- dt,data['MessungB'][1]['Timestamp'].iloc[-1]+ dt)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

ax1.set_xlabel('Messpunkt')
ax1.set_ylabel('Extinktion E')
# zeitliche Achse nicht verwendet
# ax2.set_ylabel('Temperatur °C')

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
lns = lns1+lns2+lns3+lns4
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)
plt.tight_layout()
fname = f'{title.replace(" ","_").replace(":","-")}.png'
fig.savefig(f'{path}\\{fname}')

if data['Warmup']:
    dt = timedelta(minutes=1)
    fig2,ax2 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
    temp = data['Warmup'][1]
    x = temp.Timestamp
    y = temp["EXT_LED1"]
    ax2.scatter(x,y,s=6)
    ax2.grid()
    ax2.set_xlabel('Zeit')
    ax2.set_ylabel('Extinktion E')
    ax2.set_xlim(temp['Timestamp'][0]- dt,temp['Timestamp'].iloc[-1]+ dt)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    title = f'WARMUP {title}'
    ax2.set_title(title)
    fname = f'{title.replace(" ","_").replace(":","-")}.png'
    fig2.savefig(f'{path}\\{fname}')

    


### relativ mean

def remOutl(y):
    return y[abs(stats.zscore(y))<=1]

title = f'Verschleppungsanalyse relativ {cuev} {str(data["Nullung"][1]["Timestamp"][0])}'

mydpi=96
fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
ax1.set_yscale('log')

for key in list(data.keys())[1:]:
    temp = df[df['VAAxxx']==key]
    
    num = int(len(temp)/10)
    start = temp.index[0]
    for n in range(num):
        x = np.arange(start,start+10,1)
        y = temp["EXT_LED1"].loc[start:start+9]
        
        if (key == "MessungB") & (n==0):
            y0 = ve0
        elif n==0:
            y0 = remOutl(y).mean()
            # y0mean = y.mean()
            # y0 = y.mean()
        if (key == "MessungA") & (n==0):
            ve0 = y0
        ymean = abs((remOutl(y).mean()-y0)/y0)*100
        ymean = abs(ymean)
        posY = y>0
        y = abs((y-y0)/y0)*100
        df.loc[y.index,'relativ'] = y
        df.loc[y.index,'relativMean'] = ymean
     
        # ax1.scatter(x[~posY],y[~posY], facecolors='none', edgecolors=colors[n]) 
        # ax1.scatter(x,[y]*len(x), facecolors=colors[n], edgecolors='none') 
        ax1.scatter(x[posY],y[posY], facecolors=colors[n], edgecolors='none') 
        ax1.scatter(x[~posY],y[~posY], facecolors='none', edgecolors=colors[n]) 
        ax1.plot(x,[ymean]*len(x), color=colors[n],linewidth=2) 
        ax1.plot(x,[ymean]*len(x), color='k',linewidth=0.5) 

        ax1.text(start+4, ymean*0.1, f'{round(remOutl(y).mean(),2)}+/-{round(3*remOutl(y).std(),2)}',rotation=90,fontsize='small')        
        start += 10
    if key != 'Nullung':
        block = remOutl(df.loc[temp.index,'relativ'])
        df.loc[temp.index,'relativBlock'] = block.mean()
        ax1.text(start-50, round(block.mean())*3, f'{round(block.mean(),2)}+/-{round(3*block.std(),2)}',fontsize='medium',color='red')        
ymin,ymax = ax1.get_ylim()
ymax = 0.7
# ax1.set_ylim(ymin, 0.7)   
ax1.vlines(vlines,ymin=ymin,ymax=ymax,colors='red',linestyles='dotted',label='Test')
for n in range(len(vlines)):
    ax1.text(vlines[n]+0.1,(ymax+ymin)/2,list(data.keys())[n],rotation=90)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = '''Nullung mit VE Wasser
MessungA und B mit VE Wasser
MessungProbe mit ausreagierter Probe undefinierter Extiontion

Dargestellt sind die relativen Abweichungen zum jeweiligen Bezugswert, 
wobei unsausgefüllte Marker negative Abweichungen darstellen.
VE-Messwerte beziehen sich auf den Mittelwert des ersten 10er 
Blocks nach der Nullung. Proben-Messwerte beziehen sich auf den 
Mittelwert des ersten 10er Blocks dieser Reihe.
(Ausreißer wurden zur Mittelwertbetrachtung durch eine 
zscore Bewertung entfernt: z<=1)

$\~x \pm 3*\sigma$'''
ax1.text(0.7, 0.25, textstr, transform=ax1.transAxes, fontsize='small',
        verticalalignment='top', bbox=props)

ax1.set_xlabel('Messpunkt')
ax1.set_ylabel('relative Abweichung vom Bezugswert (%)')

ax1.set_title(title)
ax1.grid()
# lns = lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
fig.canvas.draw()
plt.tight_layout()
fname = f'{title.replace(" ","_").replace(":","-")}.png'
fig.savefig(f'{path}\\{fname}')





### statistics

#warmup 0:4
#MessungA 5:104     1   2   3   4   5   6   7   8   9   10
#Probe 105:204      105 115 125 135 145 155 165 175 185 195 
#MessungB 205:304

# vaa = 'MessungB'
block = list(range(5,105))
# block = list(range(215,155))+list(range(165,175))+list(range(185,205))

data_cleaned = remOutl(df.loc[block,'relativ'])
print(f'''Mittelwert: {round(data_cleaned.mean(),3)} 
Median: {round(data_cleaned.median(),3)}
3s: {round(data_cleaned.std()*3,3)}''')





### relativ first

# title = f'Verschleppungsanalyse relativ {cuev} {str(data["Nullung"][1]["Timestamp"][0])}'

# mydpi=96
# fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
# ax1.set_yscale('log')

# for n,key in enumerate(list(data.keys())[1:]):
#     temp = df[df['VAAxxx']==key]
#     # try:
#     #     z = np.polyfit(temp["EXT_LED1"].index,temp["EXT_LED1"], 1)
#     #     p = np.poly1d(z)
#     # # temp = temp[(temp['LABEL']=='Messung') | (temp['LABEL']=='Nullung')]
#     #     lns4 = ax1.plot(temp["EXT_LED1"].index, p(temp["EXT_LED1"].index), 'lightblue',label='Trend')
#     #     ax1.text(temp["EXT_LED1"].index[-1],p(temp["EXT_LED1"].index[-1]), f'{p}')
#     # except:
#     #     pass
#     # num = int(len(temp)/10)
#     start = temp.index[0]
    
#     x = np.arange(start,start+len(temp),1)
#     # x = temp["Timestamp"].loc[start:start+9]
#     y = temp["EXT_LED1"]
#     if (key == "MessungB"):
#         y0 = ve0
#     else:
#         y0 = y.iloc[0]
#     if key == "MessungA":
#         ve0 = y0
#     y = ((y-y0)/y0)*100
#     # y = y/y0
#     posY = y>0
#     y = abs(y)
#     df.loc[y.index,'relativ'] = y
#     # y = y/y.iloc[0]
#     if key != "MessungB":
#         ax1.scatter(x[0],y.iloc[0], marker='X',s=60, color=colors[n], edgecolor='k') 
#         # ax1.scatter(x[1:],y.iloc[1:], color=colors[n]) 
#         ax1.scatter(x[1:][posY[1:]],y.iloc[1:][posY[1:]], facecolors=colors[n], edgecolors='none') 
#         ax1.scatter(x[1:][~posY[1:]],y.iloc[1:][~posY[1:]], facecolors='none', edgecolors=colors[n]) 
#     else:
#         ax1.scatter(x[posY],y[posY], facecolors=colors[n], edgecolors='none') 
#         ax1.scatter(x[~posY],y[~posY], facecolors='none', edgecolors=colors[n]) 
        
#     # lns2 = ax1.plot(x,[y.median()]*len(temp), linestyle='--', color='k', label='$\~x$')
#     # # lns2 = ax1.plot(x,[y.mean()]*10, linestyle='--', color='k', label='$\overline{x}$')
#     # up = [y.median()+3*np.std(y)]*len(temp)
#     # down = [y.median()-3*np.std(y)]*len(temp)    
#     # up = [y.mean()+3*np.std(y)]*10
#     # down = [y.mean()-3*np.std(y)]*10        
#     # lns3 = ax1.plot(x,up, linestyle='--', color='forestgreen', label='$3*\sigma$')
#     # ax1.plot(x,down, linestyle='--', color='forestgreen')
#     # locs, labels = plt.xticks() 
#     # ax1.boxplot(y, positions=[x[4]+0.5],widths=10)
#     # plt.xticks(locs)
#     # if key != "MessungProbe":
#     #     ax1.text(start, up[0]*1.01, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
#     # else:
#     #     ax1.text(start, down[0]*0.79, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
#     start += len(temp)
# # lns1 = ax1.plot(df['EXT_LED1'], label='EXT_LED1',color='mediumseagreen')
# # lns2 = ax1.plot(df['EXT_LED2'], label='EXT_LED2',color='steelblue')
# ymin,ymax = ax1.get_ylim()
# ymax = 0.7
# # ax1.set_ylim(ymin, 0.7)   
# ax1.vlines(vlines,ymin=ymin,ymax=ymax,colors='red',linestyles='dotted',label='Test')
# for n in range(len(vlines)):
#     ax1.text(vlines[n]+0.1,(ymax+ymin)/2,list(data.keys())[n],rotation=90)
# # lns3 = ax2.plot(df['HEATER_TEMP_ACTUAL'], label='HEATER_TEMP_ACTUAL',color='firebrick')

# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# textstr = '''Nullung mit VE Wasser
# MessungA und B mit VE Wasser
# MessungProbe mit ausreagierter Probe undefinierter Extiontion

# Dargestellt sind die relativen Abweichungen zum jeweiligen Bezugswert, 
# wobei unsausgefüllte Marker negative Messwerte darstellen.
# VE-Messwerte beziehen sich auf den allerersten VE-Messwert nach der Nullung. 
# Proben-Messwerte beziehen sich auf den allerersten 1. Messwert dieser Reihe.
# (s. als Kreuz markierte Messwerte)

# $\~x \pm 3*\sigma$'''
# # textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\overline{x} \pm 3*\sigma$'
# ax1.text(0.7, 0.2, textstr, transform=ax1.transAxes, fontsize='small',
#         verticalalignment='top', bbox=props)

# # ax1.set_xlim(data['Nullung'][1]['Timestamp'].iloc[0]- dt,data['MessungB'][1]['Timestamp'].iloc[-1]+ dt)
# # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
# ax1.set_xlabel('Messpunkt')
# ax1.set_ylabel('relative Abweichung vom Bezugswert (%)')
# # zeitliche Achse nicht verwendet
# # ax2.set_ylabel('Temperatur °C')

# # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
# # ax1.xaxis.set_tick_params(rotation=90)
# # #    ax1.set_aspect('equal')
# # #    ax1.locator_params(axis='y',tight=True,nbins=10)
# # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
# # ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
# #    ax2.locator_params(axis='y', nbins=10)
# #    ax2.locator_params(axis='x', nbins=10)
# ax1.set_title(title)
# ax1.grid()
# lns = lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
# plt.tight_layout()
# fname = f'{title.replace(" ","_").replace(":","-")}.png'
# fig.savefig(f'{path}\\{fname}')





# ### statistics

# #warmup 0:4
# #MessungA 5:104     1   2   3   4   5   6   7   8   9   10
# #Probe 105:204      105 115 125 135 145 155 165 175 185 195 
# #MessungB 205:304

# # vaa = 'MessungB'
# block = list(range(255,305))
# # block = list(range(215,155))+list(range(165,175))+list(range(185,205))

# print(f'''Mittelwert: {round(df.loc[block,'relativ'].mean(),3)} 
# Median: {round(df.loc[block,'relativ'].median(),3)}
# 3s: {round(df.loc[block,'relativ'].std()*3,3)}''')





# title = f'Verschleppungsanalyse relativ {cuev} {str(data["Nullung"][1]["Timestamp"][0])}'

# mydpi=96
# fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)

# for key in list(data.keys())[1:]:
#     temp = df[df['VAAxxx']==key]
#     # try:
#     #     z = np.polyfit(temp["EXT_LED1"].index,temp["EXT_LED1"], 1)
#     #     p = np.poly1d(z)
#     # # temp = temp[(temp['LABEL']=='Messung') | (temp['LABEL']=='Nullung')]
#     #     lns4 = ax1.plot(temp["EXT_LED1"].index, p(temp["EXT_LED1"].index), 'lightblue',label='Trend')
#     #     ax1.text(temp["EXT_LED1"].index[-1],p(temp["EXT_LED1"].index[-1]), f'{p}')
#     # except:
#     #     pass
#     num = int(len(temp)/10)
#     start = temp.index[0]
#     for n in range(num):
#         x = np.arange(start,start+10,1)
#         # x = temp["Timestamp"].loc[start:start+9]
#         y = temp["EXT_LED1"].loc[start:start+9]
#         y = y.iloc[0]/y
#         ax1.scatter(x[0],y.iloc[0], marker='X',s=60, color=colors[n], edgecolor='k') 
#         ax1.scatter(x[1:],y.iloc[1:], color=colors[n]) 
#         lns2 = ax1.plot(x,[y.median()]*10, linestyle='--', color='k', label='$\~x$')
#         # lns2 = ax1.plot(x,[y.mean()]*10, linestyle='--', color='k', label='$\overline{x}$')
#         up = [y.median()+3*np.std(y)]*10
#         down = [y.median()-3*np.std(y)]*10        
#         # up = [y.mean()+3*np.std(y)]*10
#         # down = [y.mean()-3*np.std(y)]*10        
#         lns3 = ax1.plot(x,up, linestyle='--', color='forestgreen', label='$3*\sigma$')
#         ax1.plot(x,down, linestyle='--', color='forestgreen')
#         # locs, labels = plt.xticks() 
#         # ax1.boxplot(y, positions=[x[4]+0.5],widths=10)
#         # plt.xticks(locs)
#         if key != "MessungProbe":
#             ax1.text(start, up[0]*1.01, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
#         else:
#             ax1.text(start, down[0]*0.79, f'{round(y.mean(),4)}+/-{round(3*np.std(y),4)}',rotation=90,fontsize='small')
#         start += 10
# # lns1 = ax1.plot(df['EXT_LED1'], label='EXT_LED1',color='mediumseagreen')
# # lns2 = ax1.plot(df['EXT_LED2'], label='EXT_LED2',color='steelblue')
# ymin,ymax = ax1.get_ylim()
# ymax = 0.7
# # ax1.set_ylim(ymin, 0.7)   
# ax1.vlines(vlines,ymin=ymin,ymax=ymax,colors='red',linestyles='dotted',label='Test')
# for n in range(len(vlines)):
#     ax1.text(vlines[n]+0.1,(ymax+ymin)/2,list(data.keys())[n],rotation=90)
# # lns3 = ax2.plot(df['HEATER_TEMP_ACTUAL'], label='HEATER_TEMP_ACTUAL',color='firebrick')

# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\~x \pm 3*\sigma$'
# # textstr = 'Nullung mit VE Wasser\nMessungA und B mit VE Wasser\nMessungProbe mit ausreagierter Probe undefinierter Extiontion\n\n$\overline{x} \pm 3*\sigma$'
# ax1.text(0.7, 0.8, textstr, transform=ax1.transAxes, fontsize='small',
#         verticalalignment='top', bbox=props)

# # ax1.set_xlim(data['Nullung'][1]['Timestamp'].iloc[0]- dt,data['MessungB'][1]['Timestamp'].iloc[-1]+ dt)
# # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

# ax1.set_xlabel('Messpunkt')
# ax1.set_ylabel('relative Abweichung vom ersten Messwert (Kreuz) des Blocks (%)')
# # zeitliche Achse nicht verwendet
# # ax2.set_ylabel('Temperatur °C')

# # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
# # ax1.xaxis.set_tick_params(rotation=90)
# # #    ax1.set_aspect('equal')
# # #    ax1.locator_params(axis='y',tight=True,nbins=10)
# # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
# # ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
# #    ax2.locator_params(axis='y', nbins=10)
# #    ax2.locator_params(axis='x', nbins=10)
# ax1.set_title(title)
# ax1.grid()
# lns = lns2+lns3
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=0)
# plt.tight_layout()
# fname = f'{title.replace(" ","_").replace(":","-")}.png'
# fig.savefig(f'{path}\\{fname}')