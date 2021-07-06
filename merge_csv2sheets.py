# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:57:51 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import glob as glob
import os as os

path = r'C:\Users\sbergmann\Desktop\XQA006\LED_Juni2020\OP234'
files = glob.glob(path+'\*.csv')

excel_file = 'OP234.xlsx'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
workbook = writer.book

for f in files:
    df = pd.read_csv(f, header=None)
    df=df[df.columns].apply(pd.to_numeric, errors = 'coerce').combine_first(df)
    sheet_name = os.path.basename(f).split('.')[0]
    df.to_excel(writer,sheet_name=sheet_name,index=False, header=False)
        
writer.save()
