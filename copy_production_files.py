# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:46:37 2018

@author: sbergmann

Copyright@Hach Lange GmbH 

Programm zum kopieren mehrer Dateitypen die zusammengehören (z.B. Produktionsdaten)

"""

import shutil
import glob as glob
import pandas as pd
import os as os
from datetime import datetime

def byserialnumber(lst, serials, keep=True):
    if keep:
        lst = lst[lst['sn'].isin(serials)]
    else:
        lst = lst[~lst['sn'].isin(serials)]
    return lst

def searchforfiles(dst, titles, amount, paths, ftypes=['csv'], rev=['all'], sn=[], keep=True):
    
    assert isinstance(dst,str), 'Zielpfad muss im Stringformat sein: %r' % dst
    assert isinstance(titles,list), 'Basisnamen müssen in einer Liste übergeben werden: %r' % titles
    for title in titles:
        assert isinstance(title,str), 'Basisname muss als String übergeben werden: %r' %title
    assert isinstance(amount,list), 'Anzahl der gewünschten Dateien muss in einer Liste übergeben werden: %r' % amount
    for a in amount:
        assert isinstance(a,int), 'Anzahl der gewünschten Dateien muss als integer übegeben werden: %r' % a
    assert isinstance(paths,list), 'Suchpfade müssen in einer Liste übergeben werden: %r' % paths
    for path in paths:
        assert isinstance(path,str), 'Suchpfad muss als String übergeben werden: %r' %path
    assert isinstance(ftypes,list), 'Gesuchte Dateitypen müssen in einer Liste übergeben werden: %r' % ftypes
    for ftype in ftypes:
        assert isinstance(ftype,str), 'Dateityp muss als String übergeben werden: %r' %ftype
    assert isinstance(sn,list), 'Gesuchte Seriennummern müssen in einer Liste übergeben werden: %r' % sn
    for s in sn:
        assert isinstance(s,str), 'Seriennummer muss als String im Format "SNxxxxxxx" übergeben werden: %r' %s
    assert isinstance(rev,list), 'Entscheidung wie mit Duplikaten umgegangen werden soll, muss in einer Liste übergeben werden: %r' % rev
    for r in rev:
        assert isinstance(r,str), 'Umgang mit Duplikaten muss im String vorliegen (Bsp: "all", "last"): %r' %r
    assert isinstance(keep, bool), 'Für die Entscheidung wie mit übergebenen Seriennummern umgegangen wird, muss ein bool übergeben werden: %r' % keep
    
    if len(titles) != len(paths):
        paths = paths*len(titles)
    if len(titles) != len(amount):
        amount = amount*len(titles)
    if len(titles) != len(ftypes):
        ftypes = ftypes*len(titles)
    if len(titles) != len(rev):
        rev = rev*len(titles)
    
    if len(sn)==0:
        sn = ['']*len(titles)

    df = pd.DataFrame({'Titles':titles,'Amounts':amount,'Types':ftypes,'Paths':paths,'Revs':rev})
    f2copy = pd.DataFrame()
    
    for num in range(len(df)):
        files = pd.DataFrame()
        files['path'] = glob.glob(df['Paths'].iloc[num]+df['Titles'].iloc[num]+'*.'+df['Types'].iloc[num])
        files['sn'] = [x.split('_')[-3] for x in files['path'].tolist()]
        files['datetime']=[datetime.strptime(s.split('_')[-2]+s.split('_')[-1].split('.')[0],'%Y%m%d%H%M') for s in files['path'].tolist()]
        files.sort_values(by=['sn'],inplace=True)
    
        if df['Revs'].iloc[num] != 'all':
            files.drop_duplicates(subset='sn',keep=df['Revs'].iloc[num],inplace=True)    
        files.reset_index(drop=True,inplace=True)
        files = byserialnumber(files,sn,keep=keep )
    
        f2copy = pd.concat([f2copy,files.iloc[df['Amounts'].iloc[num]:]],ignore_index=True)
    
    if not(os.path.exists(dst)):
        os.makedirs(dst)
    
    for src in list(f2copy['path']):
        shutil.copy(src,dst)
    
if __name__ == '__main__':

    dst = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Doughnut\18_FAST\GCS_Analyse_4Quartal_2018\Laser_Team\Verifikation\03_Drop, shock and vibration test\Serie' #Zielpfad: dorthin werden die Daten kopiert
    titles = ['HWC_LPG442.72.01012',
              'HWC_LPG442.72.01022',
              'LPG442.72.01012',
              'LPG442.72.01022']  #Liste mit Teil-Titelnamen zu Identifikation
    amount = [-20] #Liste mit der Anzahl der zu kopierenden Dateien (negativ, damit die letzten Dateien ausgewählt werden)
    ftypes = ['csv']   #Liste der Dateitypen
    paths = ['H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG442\\'] # Liste der Basispfade
    rev = ['all'] # Liste welche Dateien kopiert werden sollen, wenn Duplikate
    sn = ['SN1932303','SN1932374']
    keep = True
    
    searchforfiles(dst,titles,amount,paths,sn=sn)