# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:56:28 2021

@author: sbergmann
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
f = r'C:\Users\sbergmann\Desktop\LRP\Verschleppung_36mm_Warmup_20210428.csv'

df = pd.read_csv(f,sep=';')
df.columns = [x.replace(' ','') for x in df.columns]
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

x = df.Timestamp
y = df["EXT_LED1"]
dt = timedelta(minutes=1)
plt.scatter(x,y,s=3)
plt.xlim(df['Timestamp'][0]- dt,df['Timestamp'].iloc[-1]+ dt)
plt.grid()
