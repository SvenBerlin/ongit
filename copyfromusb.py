# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 09:37:51 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import os as os
import pandas as pd
import shutil as sh
import sys
import time
from datetime import datetime
import win32api
import glob as glob


def filestocopy(dest_folder=None,search_folder='',ftype='.csv',mode='latest',replace=False):
    """
    Kopiere Datei vom externen Speichermedium
    
    Das Script überprüft kontinuierlich die angeschlossenen Laufwerke auf einen 
    bestimmten Pfad und durchsucht diesen - wenn vorhanden - nach einem angegebenen
    Dateitypen. Es wird standardmäßig die zeitlich zuletzt erstellte Datei kopiert.
    Es kann durch den Benutzer jedoch auch bestimmt werden, welche Datei kopiert 
    werden soll
    
    Paratmeters
    ----
    search_folder: string
        Ordnerstruktur nach der in den angeschlossenen Laufwerken gesucht werden 
        soll
    ftype: string
        Dateityp nachdem gesucht werden soll
    dest_folder: string
        Zielordner, in welchen die Dateien letztlich kopiert werden
    mode: string
        Parameter zur Steuerung welche Datei kopiert werden soll
        "last" kopiert die zeitlich zuletzt erstellte Datei (default)
        "all" kopiert alle gefundenen Dateien im Ordner
        "today" kopiert alle heute erstellte Dateien
        Alternativ kann auch ein Zahlenwert eingeben werden, welcher eine Anzahl 
        an Dateien kopiert
        
    """
    if dest_folder is None:
        dest_folder = os.path.expanduser('~')+'\Desktop\copyto'
    counter = 0
    while True:    
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        counter += 1        
            
        for drive in drives:
            path = os.path.abspath(drive+search_folder)
            if os.path.exists(path):
                print('\rfound source folder', end = '\r')
                sys.stdout.write('\r' )
                files = glob.glob(path+'\*'+ftype)
                if files:
                    if not(os.path.exists(dest_folder)):
                        os.makedirs(dest_folder)
                        print('\nfolder {} created'.format(dest_folder))
                    dates = [datetime.strptime(time.ctime(os.path.getctime(x)),"%a %b %d %H:%M:%S %Y") for x in files]
                    df = pd.DataFrame({'files':files,'cdates':dates})
                    if mode=='latest':
                        copyfiles = df[df['cdates']==max(df['cdates'])]['files'].tolist()
                    elif mode=='all':
                        copyfiles=df['files'].tolist()
                    elif mode=='today':
                        copyfiles = df[df['cdates'].apply(lambda x:datetime.date(x))==datetime.now().date()]['files'].tolist()        
                    else: 
                        copyfiles = [files[-int(mode)]]
                    for file in copyfiles:
                        if not replace:
                            if not os.path.exists(dest_folder+'\\'+file.split('\\')[-1]):
                                sh.copy(file,dest_folder)
                                print('{} copied\n'.format(file))
                            else:
                                print('\rfile {} already copied'.format(file), end = '\r')
                                sys.stdout.write('\n' )
                        else:
                            sh.copy(file,dest_folder)
                            print('{} copied'.format(file))
                    while True:
                        if not os.path.exists(path):
                            break
            else:
                dots = '.'*(counter%6)
                spaces = ' '*(6-len(dots))
                print('\rSource folder not found{}'.format(dots+spaces), end = '\r')
        time.sleep(1)
        
if __name__ == '__main__':
       
    search_folder = r'verify\\results'
    dest_folder = None # default is Desktop\copyto
    ftype = '.csv'
    
    filestocopy(dest_folder,search_folder,ftype=ftype,mode='latest',replace=False)
    
    
    