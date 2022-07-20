# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 08:48:38 2022

@author: sbergmann
"""

import os as os
import glob as glob
import pandas as pd
import shutil as shutil

'''
Programm zum automatischen Verschieben von Wiederholmessungen des selben
Gerätes bzs Tests.
'''

basepath = r'C:\Users\sbergmann\Desktop\Nitro\mb5b\move_test'
bases = ['HWC','WIPSCAN']
dtypes = ['.csv','.csv.png',]
all_files = glob.glob(basepath+'\\*.*') 

split = '_'
pos = 2
keep = 'latest'  

files = []
ending = []
for dt in dtypes:
    for f in all_files:
        if dt == f[-len(dt):]:
            files.append(f)
            ending.append(dt)


archiv = os.path.join(basepath,'Archiv')
try:
    os.mkdir(archiv)
except FileExistsError:
    pass    
    
df = pd.DataFrame({'file':files})
df['dtype'] = ending
df['key'] = df['file'].apply(lambda x: os.path.basename(x).split(split)[pos])
df['base'] = df['file'].apply(lambda x: os.path.basename(x).split(split)[0])
df['ctime'] = df['file'].apply(lambda x: os.path.getctime(x))
df['mtime'] = df['file'].apply(lambda x: os.path.getmtime(x))
df.drop_duplicates('file',inplace=True)


move = []
for key in df['key'].unique():
    for base in bases:
        temp = df[(df['key']==key)&(df['base']==base)]
        for dt in dtypes:
            temp_dt = temp[temp['dtype']==dt]
            temp_dt = temp_dt.sort_values(by='mtime',)
            temp_dt = temp_dt['file'].to_list()
            if keep == 'latest':
                move+=temp_dt[:-1]
            elif keep == "oldest":
                move+=temp_dt[1:]

for f in move:
    shutil.move(f,os.path.join(archiv,os.path.basename(f)))
