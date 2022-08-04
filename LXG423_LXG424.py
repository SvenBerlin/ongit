# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:10:35 2022

@author: sbergmann
"""

import os as os
import glob as glob
import pandas as pd
from datetime import datetime

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


path = [r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG423',
        r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG424']

files = []
for p in path:
    files += glob.glob(p+'\\*.xls*')

tol_all =[]
dates = []
tol_19 =[]
sn_all = []
sn_19 = []
selected =[]
for n,f in enumerate(files):
    printProgressBar(n,len(files), prefix=f'read file {n}/{len(files)}')
    try:
        df = pd.read_excel(f)
    except Exception as e:
        print(f'{e} >>> {f}')
    date = df[df['Unnamed: 1']=='Datum']['Unnamed: 3'].iloc[0]
    dates.append(date)
    # if type(date) == datetime:
    try: 
        tol = float(df[df['Unnamed: 1']=='Toleranz']['Unnamed: 3'].iloc[0])
    except ValueError:
        tol = float(df[df['Unnamed: 1']=='Toleranz']['Unnamed: 3'].iloc[0].replace(',','.'))
    try:
        sn = df[df['Unnamed: 1']=='Gerätenummer']['Unnamed: 3'].iloc[0]
        sn_all.append(sn)
    except:
        pass
    tol_all.append(tol)
    
    # if (date >= datetime(2019,1,1)) and (tol > 5):
    if (date >= datetime(2019,1,1)):
        tol_19.append(tol)
        sn_19.append(sn)
        if (tol >= 5):
            selected.append(f)
            print(f)
data = pd.DataFrame()
data = pd.concat([pd.DataFrame(data=sn_all),
                  pd.DataFrame(data=tol_all),
                  pd.DataFrame(data=sn_19),
                  pd.DataFrame(data=tol_19)],axis=1)
data.columns='sn tol_all sn_19 tol_19'.split()
stats = data.describe([.1,.2,.3,.4,.5,.6,.7,.8,.9])
# data['sn'] = sn_all
# data = pd.concat()
# data["all"] = tol_all
# data['sn_19'] = sn_19
# data['tol_19'] = tol_19



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
plt.scatter(np.arange(0,len(tol_all),1),tol_all,s=2)
plt.xlabel("1")
plt.ylabel("Toleranz")
plt.title("LXG423 LXG424 Toleranz")

mydpi=96
fig, ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
ax1.scatter(dates,tol_all,s=2,label='Toleranzen')
ax1.plot([min(dates),max(dates)],[np.mean(tol_all)]*2,color='red',linewidth=1.5,label=r'$\bar{x}$')
ax1.plot([min(dates),max(dates)],[np.mean(tol_all)+np.std(tol_all)*3]*2,color='red',linewidth=1.5,linestyle='-.',label=r'$\bar{x} + 3\sigma$')
ax1.set_xlabel('Datum')
ax1.set_ylabel('Toleranz')
ax1.set_title(f'LXG423/LXG424 Historie der Zertifikate bis {max(dates)}: Toleranzdaten')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
ax1.xaxis.set_tick_params(rotation=90,)
ax1.xaxis.set_major_locator(plt.MaxNLocator(40))
ax1.set_xlim([datetime.datetime(2004,2,1),max(dates)+datetime.timedelta(days=30)])
ax1.tick_params(axis='both', which='major', labelsize=8)
ax1.minorticks_on()
ax1.legend()
ax1.grid()
props = dict(boxstyle='round', facecolor='wheat', alpha=1)
textstr = '\n'.join((
    r'$\bar{x} = %.2f$' % (np.mean(tol_all), ),
    r'$3\sigma = %.2f$' % (np.std(tol_all)*3,)))
# textstr = '$\bar{x} = {round(np.mean(tol_all),3)\n3\sigma = {round(np.std(tol_all)*3,3)}$'
ax1.text(0.9, 0.95, textstr, transform=ax1.transAxes, fontsize='small',
        verticalalignment='top', bbox=props)
plt.tight_layout()
