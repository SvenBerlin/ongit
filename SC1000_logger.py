# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:07:56 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import glob as glob
import os as os 
from datetime import datetime, date

# path = r'C:\Users\sbergmann\Desktop\HALT Alfa Laval\Logger'
# path = os.path.abspath(path)

# files = glob.glob(path+'\*.csv')
# filename=path+'\logger'

files = glob.glob('*.csv')
filename='combined_log'

df = pd.DataFrame()
for file in files:
    if os.path.basename(file) != os.path.basename(filename+'.csv'):
        temp = pd.read_csv(file,skiprows=87)
        temp.rename( columns={'Unnamed: 0':'DATUM'}, inplace=True )
        temp.drop(len(temp)-1,inplace=True)
        temp['DATUM'] =  pd.to_datetime(temp['DATUM'], format='%Y/%m/%d %H:%M:%S')
        # temp = temp[temp['DATUM']>datetime(2020,3,17,0,0,0)]
        temp.set_index('DATUM',inplace=True)
        df=pd.concat([df,temp],axis=1)#,ignore_index=True)
        df.dropna(inplace=True)
# df.to_csv(filename+'.csv')

excel_file = filename+'.xlsx'
sheet_name = 'Logs'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)
workbook = writer.book
worksheet = writer.sheets[sheet_name]
chart = workbook.add_chart({'type': 'line'})
for col in range(df.shape[1]):
    chart.add_series({
        'categories': [sheet_name, 1, 0, len(df)+1, 0],
        'name':       [sheet_name, 0, col+1],
        'values':     [sheet_name, 1, col+1, len(df)+1, col+1],
        'gap':        10,
    })

chart.set_x_axis({'date_axis':False,'name': 'DATUM'})
chart.set_y_axis({'min':0,'max':25,'name': 'Value', 'major_gridlines': {'visible': True}})
worksheet.insert_chart('B2', chart)
writer.save()
