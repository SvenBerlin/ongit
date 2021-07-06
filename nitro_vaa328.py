# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 09:10:18 2020

@author: sbergmann
"""

import pandas as pd
import numpy as np
import os as os
import glob as glob
import math


paths = [r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN11\VAA328\3.Versuch',
         r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MB3B\Stabilitätsmessungen_MB3B\Results\SN12\VAA328\3.Versuch',
         r'nächster Pfad']
paths = [os.path.abspath(path) for path in paths]

df = pd.DataFrame()
fields = ['mExtM2_M1','mExtM3_M1','mExtM3_M2']

for n,sonde in enumerate(paths):
    files = glob.glob(sonde+'/*.csv')
    temp = pd.DataFrame(columns=['VAA','SN']+fields)
    for f in files:
        base = os.path.basename(f).split('_')
        if "LXG" in base[3]:
            vaa = '_'.join(base[1:3])
            sn = base[4][4:6]
        else:
            vaa = '_'.join(base[1:4])
            sn = base[5][4:6]
        
        h = pd.read_csv(f,skiprows=22, usecols=fields)
        for null_row,x in enumerate(h.iloc[:,0]):
            if math.isnan(x):
                null_row +=1
                break

        h = h.iloc[null_row:,:]
        h.reset_index(drop=True, inplace=True)
        # row += h.mean().tolist()
        temp = temp.append({'VAA':vaa,
                     'SN':sn,
                     'mExtM2_M1':h['mExtM2_M1'].mean(),
                     'mExtM3_M1':h['mExtM3_M1'].mean(),
                     'mExtM3_M2':h['mExtM3_M2'].mean(),},ignore_index=True)
    temp.set_index('VAA',drop=True,inplace=True)
    df = pd.concat([df,temp])
        
iterables = [fields, df.SN.unique().tolist()]   
index = pd.MultiIndex.from_product(iterables, names= ['Kanal', 'Sonde'])
k = pd.DataFrame(index=df.index.unique().tolist(),columns=index)
for n,sn in enumerate(df.SN.unique().tolist()):
    k['mExtM2_M1',sn] = df[df['SN'] == sn]['mExtM2_M1']
    k['mExtM3_M1',sn] = df[df['SN'] == sn]['mExtM3_M1']
    k['mExtM3_M2',sn] = df[df['SN'] == sn]['mExtM3_M2']

mapper = {'11':'5mm', '12':'5mm',
          '13':'2mm', '14':'2mm',
          '15':'1mm', '16':'1mm'}

info = pd.DataFrame(index=['Spalt'],columns=index)
for col in k.columns.tolist():
    print(col)
    info[col] = mapper[col[1]]
k = k.append(info)
    
k.to_excel('test.xlsx')
    
        