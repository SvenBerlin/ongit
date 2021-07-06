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
import glob as glob

global file
file = [x for x in glob.glob('*.csv') if 'Ultraturb' in x.split('_')][-1]

mydpi=96
fig = plt.figure(figsize=(1200/mydpi,800/mydpi),dpi=mydpi,)
ax1 = fig.add_subplot(1,1,1,)

def animate(i):
    df = pd.read_csv(file)
    df['DateTime']=pd.to_datetime(df['DateTime'])
    df['SN']=df['SN'].apply(lambda x: str(x))

    ax1.clear()
    for sn in df['SN'].unique().tolist():
        temp = df[df['SN']==sn]
        ax1.plot(temp['DateTime'],temp['actVal'],label=sn)
        ax1.grid(True)
        ax1.set_title('Ultraturb LED Verifikation')
        ax1.set_xlabel('DateTime')
        ax1.set_ylabel('Trübung FNU')
        ax1.legend()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
        ax1.xaxis.set_tick_params(rotation=90)
        ax1.set_ylim(min(df['actVal'])*0.9,max(df['actVal'])*1.1)
        # ax1.xaxis_date()
        # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
        plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()