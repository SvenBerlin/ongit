# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 08:28:21 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import os as os
import glob as glob
import pandas as pd
import devdata as dv
from shutil import copyfile


def copyFile(src,dst):
    for f in src:
        base = os.path.basename(f)
        copyfile(f,os.path.join(dst,base))

def getFiles(path, prefix, dtype='csv'):
    return glob.glob(f'{path}\\{prefix}*.{dtype}')

def readFiles(files):
    failures =[]
    df = pd.DataFrame()
    lenfiles = len(files)-1
    temp = pd.DataFrame()
    for n,f in enumerate(files):
        printProgressBar(n,lenfiles)
        try:
            temp = pd.concat([temp,dv.messung(f)])
        except IndexError:
            failures.append(f)
            print(f'Datei {os.path.basename(f)} konnte nicht eingelesen werden')
        if (n/100)%1 == 0:
            df = pd.concat([df,temp])
            temp = pd.DataFrame()
            # print('reset')
        
    df = pd.concat([df,temp])
    return df, failures

def listFilesInDir(path):
    return os.listdir(path)

def createBaseExtention(files):
    return '0'*(len(str(len(files)))+1)

def numerize(base,i):
    return (base+str(i+1))[-len(base):]

def extendName(num,file):
    return num+'_'+file

def changeName(num,name,ext):
    return num + '_' + name + ext

def changeFileNames(path,name = None):
    files = listFilesInDir(path)
    base = createBaseExtention(files)
    for i, file in enumerate(files):
        filenameWithoutExtention, ext= os.path.splitext(file)
        num = numerize(base,i)
        if name is None:
            new = extendName(num,file)
        else:
            new = changeName(num,name,ext)
        os.rename(os.path.join(path,file),os.path.join(path, new))

def addSuffix(fname):
    base = fname
    num = 1
    while os.path.isfile(fname):
        prefix='0{}'.format(num)[-2:]
        fname = "{0}_{2}{1}".format(*os.path.splitext(base) + (prefix,))
        num +=1
    return fname

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()