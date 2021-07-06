# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 07:56:49 2018

@author: sbergmann

Copyright@Hach Lange GmbH 

Script for evaluation of FCT_JABIL files

The script creates separate figures for all FCT-test including tolarances
extracted from htm file.

Folder Structure:
    main-folder ()
        |
        --->HTML
        |     |
        |      -->htm file
        |
        --->weekly csv files

Paratmeters
----
path: string
    path to main folder that holds all csv files
    
Output
----
fig: png
    Grafiken über alle Testpunkte des FCTs (abgespeichert in einem neuerstellten Ordner)
    Figures of all FCT tests (saved to new created foler)
"""

import glob 
import difflib
import pandas as pd
import os as os
import os.path
import matplotlib.pyplot as plt
from matplotlib import dates
#from matplotlib.pyplot import text
import matplotlib
matplotlib.use('Agg')
from datetime import datetime as datetime


def rm_corrupt_chars(in_str, corrupt=['/','#','\\','%']):
    out_str = in_str
    if any([b in in_str for b in corrupt]):
        out_str = out_str.replace('/','_')
        out_str = out_str.replace('%','p')
        out_str = out_str.replace('#','_')
        out_str = out_str.replace('\t','_t')     
    return out_str

dateformat='%m/%d/%Y-%H:%M:%S'
formatter = dates.DateFormatter(dateformat)

path = r'C:\Users\sbergmann\Desktop\mustang'
csv_files = glob.glob(path+'\*.csv')

df = pd.DataFrame()
for file in csv_files:
    temp = pd.read_csv(file)
    week = file.split('\\')[-1].split('.')[0]
    temp.insert(loc=0, column='week', value=week)
    df = pd.concat([df,temp],ignore_index=True)
for col in df.columns:
    if df[col].dtype == 'bool':
        df[col]=df[col].astype(int)
try:
    df['TestTime'] = df['Date']+' '+df['Time']
    df.drop(['Date','Time'],axis=1,inplace=True) 
    dateformat='%d/%m/%Y %H:%M:%S'
    formatter = dates.DateFormatter(dateformat)
    df.rename(columns={'Serial Number':'SerialNumber'},inplace=True)
except:
    pass
try:
    passmap = {'PASS':1,'FAIL':0}
    df['TestResult']=df['TestResult'].map(passmap)
except:
    passmap = {'Pass':1,'Fail':0}
    df['Pass/Fail']=df['Pass/Fail'].map(passmap)
df.dropna(axis=0,inplace=True)
df.reset_index(drop=True,inplace=True)
df['TestTime'] =pd.to_datetime(df['TestTime'],format=dateformat)
df_stats = df.describe()

data_set = pd.DataFrame(df.week.drop_duplicates().reset_index(drop=True))
data_set['time'] = df.iloc[df.week.drop_duplicates(keep='last').index.tolist()]['TestTime'].values

# öffne html Datei (enthält die Grenzen der einzelnen Testparameter)
html_file = glob.glob(path+'\*\*.htm')[0]
bounds=pd.read_html(html_file, skiprows=1)[0]
bounds.columns=bounds.iloc[0]
bounds=bounds.reindex(bounds.index.drop(0))

new_path = path+'\\Auswertung'
if not os.path.exists(new_path):
    os.makedirs(new_path)
#labelCounter = (len(str(len(df.columns[2:])))+1)*"0"
labelCounter = (len(str(len(df_stats.columns)))+1)*"0"
counter = 0
mydpi =96
#for col in df.columns:#[2:]:
for col in df_stats.columns:#[2:]:
    counter = counter+1
#    print(str(counter)+'/'+str(len(df.columns)-2)+': '+col)
    print(str(counter)+'/'+str(len(df_stats.columns))+': '+col)
                    
    fig, ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi))
    try:
        mean_line = [df_stats[col].loc['mean']]*len(df)
        plus_std3 = [mean_line[0]+(df_stats[col].loc['std']*3)]*len(df)
        minus_std3 = [mean_line[0]-(df_stats[col].loc['std']*3)]*len(df)
        plus_std5 = [mean_line[0]+(df_stats[col].loc['std']*5)]*len(df)
        minus_std5 = [mean_line[0]-(df_stats[col].loc['std']*5)]*len(df)
        
        ax.plot(df['TestTime'], mean_line, 'r--', label='mean' )
        ax.plot(df['TestTime'], plus_std3, 'g--', label='+3s')
        ax.plot(df['TestTime'], minus_std3, 'g--', label='-3s')
        ax.plot(df['TestTime'], plus_std5, 'b--', label='-5s')
        ax.plot(df['TestTime'], minus_std5, 'b--', label='-5s')
    except KeyError:
#        print('could not plot: {}'.format(col))
        pass
    
    try:
        testname = difflib.get_close_matches(col,bounds['Test Name'],n=1)[0]
        lbound = [float(bounds['Lower Limit'][bounds['Test Name']==testname].iloc[0])]*len(df)
        ubound = [float(bounds['Upper Limit'][bounds['Test Name']==testname].iloc[0])]*len(df)
#        lbound = [float(bounds['Lower Limit'][bounds['Test Name']==col].iloc[0])]*len(df)
#        ubound = [float(bounds['Upper Limit'][bounds['Test Name']==col].iloc[0])]*len(df)
        ax.plot(df['TestTime'], lbound, 'k--', label='up lim' )
        ax.plot(df['TestTime'], ubound, 'k--', label='lo lim' )
    except IndexError:
#        print('could not plot: {}'.format(col))
        pass
    
    # plot der eigentlichen Daten als letztes, damit Datenlinie über alle anderen liegt
    ax.scatter(df['TestTime'], df[col],s=1.5,alpha=0.7)
    
#    ypos = ax.get_ylim()[1]-(ax.get_ylim()[1]-ax.get_ylim()[0])*0.25
#    for enum,elm in enumerate(data_set['time']):
##        ax.axvline(x=elm,linewidth=0.8,linestyle='--', color='r')
#        ax.text(elm, ypos,data_set['week'].iloc[enum].split('_')[-1],{'alpha':0.6},rotation=90)
##        text = ax.annotate(data_set['week'].iloc[enum].split('_')[-1],xy=(elm, ax.get_ylim()[1]))
##        text.set_alpha(.6)
##        text(elm, ax.get_ylim()[1], data_set['week'].iloc[enum].split('_')[-1],
##             rotation=90, verticalalignment='center')

    try:
        # Bug-Umgehung: wenn ohne, Grafiken mit konstanten Werten erhalten exponentielle y-Achse
        ax.ticklabel_format(useOffset=False, axis='y') 
    except AttributeError:
        pass
    
    ax.set(xlabel='time', ylabel='value',title=col)

    ax.set_xticklabels(labels=df['SerialNumber'],rotation=90)
    ax.xaxis.set_major_formatter(formatter)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    
    # Testnamen enthalten zum Teil verbotene Buchstaben, die nicht als Namen im Windowsdateisystem verwendet werden können
#    if '/' or '#' or '\\' in col:
#       col = col.replace('/','_')
#       col = col.replace('#','_')
#       col = col.replace('\t','_t')
    name= rm_corrupt_chars(col)
    fname=new_path+'\\'+(labelCounter+str(counter)+'_')[-4:]+name
    fname = fname[:255] # wegen zu langen Dateinamen (256+'.png' = 260)
#    fig.savefig(new_path+'\\'+(labelCounter+str(counter)+'_')[-4:]+name+'.png')
    fig.savefig(fname+'.png')
    
        
    plt.close(fig)