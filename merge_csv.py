# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 07:53:29 2021

@author: sbergmann
"""

import os as os
import pandas as pd
import glob as glob


path = r'C:\Users\sbergmann\Desktop\Aquarius\Breadboard\Dauertest'
path = os.path.abspath(path)
fname = os.path.join(path,f'{os.path.basename(path)}.csv')

prefix = '' # zur gezielten Selektion von bestimmten csv-Dateien innerhalb eines Archivs
skiprows = 0 # zu überspringende Zeilen beim Einlesen (multicolumnlengths)
droprows = [1] # Liste der nicht zuberücksichtigen Zeilen der eingelesenen Daten 
files = glob.glob(path+f'\\{prefix}*.csv')

df = pd.DataFrame()

for f in files:
    temp = pd.read_csv(f, skiprows=skiprows)
    try:
        temp.drop(temp.index[droprows],inplace=True)
    except:
        pass
    df = pd.concat([df,temp])

df.reset_index(drop=True, inplace=True)
df.to_csv(fname,index=True,header=True)    


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta

df.DateTime = pd.to_datetime(df.DateTime)
df.actVal = pd.to_numeric(df.actVal, errors='coerce')
df.dropna(subset=['actVal'],inplace=True)

dt = timedelta(minutes=10)

z = np.polyfit(df.index, df.actVal, 1)
p = np.poly1d(z)
fit = p(df.index)
mydpi = 96

fig,ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
lns1 = ax.plot(df.sort_values(by=['DateTime']).DateTime,df.sort_values(by=['DateTime']).actVal, label='Luft_355nm')
# lns1 = ax.plot(df.DateTime,df.actVal, label='Luft_355nm')
lns2 = ax.plot(df.sort_values(by=['DateTime']).DateTime,fit, label='fit')
ax.set_xlabel('Zeit')
ax.set_ylabel('Photostrom (A)')
ax.set_title('Breadboard_Dauertest')
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.set_xlim([df.DateTime.min()-dt, df.DateTime.max()+dt])
# ax.set_ylim([df.actVal.min()*0.9,df.actVal.max()*1.1])
# ax.set_ylim([0,6*10e-9])


props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# textstr = f'min = {round(fit.min(),10)}A\nmax = {round(fit.max(),10)}A\nrange = {round(fit.max()-fit.min(),10)}A'
textstr = f'min = {round(df.actVal.min(),10)}A\nmax = {round(df.actVal.max(),10)}A\nrange = {round(df.actVal.max()-df.actVal.min(),10)}A'
ax.text(0.7, 0.25, textstr, transform=ax.transAxes, fontsize='small',
        verticalalignment='top', bbox=props)

# lns = lns1
# labs = [l.get_label() for l in lns]
# ax.legend(lns, labs, loc=0)

ax.legend()
plt.tight_layout()

# import numpy as np

# def trans2ext(trans):
#     return np.log10(trans**-1)

# fit_trans = fit-fit[0]
# fit_ext = trans2ext(trans)
# t0 = trans2ext(fit[0])
