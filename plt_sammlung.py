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

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
#matplotlib.use('agg')

mydpi=96
fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
ax2 = ax1.twinx()
lns1 = ax1.plot(df[cols[0]], label=cols[0].split(';')[0],color='mediumseagreen')
lns2 = ax2.plot(df[cols[1]], label=cols[1].split(';')[0],color='steelblue')
lns3 = ax2.plot(df[cols[2]], label=cols[2].split(';')[0],color='firebrick')

ax1.set_xlabel('Datum')
ax1.set_ylabel(cols[0].split(';')[1]+'('+cols[1].split(';')[2]+')')
ax2.set_ylabel(cols[1].split(';')[1]+'('+cols[1].split(';')[2]+')')

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
ax1.xaxis.set_tick_params(rotation=90)
#    ax1.set_aspect('equal')
#    ax1.locator_params(axis='y',tight=True,nbins=10)
ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
#    ax2.locator_params(axis='y', nbins=10)
#    ax2.locator_params(axis='x', nbins=10)
ax1.set_title(title)
ax1.grid()
lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc=0)
fname = 'Nitratax - Wassmannsdorf_vom_{}_bis_{}'.format(datetime.strftime(df.index[0], '%Y%m%d'),datetime.strftime(df.index[-1], '%Y%m%d'))
fig.savefig(r'plots\\'+fname+'.jpg')
pickle.dump(fig, open(r'plots\\'+fname+'.fig.pickle', 'wb'),protocol=1)