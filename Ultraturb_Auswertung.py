# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:15:29 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
### MATPLOTLIB
'''
https://matplotlib.org/3.1.0/gallery/color/named_colors.html
'''

import pandas as pd
import glob as glob
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
#matplotlib.use('agg')

path = r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\Projekte\XQA006\Messungen\Messdurchgang_01'
files = glob.glob(path+'\*.csv')

df = pd.DataFrame()
for f in files:
    df = pd.concat([df,pd.read_csv(f)],ignore_index=True)
# df['DateTime'] = pd.to_datetime(df['DateTime'])

# bereiche = [(0.1,0.25),
#             (0.35, 0.65),
#             (0.85, 1.15),
#             (4.75, 5.25),
#             (9.5, 10.5),
#             (19, 20),
#             (20, 21),
#             (48, 52),
#             (95, 105),
#             (240, 260),
#             (490, 510),
#             (700, 800),
#             (900, 1100)] 
bereiche = [0.012, 0.5, 1.0, 5, 10, 19.5, 20.5, 50, 100, 250, 500, 750, 1000]

for step in bereiche:
    # temp = df[(df['actVal']>step[0]) &  df['actVal']<step[1]]
    temp = df[(df['actVal']>step*0.8) &  (df['actVal']<step*1.2)]
    temp.reset_index(drop=True, inplace=True)
    
    mydpi=96
    fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
    for sn in temp['SN'].unique().tolist():
        if sn in [2007743,2007746]:
            linstyle = 'solid'
        else:
            linstyle = 'dotted'
        # ax2 = ax1.twinx()
        # ax1.plot(temp[temp['SN']==sn]['DateTime'],temp[df['SN']==sn]['actVal'], label=sn)#,color='mediumseagreen')
        ax1.plot(temp[temp['SN']==sn]['actVal'], linestylelabel=sn)#,color='mediumseagreen')
        # ax1.plot(temp[temp['SN']==sn]['DateTime'],temp[temp['SN']==sn]['actVal'], label=sn)#,color='mediumseagreen')
        # lns1 = ax1.plot(df[cols[0]], label=cols[0].split(';')[0],color='mediumseagreen')
        # lns2 = ax2.plot(df[cols[1]], label=cols[1].split(';')[0],color='steelblue')
        # lns3 = ax2.plot(df[cols[2]], label=cols[2].split(';')[0],color='firebrick')
        
        ax1.set_xlabel('Datum')
        ax1.set_ylabel('{} ({})'.format(temp['Groesse'].iloc[0],temp['Einheit'].iloc[0]))
        # ax2.set_ylabel(cols[1].split(';')[1]+'('+cols[1].split(';')[2]+')')
        
        # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
        # ax1.xaxis.set_tick_params(rotation=45)
        # ax1.set_xticks(temp.index, temp['DateTime'])
        #    ax1.set_aspect('equal')
        #    ax1.locator_params(axis='y',tight=True,nbins=10)
        # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
        # ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
        #    ax2.locator_params(axis='y', nbins=10)
        #    ax2.locator_params(axis='x', nbins=10)
        ax1.set_title('Ultraturb LED Verifikation - 1. Durchgang - {} FNU'.format(str(step)))
        ax1.grid(True)
        # lns = lns1+lns2+lns3
        # labs = [l.get_label() for l in lns]
        # ax1.legend(lns, labs, loc=0)
        ax1.legend()
        
    ax1.set_xticklabels(temp[temp['SN']==sn]['DateTime'])
    fname = 'Ultraturb LED Verifikation - 1. Durchgang - {} FNU'.format(str(step))
    fig.savefig(fname+'.jpg')
    plt.close()
# pickle.dump(fig, open(r'plots\\'+fname+'.fig.pickle', 'wb'),protocol=1)