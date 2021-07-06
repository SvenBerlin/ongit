# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:21:33 2018

Parser to extract HSI CALIB data and corrosponding temperature from PuTTy Log file

e.g.:
    
    47: HSI CALIB: F_before=15998156, F_after=15987507, CalibVal=16
    and
    45: get_uC_temperature temperature[degC]:50.8
    to Dataframe:
    F_before    F_after    CalibVal    temperature
    15998156    15987507    16          50.8
    …           …           …           …
    
    Saving as txt and plot as png file in same folder as PuTTy log file


@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import os as os
import os.path
import matplotlib.pyplot as plt
import pandas as pd

def HSI_Parse(file, fout, err_list):
    
    '''
        Parameters
        ----------
        
        file:       absolute path of the current file to convert
        
        fout:      absolute path of the output file
        
        err_list:   list to store all files rised errors
    '''
   
    try:
        lines = [line.rstrip('\n') for line in open(file)]
        new_txt = []
        new_txt.append('F before,F after,CalibVal,temperature')
        calib = 0
        for lin in lines:
            if 'HSI CALIB' in lin:
                for s in lin.split():
                    if 'before' in s:
                        fb = s.split('=')[-1][:-1]
                    if 'after' in s:
                        fa = s.split('=')[-1][:-1]
                    if 'CalibVal' in s:
                        calval = s.split('=')[-1]
                calib = fb+','+fa+','+calval+','
            if 'get_uC_temperature' in lin and calib!=0:
                temp = lin.split(':')[-1]
                new_line = calib+temp
                new_txt.append(new_line)
                calib = 0
              
        parsedfile = open(fout, 'w')        
        for nlin in new_txt:
            parsedfile.write("%s\n" % nlin)
        parsedfile.close()  
        df = pd.read_csv(fout)
    except UnicodeDecodeError:
        print(file+' not readable') 
        err_list.append(file)
        
    return df,err_list


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

### main 

file = os.path.abspath(r'C:\Users\sbergmann\Desktop\python_test\putty.log')
fout = file.split('.')[0]+'_parsed.log'
#fout = 'parsed_'+file.split('\\')[-1]

err_list=[]

df, err_list = HSI_parse(file, fout, err_list)



fig, ax = plt.subplots(figsize=(1920/96,1080/96))
par1 = ax.twinx()
par2 = ax.twinx()
par2.spines["right"].set_position(("axes", 1.05))
make_patch_spines_invisible(par2)
par2.spines["right"].set_visible(True)

p1, = ax.plot(df['F before'], color='blue', label='f before')
p2, = ax.plot(df['F after'], color='green', label='f after')
p3, = par1.plot(df['CalibVal'], 'r-.', alpha=.7, label='f CalibVal')
p4, = par2.plot(df['temperature'], 'k-.', alpha=.7, label='temperature')

ax.set_xlabel('#')
ax.set_ylabel('Frequency MHz')
par1.set_ylabel('CalibVal')
par2.set_ylabel('Temperature °C')

ax.grid()
lines = [p1,p2,p3,p4]
ax.legend(lines, [l.get_label() for l in lines])
ax.ticklabel_format(useOffset=False, axis='y') 
plt.tight_layout()
#fig.savefig(file.split('\\')[-1].split('.')[0]+'.png')
fig.savefig(fout.split('.')[0]+'.png')