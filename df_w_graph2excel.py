# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:13:13 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

excel_file = 'axis_labels.xlsx'
positions = ['G2','O2','G18','O18']
sheet_name = 'Sheet1'
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)
workbook = writer.book
worksheet = writer.sheets[sheet_name]
for col in range(df.shape[1]):
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': ['Sheet1', 1, 0, len(df)+1, 0],
        'name':       ['Sheet1', 0, col+1],
        'values':     ['Sheet1', 1, col+1, len(df)+1, col+1],
        'gap':        10,
    })

    chart.set_x_axis({'name': 'Index'})
    chart.set_y_axis({'name': 'Value', 'major_gridlines': {'visible': True}})


    worksheet.insert_chart(positions[col], chart)

writer.save()
