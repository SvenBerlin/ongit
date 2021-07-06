# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:59:15 2020

@author: sbergmann
"""

import devdata as dv
import pandas as pd
import os as os
import glob as glob
from datetime import datetime
from matplotlib import dates

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


'''
Tool zum einlesen von Produktionsdaten und Erstellung von Grafiken zu diesen.
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

# Hier den Pfad zu den Dateien angeben
path = r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\19_Sustaining\RustyIssue_Feb2021\FI_Daten_2020_komplett'
prefix = 'FI'
read_pickle = True #hier einstellen ob vorhandene Pickle-Datei (Datenkontainer) eingelesen werden soll

dateformat='%d/%m/%Y %H:%M:%S'
formatter = dates.DateFormatter(dateformat)


tols = {'NG11': 0.05, 'NG5':0.05, 'NG3':0.02} # Toleranzen für die jeweiligen Prüfmittel

block = ['HWC_Hardware','Fi']

output = path+ f'\\out'
if read_pickle:
    print('lese vorhandene pickle-Datei ein')
    file = glob.glob(output+'\\'+'*.pickle')[0]
    df = pd.read_pickle(file)
else:    
    print('lese Dateien vom gegebenen Pfad ein')
    files = glob.glob(path+'\\'+prefix+'*.csv')
    # files = files[:100]
    lenfiles = len(files)-1
    
    
    failures =[]
    df = pd.DataFrame()
    
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
    
    os.mkdir(f'{output}')
    
    df.loc[df["block"]==block[0],'VAAxxx'] =df[df["block"]==block[0]]['VAAxxx'].str.cat(df[df["block"]==block[0]]['Ident'],sep="_")
    df.loc[df["block"]==block[1],'VAAxxx'] =df[df["block"]==block[1]]['VAAxxx'].str.cat(df[df["block"]==block[1]]['name'],sep="_").str.cat(df[df["block"]==block[1]]['Ident'],sep="_")
    
    df['DateTime']=pd.to_datetime(df['DateTime'],format=dateformat)
    
    df.to_pickle(f'{output}\\data_{os.path.basename(path)}.pickle')
# output = 'output'
# os.mkdir(f'{output}')



print("\nErstelle alle plots\n")
mydpi=96
# vaa = df[df['block']==block]['VAAxxx'].unique().tolist()[0]


VAAxxx = df[df['block'].isin(block)]['VAAxxx'].unique().tolist()
# desc = [x for x in df[df['block'].isin(block)]]
lenVAA = len(VAAxxx)-1
for n,vaa in enumerate(VAAxxx):
    printProgressBar(n, lenVAA)
    temp = df[df['VAAxxx']==vaa]
    temp['actVal']=temp['actVal'].astype(float)
    if [glass for glass in list(tols.keys()) if glass in vaa]:
        temp['actVal']=temp['actVal']/temp['NomVal']
        
    temp_stats = temp.describe()
    
    mean_line = [temp_stats['actVal'].loc['mean']]*len(temp)
    plus_std3 = [mean_line[0]+(temp_stats['actVal'].loc['std']*3)]*len(temp)
    minus_std3 = [mean_line[0]-(temp_stats['actVal'].loc['std']*3)]*len(temp)
    plus_std5 = [mean_line[0]+(temp_stats['actVal'].loc['std']*5)]*len(temp)
    minus_std5 = [mean_line[0]-(temp_stats['actVal'].loc['std']*5)]*len(temp)
    
    
    fig, ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi))
    
    ax.plot(temp['datetime'], mean_line, 'r', label='mean' )
    ax.plot(temp['datetime'], plus_std3, 'g', label='+3s')
    ax.plot(temp['datetime'], minus_std3, 'g', label='-3s')
    ax.plot(temp['datetime'], plus_std5, 'b', label='-5s')
    ax.plot(temp['datetime'], minus_std5, 'b', label='-5s')
    
    glass = [glass for glass in list(tols.keys()) if glass in vaa]
    if glass:
        ax.plot(temp['datetime'], [1+tols[glass[0]]]*len(temp), 'k', label='up lim' )
        ax.plot(temp['datetime'], [1-tols[glass[0]]]*len(temp), 'k', label='lo lim' )
        ax.set_ylabel('%')
    else: 
        ax.plot(temp['datetime'], [temp["loTol"].iloc[0]]*len(temp), 'k', label='up lim' )
        ax.plot(temp['datetime'], [temp["upTol"].iloc[0]]*len(temp), 'k', label='lo lim' )
        ax.set_ylabel('value')
    
    ax.scatter(temp['datetime'], temp['actVal'],s=2.5,alpha=0.7)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
    
    ax.set_xlabel('time')
    ax.set_title(vaa)
    # ax.set(xlabel='time', ylabel='value',title=vaa)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    
  
    fname = f'{output}\\{vaa}.png'
    fig.savefig(fname)
    plt.close()
