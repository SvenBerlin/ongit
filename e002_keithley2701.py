# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:30:35 2017

@author: jwykhoff

Copyright@Hach Lange GmbH Tue Jul 25 14:30:35 2017
"""
import messaufbau as ma
import pandas as pd
from datetime import datetime
import time
# out = r'C:\Users\sbergmann\Desktop\NitroLog'
sonden = {'Sonde1':[1,218],
          'Sonde2':[1,219],
          'Sonde3':[2,220],}
try:
    k1=ma.KEITHLEY2701()
    k1.connect()
    # h=k1.get_temperature(channel=220)
    #print('die Temperatur auf dem Sensor 110 in °C beträgt:')
    #print(h)
    #print('die Temperatur auf dem Sensor 109 in °C beträgt:')
    #print(k1.get_temperature(channel=109))
    print('\n Messung mit Ergebnistabelle:')
    n=1
    df = pd.DataFrame()
    t0 =datetime.now()
    while True:
        for s in sonden:
            h=k1.messung('Nitro_Temptest',sonden[s][0],s,channel=sonden[s][1])# initiales df
            h['actVal'] = float(h['actVal'][0].split(',')[0].split(' ')[0])
            # print(f'\r Messung #{n}, Zeit: {datetime.now()-t0}\t|{h["VAAxxx"][0]}\t|{h["DateTime"][0]}\t|{h["actVal"][0]}', end = '\r')
            # print(f'|{h["VAAxxx"][0]}\t|{h["DateTime"][0]}\t|{h["actVal"][0]}')
            df=pd.concat([df,h],ignore_index=True)
        print(f'''\r Messung #{n}, Zeit: {datetime.now()-t0}\t
              {df["name"].iloc[-3]}: {df["actVal"].iloc[-3]}\t
              {df["name"].iloc[-2]}: {df["actVal"].iloc[-2]}\t
              {df["name"].iloc[-1]}: {df["actVal"].iloc[-1]}\t
              ''', end = '\r')
        time.sleep(5)
        n+=1
    k1.disconnect()
finally:
    k1.disconnect()
    df.to_csv('templog.csv')
