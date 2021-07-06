# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:57:51 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import glob as glob
import os as os
from datetime import datetime

class GONIOEXCEL():
    def __init__(self,path,user,note):
        self.path = path
        self.excel_file = self.getName()
        self.user = user
        self.note = note
        self.files = glob.glob(self.path+'\*.csv')
        self.numofcharts = self.getnumofcharts()
        # self.create()
        
    def getName(self):
        name = '{}.xlsx'.format(os.path.basename(path))
        if os.path.isfile(name): name = addSuffix(name)
        return name
    
    def _create(self):
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        workbook = writer.book
        
        worksheet = workbook.add_worksheet('Uebersicht')
        
        worksheet.write(0,0, date_time)
        worksheet.write(0,1, user)
        worksheet.write(3,1,'Messbedingungen')
        worksheet.insert_textbox(3,2, note)
        
        
        
    def getnumofcharts(self):
        return pd.DataFrame(self.files)[0].apply(lambda x: os.path.splitext(os.path.basename(x))[0].split('_')[-1]).unique()
    
    def addSuffix(fname):
        base = fname
        num = 1
        while os.path.isfile(fname):
            prefix='0{}'.format(num)[-2:]
            fname = "{0}_{2}{1}".format(*os.path.splitext(base) + (prefix,))
            num +=1
        return fname
        
def addSuffix(fname):
    base = fname
    num = 1
    while os.path.isfile(fname):
        prefix='0{}'.format(num)[-2:]
        fname = "{0}_{2}{1}".format(*os.path.splitext(base) + (prefix,))
        num +=1
    return fname


path = r'C:\Users\sbergmann\Desktop\XQA006\LED_Juni2020\OP234'
files = glob.glob(path+'\*.csv')

date_time = datetime.strftime(datetime.now(), '%d.%m.%Y')
user = 'Sven Bergmann/EGO'
note = ['Dunkelraum (EGO)',
        'LSC100 Goniometer',
        '10xOP234',
        '100mA/2V',
        '10mA/2V',]
row_chart = str(6+len(note))
note = '\n'.join(note)

excel_file = '{}.xlsx'.format(os.path.basename(path))
if os.path.isfile(excel_file): excel_file = addSuffix(excel_file)

writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
workbook = writer.book

worksheet = workbook.add_worksheet('Uebersicht')

worksheet.write(0,0, date_time)
worksheet.write(0,1, user)
worksheet.write(3,1,'Messbedingungen')
worksheet.insert_textbox(3,2, note)

chart1 = workbook.add_chart({'type': 'line'})
chart1.set_title({'name': f'Relative Intensitäten der spektralen Messung {note[3]}'})
chart1.set_x_axis({'name': 'Wellenlänge (nm)'})
chart1.set_y_axis({'name': 'relative Intensitaet (1)', 'major_gridlines': {'visible': True}})

# chart2 = workbook.add_chart({'type': 'line'})
# chart2.set_title({'name': 'Relative Intensitäten der spektralen Messung (10mA/2,0V)'})
# chart2.set_x_axis({'name': 'Wellenlänge (nm)'})
# chart2.set_y_axis({'name': 'relative Intensitaet (1)', 'major_gridlines': {'visible': True}})

for f in files:
    df = pd.read_csv(f, header=None)
    df=df[df.columns].apply(pd.to_numeric, errors = 'coerce').combine_first(df)
    sheet_name = os.path.basename(f).split('.')[0]
    df.to_excel(writer,sheet_name=sheet_name,index=False, header=False)
    worksheet = workbook.worksheets()[-1]
    for x in range(46,len(df)):
        worksheet.write_formula(x,53,'=(AB'+str(x+1)+'/MAX(AB47:AB'+str(len(df))+'))')
    if sheet_name.split('_')[-1] == '100mA':
        chart1.add_series({
            'categories': [sheet_name, 46, 0, len(df)+1, 0],
            'name':       sheet_name,
            'values':     [sheet_name, 46, 53, len(df)+1, 53],
            'gap':        10,
        })
    else:
        chart2.add_series({
            'categories': [sheet_name, 46, 0, len(df)+1, 0],
            'name':       sheet_name,
            'values':     [sheet_name, 46, 53, len(df)+1, 53],
            'gap':        10,
        })
    
chart1.set_size({'width': 800, 'height': 500})
chart2.set_size({'width': 800, 'height': 500})

worksheet = workbook.worksheets()[0]

worksheet.insert_chart('B{}'.format(row_chart), chart1)
worksheet.insert_chart('O{}'.format(row_chart), chart2)
    
writer.save()
