# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 09:30:35 2018

@author: sbergmann
Script zum erstellen von Pseudo-HWC/FI Daten
Copyright@Hach Lange GmbH 
"""

import random
import datetime

path = r'C:\Users\sbergmann\Desktop\python_test\hwc_'
num_files = 100 # Anzahl der zu erzeugenden Files
num_data = 100 #Anzahl der Datensätze pro File
header = 'DateTime,VAAxxx,ActVal,SN,Type'
sn = random.randint(100000,200000)
time = datetime.datetime.now()
for i in range(num_files):
    new_csv = []
    new_csv.append(header)
    sn = sn+1
    time = time+datetime.timedelta(0,random.randint(300,1000))
    time_str = str(time).replace(':','').replace('-','').replace(' ','_').split('.')[0]
    typ = random.randint(0,2)
    if typ == 0 or typ == 1:
        typ = 'EPA'
    else:
        typ = 'ISO'
    for j in range(num_data):
        time = time + datetime.timedelta(0,random.randint(40,100))
        row = str(time)+','+str(j+1)+','+str(random.uniform(0,1)*10)+','+str(sn)+','+typ
        new_csv.append(row)    
    hwcfile = open(path+'\\hwc_'+str(sn)+'_'+time_str+'.csv', 'w')        
    for nlin in new_csv:
        hwcfile.write("%s\n" % nlin)
    hwcfile.close() 