# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 09:05:58 2017

@author: sbergmann
"""

import socket as socket
import time as time
import datetime as datetime
import os as os
import sys as sys

#import glob as glob
import numpy as np
#import matplotlib as mpl
import pandas as pd #zentraler Datentyp für uns: das DataFrame.


def h1_ky_get_zeit(string):
    '''formatiere zu kruz geschriebene Zeitangabe um.
    bringe einen 1-elementigen string auf ein zwei-elementiges durch 
    voranstellen von '0'.

    Parameter
    ---------
    string
    
    Ausgabe
    -------
    string

    Beispiel
    --------
    >>> h1_fl_get_zeit('5')
    '05'
    '''
    out=string
    if len(string)==1:
        out='0'+string
    return(out)

def ky_get_zeit(s):
    '''liefer die zeit die im Flukegerät eingestellt ist.
      
    Parameter
    ---------
    s: socket.socket, m.a.W. Funktion des socket Moduls
    stellt den Zugriff auf das (Fkluke-)Gerät dar
    
    Ausgabe
    -------
    string
    Zeitangabe im (Doughnut-) Format dd.mm.yyyy HH:MM:SS
    '''
    #date:
    s.send('SYST:DATE?\n'.encode('utf-8'))
#    time.sleep(0.1)
    #(date,a1)=s.recvfrom(h1-1)
    (re2,a1)=s.recvfrom(256)#lese die mehrfache länge aus. Der gleiche Inhalt widederholt sich.
    h=re2.decode().split('\n')#schneide den ersten komplett gefundenen Eintrag heraus
    try:
        date=h[1]
    except:
        date=h[0]
    if date=='':#falls nur einen Eintrag gegeben wird, nehme diesen nullten.
        date=h[0]
    try:
        hds=date.split('/')
        date_dformatiert=h1_ky_get_zeit(hds[1])+'.'+h1_ky_get_zeit(hds[0])+'.'+h1_ky_get_zeit(hds[2])
    except:
        date_dformatiert=date
    #time:
    h2=s.send('SYST:TIME?\n'.encode('utf-8'))
    time.sleep(0.1)
    #(tim,a2)=s.recvfrom(h2-1)
    (tim2,a2)=s.recvfrom(256)#lese die mehrfache länge aus. Der gleiche Inhalt widederholt sich.
    h2=tim2.decode().split('\n')#schneide den ersten komplett gefundenen Eintrag heraus
    try:
        tim=h2[1]
    except:
        tim=h2[0]
    if tim=='':#falls nur einen Eintrag gegeben wird, nehme diesen nullten.
        tim=h2[0]
    #print(' '+tim[0:-2].decode())
    tstamp=date_dformatiert+' '+tim
    #print(tstamp)
    return(tstamp)

def ky_get_error(s):
    '''liefer den Fehlereintrag der im Flukegerät vorliegt.
    
    Parameter
    ---------
    s: socket.socket, m.a.W. Funktion des socket Moduls
        stellt den Zugriff auf das (Fkluke-)Gerät dar
    
    Ausgabe
    -------
    string
    '''
    #h2=s.send('*CLS;SYST:ERR?\n'.encode('utf-8'))
    #h1=s.send('*ESR?\n'.encode('utf-8'))
    #time.sleep(0.1)
    #(re1,a1)=s.recvfrom(h1)
    s.send('SYST:ERR?\n'.encode('utf-8'))
    time.sleep(0.1)#warte um keinen Fehler zu erzeugen
    (re2,a2)=s.recvfrom(256)#lese die mehrfache länge aus. Der gleiche Inhalt widederholt sich.
    h=re2.decode().split('\r\n')#schneide den ersten komplett gefundenen Eintrag heraus
    try:
        out=h[1]
    except:
        out=h[0]
    if out=='':#falls nur einen Eintrag gegeben wird, nehme diesen nullten.
        out=h[0]
    s.send('*CLS\n'.encode('utf-8'))#setze die Fehlermeldung zurück
    #return((out,re2,a2))#debugging
    #err,re,a)=fl_get_error(s);print(err);print(re);print(a)
    return(out)

def ky_get_volt(s,mode):
    '''liefer eine Einzelmessung der Spannung die am Flukegerät gemessen wird.
           
    Parameter
    ---------
    s: socket.socket, m.a.W. Funktion des socket Moduls
        stellt den Zugriff auf das (Fkluke-)Gerät dar
    mode: string
        'init','full','trigg', default ist 'full'
    
    Ausgabe
    -------
    string
    '''
    #Einzelmessung der DC-Spannung  im 10V-Range
    out='NaN'
    if mode=='full':
        h2=s.send('CONF:VOLT 3;:TRIG:SOUR BUS;:INIT;*TRG;FETCH?\n'.encode('utf-8'))
        time.sleep(0.1)
        (re,a2)=s.recvfrom(h2-1)
        out=re.decode().split('\r\n')[0]
    if mode=='trigg':
        h2=s.send(':TRIG:SOUR BUS;:INIT;*TRG;FETCH?\n'.encode('utf-8'))
        time.sleep(0.1)
        (re,a2)=s.recvfrom(h2-1)
        out=re.decode().split('\r\n')[0]
    if out=='':
        out='NaN'
    if mode=='init':
        h2=s.send('CONF:VOLT 3;:TRIG:SOUR BUS;:INIT\n'.encode('utf-8'))
        out='NaN'
    return(out)

def ky_get_temp(s):
    s.send('INIT:CONT OFF;\n'.encode('utf-8'))
    time.sleep(0.2)
    s.send("FUNC 'TEMP';\n".encode('utf-8'))
    time.sleep(0.2)
    s.send('TEMP:FRTD:TYPE PT100;\n'.encode('utf-8'))
    time.sleep(0.2)
    s.send('ROUT:CLOS (@102);\n'.encode('utf-8'))
    time.sleep(0.2)
    s.send('INIT;\n'.encode('utf-8'))
    time.sleep(0.2)
    s.send('READ?;\n'.encode('utf-8'))
    time.sleep(0.2)
    (temp,a1)=s.recvfrom(256)
    h=temp.decode().split('\r\n')
    out=h[0]
    return(out)

def ky_messung(s,VAA,Register):
    '''messung aus zeit, typ, VAA,volt, fehlereintrag, Register'''
    zeit=ky_get_zeit(s);print(zeit)
    zeit=datetime.datetime.strptime(zeit, '%Y,%m,%d %H,%M,%S.%f')
    time.sleep(0.1)
    typ='keithley2701Multimeter'
    #VAA='Nullmessung'
    temp=ky_get_temp(s);print(temp)
    time.sleep(0.1)
    err=ky_get_error(s);print(err)
    s.send('*CLS\n'.encode('utf-8'))#setze (noch einmal) die Fehlermeldung zurück
    time.sleep(0.1)
    #df=pd.DataFrame({'time':zeit,'typ':typ,'VAA':VAA,'actVal':'time':zeit,'typ':typ,'VAA':VAA,'actVal':volt,'unit':'V','check':err,'unit':'V','check':err},index=[1])
    dat=[typ,VAA,zeit,temp,'C',err,Register]
    cols=['Type','VAAxxx','DateTime','actVal','Unit','check','Register']
    df=pd.DataFrame(data=dat).T
    df.columns=cols
    return(df)

PORT = 1394              # The same port as used by the server
s16 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s16.connect(('192.168.8.2', PORT))
s16.send('SYST:BEEP;*RST\n'.encode('utf-8'))
s16.send('*CLS\n'.encode('utf-8'))#setze (noch einmal) die Fehlermeldung zurück
#time.sleep(1)
#s16.send("FUNC 'TEMP';\n".encode('utf-8'))
#time.sleep(0.2)
#s16.send('TEMP:FRTD:TYPE PT100;\n'.encode('utf-8'))
#time.sleep(0.2)
#s16.send('ROUT:CLOS (@102);\n'.encode('utf-8'))
#time.sleep(0.2)
#s16.send('INIT;\n'.encode('utf-8'))
#time.sleep(0.2)
#s16.send('READ?;\n'.encode('utf-8'))
#time.sleep(0.2)

time.sleep(0.2)
df_all=pd.DataFrame()
time.sleep(0)#zeit um vor messbegin den Raum zu verdunkeln und zu verlassen
intervall=5.0#s zwischen zwei Messpaaren
messzeit=0.3#in Minuten
#s16.send("*RST;\n".encode('utf-8'))
#time.sleep(0.2)
for i in range(int(messzeit*np.ceil(60/intervall))):
    #i=0
    try:
        df=ky_messung(s16,'leer_Ref',i);
        df_all = pd.concat([df_all, df])
    except:
        print('Problem im Schritt i = '+str(i)+'.')
    time.sleep(int(intervall))#1 sekunde
#df=fl_messung(s,'leerer2mmChip_00xoomm');df_all = pd.concat([df_all, df])
#df=fl_messung(s,'leerer2mmChip_11xoomm');df_all = pd.concat([df_all, df])
#df=fl_messung(s,'leer_dark');df_all = pd.concat([df_all, df])
#df=fl_messung(s,'Nullmessung');df_all = pd.concat([df_all, df])
#df=fl_messung(s,'fc_blue_100');df_all = pd.concat([df_all, df])
time.sleep(0.2)
df_all['actVal']=df_all['actVal'].astype(float,copy=True)
df_all.index=range(len(df_all.index))
zielordner=r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\python\fluke8846A\keithley2701'
zieldatei=r'test_'+time.strftime('%Y%m%d_%H%M%S')+'.xlsx'
df_all.to_excel(os.path.join(zielordner,zieldatei))











