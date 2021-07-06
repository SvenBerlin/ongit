# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 08:46:37 2021

@author: sbergmann
"""

'''
Tool zum ersetzen eines Substring durch einen anderen innerhalb einer CSV-Datei.
Die Datei wird mit dem Prefix "mod_" abgespeichert.

'''

# import pandas as pd
import glob as glob
# import os as os 
# import csv

search_for = 'T'
replace_with = ' '

path = r'C:\Users\sbergmann\Desktop'
files = glob.glob(path+'//EE*.csv')

for f in files:
    
    file = open(f, 'r') 
    lines = file.readlines() 
    if lines[0][0] != '[':
        lines[0] = lines[0][3:]
    for idx,line in enumerate(lines):
        if '#DateTime' in line:
            break
    
    for n in range(idx+1,len(lines)-1):
        lines[n] = lines[n].replace('T', ' ')
    
    # fname = f'{os.path.dirname(f)}\\mod_{os.path.basename(f)}'    
    # file = open(fname, 'w')
    # file.writelines(lines)
    # file.close()
    
    # df = pd.read_csv(f,sep='?',header=None)
    # idx = df[0][df[0].str.match('#DateTime')].index[0]
    # df.loc[idx+1:,0] = df.loc[idx+1:,0].apply(lambda x: x.replace(search_for,replace_with))
    # # df.loc[:,0] = df.loc[:,0].apply(lambda x: x.replace(',','‚')) # unicode Single Low-9 Quotation Mark U+201A
    
    # fname = f'{os.path.dirname(f)}\\mod_{os.path.basename(f)}'
    
    # # df.to_csv(fname,header=False,index=False,encoding='utf-8-sig') 
    # # df.to_csv(fname,header=False,index=False, sep=',', quoting=csv.QUOTE_NONE, escapechar="") 
    # df.to_csv(fname,header=False,index=False,) 
    
