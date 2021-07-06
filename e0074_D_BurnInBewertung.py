# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 08:38:29 2019

author: Jan Wykhoff, Sven Bergmann
copyright@HACH LANGE GmbH 2019
For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""
import sys
import os as os
pythonpaths = [os.path.abspath(r'C:\Users\Public\Documents\Python Scripts\forpythonpath'),
               os.path.abspath(r'C:\ProgramData\Anaconda3'),
               os.path.abspath(r'C:\ProgramData\Anaconda3\Scripts'),
               os.path.abspath(r'C:\ProgramData\Anaconda3\Library\bin')]
for path in pythonpaths:
    try:
        sys.path.index(path) # Or os.getcwd() for this directory
    except ValueError:
        print(path+' wurde den Umgebungsvariablen hinzugefügt')
        sys.path.append(path)

import numpy as np
import shutil as sh
import glob as glob
import pandas as pd
import time as time
import ctypes  # An included library with Python install.   
#eigene Pakete:
import devdata as dv

import warnings
warnings.filterwarnings("ignore")

path_to_watch= os.path.abspath(r'C:\Users\Public\Documents\Doughnut_BurnIn_Laserteam') #Leseordner
zielpfad=os.path.abspath(r'C:\Users\Public\Documents\Doughnut_BurnIn_Laserteam\zumMontageordner')
zielpfaddefect=os.path.join(zielpfad,r'defect')
minimaleAnzahlDerMessungen=1000 # tbd: anpassen an plausible länge der Messdatei
if not( os.path.exists(path_to_watch) ):
    os.makedirs(path_to_watch)
if not( os.path.exists(zielpfad) ):
    os.makedirs(zielpfad)   
if not( os.path.exists(zielpfaddefect) ):
    os.makedirs(zielpfaddefect)       

def _write_df(df, file):
    '''
    speicher DataFrame als csv
    
    Ein DataFrame wird in einem Zielpfad abgespeichert ohne eine eventuell mit selben Dateinamen
    vorhandene csv Datei zu überschreiben
    
    Parameter
    ----
    df: DataFrame
        DataFrame die als csv-Datei abzuspeichern ist
    file: string
        Pfadname der zu speichernden csv-Datei
        
    Ausgabe
    ----
    string
        Pfadname der Zieldatei
    '''
    zieldatei=os.path.abspath(file)
    i=0
    while os.path.exists(zieldatei):
        h=zieldatei
        zieldatei=os.path.abspath(zieldatei+str(i))
        i=i+1
        #print('Die Datei '+h+' existiert bereits. Sie wird unter folgendem Namen abgespeichert: '+zieldatei+'.')
    df.to_csv(zieldatei,index=False)
    return(zieldatei)
def _move(file, zielpfad):
    '''
    verschiebe Datei
    
    Es wird eine Datei an einen anderen Ort verschoben
    
    Parameter
    ----
    file: string
        Pfadname der zu verschiebenden Datei
    zielpfad: string
        Pfadname des neuen Speicherortes    
    
    Ausgabe
    ----
    string
        Pfadname der Zieldatei
    '''
    zieldatei=os.path.join(zielpfad,os.path.basename(file))
    i=0
    while os.path.exists(zieldatei):
        h=zieldatei
        zieldatei=os.path.abspath(zielpfad+r'\\'+os.path.basename(file)+str(i))
        i=i+1
        #print('Die Datei '+h+' existiert bereits. Sie wird unter folgendem Namen abgespeichert: '+zieldatei+'.')
    sh.move(file,zieldatei)
    return(zieldatei)
def _fail_ok(x):
    '''
    Erstelle Ergebnistext
    
    Es wird ein string als Ergebnistest erstellt, basierend auf ein booleschen 
    Eingangswert. 
    
    Parameter
    ----
    x: bool
        Entweder True oder False
    
    Ausgabe
    ----
    string
        {fail,ok}
    '''
    if x:
        out= 'fail'
    else:
        out= 'ok'
    return(out)
def _burninauswertung(file, zielpfad):
    '''
    werte eine Doughnut BurnIn Datei aus
    
    Die übergebene Datei wird als DataFrame eingelesen und hinsichtlich
    TURBMEAS_REF_NAMPERE ausgewertet.  Als bestanden gilt die Auswertung, wenn 
    die Veränderung zum Anfangswert über die gesamte Messzeit innerhalb von
    loTol und upTol liegt.
    
    Parameter
    ----
    file: string
        Pfadname zur auszuwertenden Datei 
        (z.B.: VRFY_LXG445.99.B2112_AU1874433_SN1874433_20190215_1846.csv)
    zielpfad: string
        Pfadname des Speicherorts nach bestandener Auswertung
    
    Ausgabe
    ----
    bool
        {True,False}
    
    Funktionen
    ----
    dv.messung liest eine Datei als DataFrame ein (Teil des Pakets devdata)
    '''
    df=dv.messung(file,typ='D_Pr_BurnIn')
    df=df[['block','Type','actVal','datei','sn','DateTime','id','name',
           'redline','VAAxxx','Unit','Dateityp','Register',
           'TURBMEAS_REF_NAMPERE']]
    ref=df[df['block']=='Log']['TURBMEAS_REF_NAMPERE'].get_values()
    startref=ref[0]
    intensity = ref / startref *100 # in Prozent
    loTol= 80
    upTol= 120
    NomVal= 100
    totalevaluation= 'FAIL'
    intarray=intensity[~np.isnan(intensity)]
    if (intarray.min()<loTol)&(len(intarray)>minimaleAnzahlDerMessungen):
        check = False
    else:
        totalevaluation= 'OK'
        check = True
    #ergebniss: bewertungsdatei
    h=df[df['block']=='Log']
    h['intensity']= intensity
    h['loTol']= loTol
    h['upTol']= upTol
    h['NomVal']=NomVal
    h['check']= h['intensity']<loTol
    h['check']=h['check'].apply(lambda x: _fail_ok(x))
    h.index=range(len(h.index))
    header=df[df['block']=='Header']
    h2=header[header['Type']=='DevName']
    h2['Type']= 'Total evaluation'
    h2['actVal']= totalevaluation
    h2['redline']=np.nan
    h2.index=range(len(h2.index))
    out=h2.merge(h,how='outer')
    bewertungsdatei=os.path.abspath(os.path.dirname(file)+r'\\BurnIn_'+os.path.basename(file))
    bewertungsdatei= _write_df(out, bewertungsdatei)
    _move(bewertungsdatei, zielpfad)
    _move(file, zielpfad)
    return check

