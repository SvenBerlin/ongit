# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 10:29:13 2021

@author: sbergmann
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


file = r'C:\Users\sbergmann\Desktop\NITRO HALT\csv_out\HALT_LXG448.99.12000_SN30151934_210629_103807.csv'
file = r'C:\Users\sbergmann\Desktop\NITRO HALT\csv_out\HALT_LXG448.99.12000_SN30151934_210629_152952.csv'

with open(file, "r") as f:
    lines = f.readlines()
i = 0
for i, line in enumerate(lines):
    if '#DateTime' in line:
        break
# print(skipped)
df = pd.read_csv(file, skiprows=i)
df['#DateTime'] = pd.to_datetime(df['#DateTime'])
df = df[df['#DateTime']>datetime(2021,6,29,10,52)]
df['Date'] = df['#DateTime'].apply(lambda x: x.strftime('%d.%m.%Y'))
df['Time'] = df['#DateTime'].apply(lambda x: x.strftime('%I:%M:%S %p'))

df.to_csv('cropped_data.csv', index=False)

chamber = r'C:\Users\sbergmann\Desktop\NITRO HALT\chambers_log.xlsx'
df_ch = pd.read_excel(chamber)
# df['Time'] = df['#DateTime'].apply(lambda x: x.strftime('%I:%M:%S %p'))
df['Time'] = pd.to_datetime(df.Time,format='%H:%M:%S %p').dt.time
df_ch['#DateTime'] = 0
df_ch['#DateTime'] = df_ch['Time'].apply(lambda x: datetime.combine(datetime(2021,6,29),x))


mydpi = 96
fig, ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
lns1 = ax.plot(df_ch['#DateTime'],df_ch['Vib Setpoint G'], label= 'Vib Setpoint G')
ax2 = ax.twinx()
lns2 = ax2.plot(df_ch['#DateTime'],df_ch['Product Temp °C'], alpha=.75,color='r',label= 'Product Temp °C')
ax3 = ax.twinx()
lns3 = ax3.plot(df['#DateTime'],df['FlashLampVoltage'],alpha=1,color='g',label= 'FlashLampVoltage')
ax3.scatter(df['#DateTime'],df['FlashLampVoltage'], s=2,alpha=.75,color='g',label= 'FlashLampVoltage')
ax3.spines["right"].set_position(("axes", 1.05))
ax3.spines["right"].set_visible(True)
ax3.set_ylabel('FlashLampVoltage (V)')
ax4 = ax.twinx()
lns4 = ax4.plot(df['#DateTime'],df['mDExtM2_M1'], alpha=1,color='k',label= 'mDExtM2_M1')
ax4.scatter(df['#DateTime'],df['mDExtM2_M1'],s=2, alpha=.75,color='k',label= 'mDExtM2_M1')
ax4.spines["right"].set_position(("axes", 1.1))
ax4.spines["right"].set_visible(True)
ax4.set_ylabel('mDExtM2_M1 (mE)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.set_xlabel('Time')
ax.set_ylabel('Vibration (g)')
ax2.set_ylabel('Temperature (°C)')
ax.set_title('NItro - Vibration HALT 29. June 2021')
ax.grid()
lns = lns1+lns2+lns3+lns4

labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)
lns3.pop(0).remove()
lns4.pop(0).remove()
plt.tight_layout()