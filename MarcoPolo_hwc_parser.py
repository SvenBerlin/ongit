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

def MP_parse(file, fpath, err_list):
    
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
            if lin == '[GENERAL]':
                new_txt.append('[General]')
                new_txt.append('#Type,actVal')
            elif '#Test' in lin:
                new_txt.append('[Hardware]')
                new_txt.append('#VAAxxx,name,actVal,NomVal,loTol,upTol,check,ResultString')
            elif lin == '[HARDWARE]':
                pass
            elif lin == '[CALADJUST]':
                new_txt.append('[Fi]')
                new_txt.append('#VAAxxx,name,actVal,NomVal,loTol,upTol,check,ResultString')
            elif lin == '[CALIBDATA]':
                new_txt.append('[ConfData]')
                new_txt.append('#VAAxxx,actVal')
            elif lin == '#END':
                break
            else:
                new_txt.append(lin)
                
        hwcfile = open(fpath, 'w')        
        for nlin in new_txt:
            hwcfile.write("%s\n" % nlin)
        hwcfile.close()  
    except UnicodeDecodeError:
        print(file+' not readable') 
        err_list.append(file)
        
    return err_list


### main 

path = os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\new')
copy_path = os.path.normpath(path + os.sep + os.pardir)+'\\parsed'
copy_path = path = os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten')

if not os.path.exists(copy_path):
    os.makedirs(copy_path)

folders = [subfolder[0] for subfolder in os.walk(path)][1:]
err_list=[]
count = 1
for folder in folders:
    try:
        file = glob.glob(folder + '\\*')[-1]
    except IndexError:
        err_list.append(folder)
        print(folder+' contains no files')
        pass
    
    print(str(count)+'/'+str(len(folders)))
    
    fpath = copy_path+'\\'+file.split('\\')[-1]

    MP_parse(file, fpath, err_list)
    count = count+1
print('----- all files parsed -----')
