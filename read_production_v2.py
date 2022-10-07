# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:59:15 2020

@author: sbergmann
"""

import devdata as dv
import pandas as pd
import os as os
import glob as glob
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


'''
Tool zum einlesen von Produktionsdaten und Erstellung von Grafiken zu diesen.

Hier: HWC Daten von LXG445 im Zeitraum 2020, unterteilt in EPA und ISO
--> Pickle Datei der eingelesenen HWC Daten von 2020 vorhanden
'''

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

"""
output = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG445\python\outputs'
"""
# 'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG445\python\outputs'

"""
Source Path of data
"""

path = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG445\Analytical_Unit'

"""
output path of data
"""

output = r'C:\Users\bhoheisel\Desktop\Output'


"""
Prefix of dataname
"""

prefix = 'PRC'

"""
Time of scope (Required)
"""

planetime = ['20180101','20220331']



dtformat = '%Y%m%d'
time = [datetime.strptime(t,dtformat) for t in planetime]
dt = timedelta(hours=12) # +/- planetime zur richtigen Einstellung der x-Achse

block = 'PRC_AU_Hardware'

files = glob.glob(path+'\\'+prefix+'*.csv')
files = files + glob.glob(PATHNUMMERODUO+'\\'+prefix+'*.csv') # DIE ZEILE WENN DATEN AUS 2. ORDNER IDENTISCH BEHANDELT WERDEN SOLLTEN
# files = [f for f in files if year in f.split('_')[-2][:4]]
files = [f for f in files if ((datetime.strptime(f.split('_')[-2],dtformat)>=time[0]) & (datetime.strptime(f.split('_')[-2],dtformat)<time[1]))]
# files = files[0:10]
lenfiles = len(files)-1



failures =[]
df = pd.DataFrame()

# for n,f in enumerate(files):
#     printProgressBar(n, lenfiles)
#     try:
#         df = pd.concat([df, dv.messung(f)])
#     except:
#         failures.append(f)
#         print(f'Datei {os.path.basename(f)} konnte nicht eingelesen werden')
        
# schneller
temp = pd.DataFrame()
for n,f in enumerate(files):
    printProgressBar(n,lenfiles)
    try:
        temp = pd.concat([temp,dv.messung(f)])
    except IndexError:
        failures.append(f)
        print(f'Datei {os.path.basename(f)} konnte nicht eingelesen werden')
    if (n/100)%1 == 0:
        df = pd.concat([df,temp])
        temp = pd.DataFrame()
        # print('reset')
        
df = pd.concat([df,temp])

output = output+f'\\{planetime[0]}{planetime[1]}'
os.mkdir(f'{output}')
        
print("\nErstelle alle plots\n")
mydpi=96
# vaa = df[df['block']==block]['VAAxxx'].unique().tolist()[0]
VAAxxx = df[df['block']==block]['VAAxxx'].unique().tolist()
lenVAA = len(VAAxxx)-1
for n,vaa in enumerate(VAAxxx):
    printProgressBar(n, lenVAA)
    temp = df[df['VAAxxx']==vaa]
    epa = temp[(temp['AUType']=='EPA') | (temp['AUType']=='EPA (auto verify)')]
    iso = temp[(temp['AUType']=='ISO') | (temp['AUType']=='ISO (auto verify)')]
    
    #plot data
    fig,ax = plt.subplots(2,1, sharey=True,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi,constrained_layout=True)    
    title = fig.suptitle(f'{vaa} im Zeitraum von {temp["date"].min()} bis {temp["date"].max()}')
    try:
        ax[0].scatter(epa['date'], epa['actVal'], s=2, alpha=0.6, color='blue')
        ax[0].set_ylabel(epa['Unit'].iloc[0])
        ax[0].plot(epa['date'],epa['loTol'],linewidth=0.8,alpha=0.5,color="green",label='Toleranzen')
        ax[0].plot(epa['date'],epa['NomVal'],linewidth=0.8,alpha=0.5,color="black",label='NominalVal')
        ax[0].plot(epa['date'],epa['upTol'],linewidth=0.8,alpha=0.5,color="green")
        ax[0].set_ylim(epa['upTol'].iloc[0]*1.025,epa['loTol'].iloc*0.975)
        ax[0].legend()
    except: 
        pass

    try:
        ax[1].scatter(iso['date'], iso['actVal'], s=2, alpha=0.6, color='red')
        ax[1].set_ylabel(iso['Unit'].iloc[0])
        ax[1].plot(iso['date'],iso['loTol'],linewidth=0.8,alpha=0.5,color="green",label='Toleranzen')
        ax[1].plot(iso['date'],iso['NomVal'],linewidth=0.8,alpha=0.5,color="black",label='NominalVal')
        ax[1].plot(iso['date'],iso['upTol'],linewidth=0.8,alpha=0.5,color="green")
        ax[1].set_ylim([iso['upTol'].iloc[0]*1.025,iso['loTol'].iloc*0.975])
        ax[1].legend()
    except: 
        pass

    ax[0].set_title('EPA')
    ax[1].set_title('ISO')
    ax[1].set_xlabel('Datum')
    
    #Beschränkung der x-Skala auf den Auswertezeitraum (Dateien mit fehlerhafter Datumsangabe werden so ausgeblendet)
    ax[0].set_xlim(time[0]- dt,time[-1]+ dt)
    ax[1].set_xlim(time[0]- dt,time[-1]+ dt)
    
    fname = f'{output}\\{vaa}.png'
    fig.savefig(fname)
    plt.close()


df.to_pickle(f'{output}\\data_{prefix}_{planetime[0]}_{planetime[1]}.pickle')
# df = pd.read_pickle('lxg445_hwc.pickle')