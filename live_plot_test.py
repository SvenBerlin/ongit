'''
pythonprogramming.net/live-graphs-matplotlib-tutorial/
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates
from matplotlib import rcParams
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

mydpi=96
fig = plt.figure(figsize=(1200/mydpi,800/mydpi),dpi=mydpi,)
ax1 = fig.add_subplot(1,1,1,)

def animate(i):
    df = pd.read_csv('raw.csv')
    df['DateTime']=pd.to_datetime(df['DateTime'])

    for sn in df['SN'].unique().tolist():
        temp = df[df['SN']==sn]
        ax1.clear()
        ax1.plot(temp['DateTime'],temp['actVal'],label=sn)
        ax1.grid()
        ax1.set_xlabel('DateTime')
        ax1.set_ylabel('turbidity FNU')
        ax1.legend()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
        ax1.xaxis.set_tick_params(rotation=90)
        ax1.set_ylim(min(temp['actVal'])*0.9,max(temp['actVal'])*1.1)
        # ax1.xaxis_date()
        # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
        plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()