# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 08:47:27 2018

@author: sbergmann

Copyright@Hach Lange GmbH 

Programm to convert MarcoPolo HWC files to devdata format

    Parser will create a new folder one step back from the mainfolder to store
    all processed hwc files

    Parameters
    ----------
    
    path:       absolute path of mainfolder that holds hwc files in subfolders

    Functions
    ---------
    
    MP_parse:   function to convert a MarcoPolo hwc file to devdata format

"""

import glob
import os as os
import os.path

def MP_parse(file, err_list):
    
    '''
        Parameters
        ----------
        
        file:       absolute path of the current file to convert
        
        fpath:      absolute path of the output file
        
        err_list:   list to store all files rised errors
    '''
   
    try:
        lines = [line.rstrip('\n') for line in open(file)]
        new_txt = []    
        for lin in lines:
            if lin == '#VAAxx,actVal':
                new_txt.append('#VAAxxx,actVal')
            elif lin == '#END':
                break
            else:
                new_txt.append(lin)
                
        hwcfile = open(file, 'w')        
        for nlin in new_txt:
            hwcfile.write("%s\n" % nlin)
        hwcfile.close()  
    except UnicodeDecodeError:
        print(file+' not readable') 
        err_list.append(file)
        
    return err_list


### main 
err_list =[]

folder = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\parsed'
files = glob.glob(folder+'\\*txt')
count = 1
for file in files:    
    print(str(count)+'/'+str(len(files)))
    
    MP_parse(file, err_list)
    count = count+1
print('----- all files parsed -----')