def _is_locked(files):
    '''
    Prüfe ob Dateien abgeschlossen sind
    
    Zunächst werden alle in der Liste files übergebenen Dateien überprüft, ob sich
    innerhalb von 60s die Dateigrößen verändert haben.  Wenn nicht, wird anschließend 
    versucht die ersten 8 Zeichen der Dateien im Lese- und Schreibmodus zu öffnen um 
    sicherzustellen das die Datei geschlossen ist.
    
    Parameter
    ----
    files: list
        enthält alle zu überprüfende Dateipfade
    
    Ausgabe
    ----
    bool
        {True,False}
    '''
    file_object = None
    ''' ERGÄNZUNG
    Datei wird zwar bereits zu Beginn erstellt, jedoch immer wieder geöffnet und erweitert
    --> einfacher Test ob Datei geöffnet reicht nicht aus, daher: teste ob Datei sich 
    in ihrer Größe ändert
    '''
    df = pd.DataFrame({'files':files,'locked':True,'exists':None, 'size':0})
    df['exists']=df['files'].apply(lambda x:os.path.exists(x))
#    df[df['exists'] == True]['size']=df['files'].apply(lambda x:os.stat(x).st_size)
    df['size']=df['files'].apply(lambda x:os.stat(x).st_size)
    print('Teste in 60 Sekunden ob Datei sich verändert hat und der BurnIn beendet ist...')
    time.sleep(60)
    for idx, row in df[df['exists'] == True].iterrows():
        if os.stat(df.loc[idx,'files']).st_size != df.loc[idx,'size']:            
            df.loc[idx,'size']=os.stat(df.loc[idx,'files']).st_size
        else:
            #QUELLE: https://www.calazan.com/how-to-check-if-a-file-is-locked-in-python/
            """Checks if a file is locked by opening it in append mode.
            If no exception thrown, then the file is not locked.
            """
            try:
                buffer_size = 8
                # Opening file in append mode and read the first 8 characters.
                file_object = open(df.loc[idx,'files'], 'a', buffer_size)
                if file_object:
                    df.loc[idx,'locked']=False
            except IOError:
               text='--- Datei '+os.path.basename(df.loc[idx,'files'])+' nicht geschlossen ---'
               ctypes.windll.user32.MessageBoxW(0, text, text, 0x30)# 0x03: Ausrufezeichen im gelben Warndreieck.
            finally:
                if file_object:
                    file_object.close()
    if len(df[df['locked']==False]) == len(df):
        locked = False
    else:
        locked = True
    return locked
    
def main(path_to_watch, basenamepattern):
    '''
    überwache Ordner auf neue Doughnut BurnIn Dateien
    
    Solange main läuft, wird der zu überwachende Ordner auf neue Doughnut
    BurnIn Dateien überprüft.
    
    Parameter
    ----
    path_to_watch: string
        Pfadname des Ordner der überwacht werden soll
    basenamepattern: string
        Text in Form eines Teils des Dateinamen der in den Dateien enthalten 
        sein muss, damit die Dateien als relevant erkannt werden
    
    Ausgabe
    ----
    done
    '''
    while 1:
        files = glob.glob(path_to_watch+r'\\*.csv')
        if files:
            if not _is_locked(files): #Teste ob Dateien gelocked sind
                text = 'Anzahl der Geräte: '+str(len(files))+'\n\nSeriennummer\tResult\n--------------------------------\n'
                for file in files:
                    if file.find(basenamepattern)>-1:       
                        try:
                            if _burninauswertung(file, zielpfad):
                                text = text+file.split('_')[-3][2:]+'\t\tgut\n'
                            else:
                                text = text+file.split('_')[-3][2:]+'\t\tschlecht\n'
                        except:
                            text = text+file.split('_')[-3][2:]+'\t\tdefekt\n'                        
                            _move(file, zielpfaddefect)
                if ('schlecht' in text) or ('defekt' in text):
                    text = text+'\n\n\n-------- Bitte R&D benachrichtigen! --------'
                ctypes.windll.user32.MessageBoxW(0, text, 'BurnIn Results', 0x30)
                print('Dateien abgearbeitet. Warte nun auf neue Dateien....\n Bei Wunsch, kann dieses Programm VAPx geschlossen werden.')
        else:
            print('Warte auf neue Dateien....')
            time.sleep(5)
    return('done')
if __name__ == "__main__":
    main(path_to_watch, 'VRFY_LXG445')


'''
Notiz:
    Ausgliedern der Schleifen?
    Laufwerk H
    Grenzen/Toleranzen
    MessageBox anpassen
    Doppelstarts: flag setzen?
'''

