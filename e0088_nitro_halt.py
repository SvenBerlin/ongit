# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 11:20:43 2019

author: Jan Wykhoff
copyright@HACH LANGE GmbH 2018
For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""
#  sehr häufig verwendete Pakete:
import os as os
from os.path import sep as sep
import glob as glob
import matplotlib.pyplot as plt
#import devdata as dv
#date = dv.dvtime(formatmode='dformat_dateiname')
from datetime import datetime
date = datetime.now().strftime("%d%m%Y_%H%M%S")

#  import shutil as sh # z.B. copy für Dateien
#  import matplotlib.pyplot as plt
import pandas as pd
#  eigene Pakete:
# import devdata as dv
#ordner = os.path.abspath(r'C:\Users\jwykhoff\python\globalWorkingDir\forpythonpath\devdata\_test\nitro\alt')
ordner = os.path.abspath(r'C:\Users\sbergmann\Desktop\nitro')
allfiles = glob.glob(ordner +sep+'*EE*_*.csv')
dflist=[]
for file in allfiles:
    dfi = pd.read_csv(file,skiprows = 20)
    dflist.append(dfi)
df = pd.concat(dflist)
df.index = range(len(df))
df.rename(columns={'#DateTime':'DateTime'}, inplace = True)
#  h = df['TimeStamp']
#  df['TimeStamp'] = h.to_timestemp()
cols=['DateTime', 'FlashLampVoltage', 'WiperDrivingSectionPeakCurrent_mA', 'mExtM2_M1', 'mExtM3_M1', 'mExtM3_M2',   'TemperatureFlashBoard', 'HumidityFlashboard']
df = df[cols]

df['DateTime']=pd.to_datetime(df['DateTime'])
df.drop(index=[0,1],inplace=True)
df.reset_index(drop=True,inplace=True)

wiper = pd.notna(df['WiperDrivingSectionPeakCurrent_mA'])
df_wiper = df[wiper]['WiperDrivingSectionPeakCurrent_mA']
df_wiper.reset_index(drop=True, inplace=True)
df.drop(df[wiper].index,inplace=True)
df.reset_index(drop=True,inplace=True)
df['WiperDrivingSectionPeakCurrent_mA']=df_wiper

df['Type'] = 0
wiper = pd.notna(df['WiperDrivingSectionPeakCurrent_mA'])
df['Type'][wiper] = 'wiper'
df['Type'][~wiper] = 'simple'


#freq_list = []

# First line is empty
#freq_list.append("")

# Calculate frequency according to flash lamp total count and passed time since
# pevious log entry
#for i in range(1, len(df)):
#    freq_diff = df['FlashLampTotalCount'][i] - df['FlashLampTotalCount'][i-1]
#    time_diff_s = (df['DateTime'][i] - df['DateTime'][i-1]).total_seconds()
 #   freq_list.append(freq_diff / time_diff_s)

#df['Frequency'] = freq_list

#df.to_excel(ordner + sep + 'a6.xlsx')
excel_file = ordner + sep + date+'.xlsx'
positions = ['G2','O2','W2', 'G18','O18','W18', 'O34', 'G34'   ]
xlabels = ['Time [h]', 'Time [h]', 'Time [h]', 'Time [h]', 'Time [h]', 'Time [h]', 'Time [h]', 'Time [h]']
ylabels = ['Voltage [V]','flashes', 'Voltage [V]', 'Voltage [V]','Celcius [°C]','Humiditiy [%]', 'Frequency [Hz]','Frequency [Hz]']

sheet_name = 'Sheet1'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)
workbook = writer.book
worksheet = writer.sheets[sheet_name]
for col in range(len(positions)):
    chart = workbook.add_chart({'type': 'line'})
    
    if 'Wiper' in df.columns[col+1]:
        temp = df[df['Type']=='wiper']
    else:
        temp = df[df['Type']=='simple']

    chart.add_series({
        'categories': ['Sheet1', 1, 0, len(temp)+1, 0],
        'name':       ['Sheet1', 0, col+2],
        'values':     ['Sheet1', 1, col+2, len(temp)+1, col+2],
        'gap':        10,
    })

    chart.set_x_axis({'name': xlabels[col]})
    chart.set_y_axis({'name': ylabels[col], 'major_gridlines': {'visible': True}})


    worksheet.insert_chart(positions[col], chart)

writer.save()

df['FlashLampVoltage'].plot()
#df.plot(kind'scatter',x='num_children', y='num_pets', color='')
