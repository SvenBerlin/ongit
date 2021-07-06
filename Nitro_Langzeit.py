# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 07:59:48 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import glob as glob
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import seaborn as sns
sns.set(context='paper',style='whitegrid')
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import pickle
import os as os

path = r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3A\Stabilitätsmessungen_MB3A\Results'
files = glob.glob(path+'\*\Langzeitstabilität\*.csv')

files = [r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN11\Langzeittest_LXG448.99.22001_SN3B111809_201006_151751_xEnde.csv',
         r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN12\Langzeittest_LXG448.99.22001_SN3B120433_201006_150827_xEnde.csv',
         r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN15\Langzeittest_LXG448.99.22001_SN3B151718_201006_141340_Ende.csv',
         r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN16\Langzeittest_LXG448.99.22001_SN3B162530_201006_150958_Ende.csv',
         #r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3A\Stabilitätsmessungen_MB3A\Results\Sonde_05\Langzeitstabilität\EE_LXG448.99.22000_SN3A052420_200814_133851.csv',
        # r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3A\Stabilitätsmessungen_MB3A\Results\Sonde_06\Langzeitstabilität\EE_LXG448.99.22000_SN3A063623_200814_140725.csv',
         ]

nitro_cols = ['mExtM2_M1','mExtM3_M1','mExtM3_M2','TemperatureFlashBoard', 'TemperatureMainboard']
# f = r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3A\Stabilitätsmessungen_MB3A\Results\Sonde_01\Langzeitstabilität\EE_LXG448.99.22000_SN3A011728_200814_140902.csv'
plot_folder = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Langzeit_plots'
for f in files:
    
    nitro = pd.read_csv(f, usecols=[0], header=None, skip_blank_lines=False)
    idx = nitro[nitro[0] == '#DateTime'].index[0]
    nitro = pd.read_csv(f, skiprows=idx, skip_blank_lines=False)    
    nitro['#DateTime'] = pd.to_datetime(nitro['#DateTime'],format='%Y-%m-%dT%H:%M:%S', errors='ignore')    
    nitro.set_index('#DateTime', drop=True, inplace=True)
    for col in nitro_cols:
        nitro[col] = pd.to_numeric(nitro[col],downcast='float')

    new_csv = pd.read_csv(f, header=None, sep='?')
    new_csv = pd.concat([new_csv.iloc[:idx],new_csv.iloc[idx::10]])
    fname = os.path.dirname(f)+'\\gekürzt_'+os.path.basename(f)
    new_csv.to_csv(fname)

    sonde = f.split('\\')[-3]
    ### Single 
    mydpi=96
    fig,(ax1, ax2) = plt.subplots(2,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi,sharex=True)
    ax12 = ax1.twinx()
    ax12.spines["right"].set_position(("axes", 1))
    ax12.spines["right"].set_visible(True)
    
    lns1 = ax1.plot(nitro[nitro_cols[0]].iloc[2:], label=nitro_cols[0],color='red')
    lns12 = ax1.plot(nitro[nitro_cols[1]].iloc[2:], label=nitro_cols[1],color='blue')
    lns13 = ax1.plot(nitro[nitro_cols[2]].iloc[2:], label=nitro_cols[2],color='green')
    lns14 = ax12.plot(nitro[nitro_cols[3]].iloc[2:], label=nitro_cols[3], color='black')
    lns15 = ax12.plot(nitro[nitro_cols[4]].iloc[2:], label=nitro_cols[4], color='darkgray')
    
    ax1.set_ylabel('mExt')
    ax12.set_ylabel('Temperatur °C')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
    ax1.xaxis.set_tick_params(rotation=45)
    ax1.set_title('Nitro Langzeittest ({}) - {} bis {}'.format(sonde,
                    datetime.strftime(nitro.index[0], '%d.%m.%Y %H:%M:%S'),datetime.strftime(nitro.index[-1], '%d.%m.%Y %H:%M:%S')))
    lns = lns1+lns12+lns13+lns14
    labs = [l.get_label() for l in lns]
    legend = ax1.legend(lns, labs, loc=0)
    
    ax21 = ax2.twinx()
    ax21.spines["right"].set_position(("axes", 1))
    ax21.spines["right"].set_visible(True)
    
    
    lns2 = ax2.plot(nitro[nitro_cols[0]].iloc[2:], label=nitro_cols[0],color='red')
    lns21 = ax2.plot(nitro[nitro_cols[1]].iloc[2:], label=nitro_cols[1],color='blue')
    lns22 = ax21.plot(nitro[nitro_cols[3]].iloc[2:], label=nitro_cols[3],color='black')
    
    ax2.set_xlabel('Datum')
    ax21.set_ylabel('Temperatur °C')
    ax2.set_ylabel('mExt')
    # ax2.set_ylim()
    # ax2.relim()
    # ax2.autoscale_view() 
    
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
    ax2.xaxis.set_tick_params(rotation=45)
    lns = lns2+lns21+lns22
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    
    fname = 'Nitro_Langzeittest_{}_{}_{}'.format(sonde,datetime.strftime(nitro.index[0], '%Y%m%d'),datetime.strftime(nitro.index[-1], '%Y%m%d'))
    fig.savefig(os.path.join(plot_folder,fname+'.jpg'))
    plt.close()