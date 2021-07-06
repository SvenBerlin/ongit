import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import glob as glob
import os as os
import time as time
import numpy as np
from datetime import datetime, timedelta


def merge_csv_2():
    csvs = glob.glob(r'C:\Users\sbergmann\Desktop\NITRO HALT\csv_out\*.csv')
    list_df = []
    for csv in csvs:
        # head, tail = ntpath.split(csv)
        # clean_csv = head + '\\clean\\clean_' + tail
        with open(csv, "r") as f:
            lines = f.readlines()
        i = 0
        for i, line in enumerate(lines):
            if '#DateTime' in line:
                break
        # print(skipped)
        df = pd.read_csv(csv, skiprows=i)
        # list_df.append(df)
    # df_merged = pd.concat(list_df)
    # df_observe = df_merged[["m_dext_m2_m1","m_dext_m3_m1","kNO2", "kNO3", "kNOX", "number_of_cycles","number_of_flashes_per_cycle","number_of_adc_readings_per_cycles","m_dext_m1_z1","m_dext_m2_z2","m_dext_m3_z3","wiper_log_valid","mainKey.1","end_position"]]
    # df_observe.to_csv(r'C:\Users\sbergmann\Desktop\NITRO HALT\observe.csv', index=False, sep=';', decimal=',')
    # df_merged.to_csv(r'C:\Users\sbergmann\Desktop\NITRO HALT\merged_all.csv', index=False, sep=';', decimal=',')
    return df




def update_line(ax, new_data):
    # ax.set_xdata(np.append(ax.get_xdata(), new_data[0]))
    # ax.set_ydata(np.append(ax.get_ydata(), new_data[1]))
    ax.set_xdata(new_data[0])
    ax.set_ydata(new_data[1])
    plt.draw()
    plt.show()

path = r'C:\Users\sbergmann\Desktop\LRP'
datei = glob.glob(r'C:\Users\sbergmann\Desktop\NITRO HALT\csv_out\*.csv')[-1]

fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()
ax.grid()
plt.ion()
plt.show()
last = 100
# 
dt = timedelta(minutes=2)
while True:
    # df = pd.read_csv(datei,)
    df = merge_csv_2()
    
    xcol = '#DateTime'
    ycol = 'mDExtM2_M1'
    y2col = 'FlashLampVoltage'
    x = pd.to_datetime(df[xcol])[-last:]
    y = df[ycol][-last:]
    y2 = df[y2col][-last:]
    ax.scatter(x,y,color='r',s=4, label=ycol)
    ax2.scatter(x,y2,color='b',s=4, label=y2col)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    # ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x),4), ',')))
    ax.set_xlabel(xcol)
    ax.set_ylabel(ycol)
    # ax.legend()
    
    ax.set_xlim(x.iloc[0]-dt, x.iloc[-1]+dt)
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))

    fig.canvas.draw()
    fig.canvas.flush_events()
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(5)
    # plt.pause(5)