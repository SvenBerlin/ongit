# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 08:10:50 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
from matplotlib.gridspec import GridSpec
import os

basenamepattern = 'VRFY_LXG445'
path = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG445\Script_BurnIn'
#path = r'C:\Users\Public\Documents\Doughnut_BurnIn_Laserteam\zumMontageordner\Test'
#path = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG3\LXG445\Script_BurnIn\ausgewertet'
#path = r'C:\Users\Public\Documents\Doughnut_BurnIn_Laserteam'
value = 'TURBMEAS_REF_NAMPERE'
tolerance = {'lTol':30,'uTol':420}

files = glob.glob(path+'\\'+basenamepattern+'*csv')

df = pd.DataFrame()
for num, file in enumerate(files):
    print('{}/{}: {}'.format(num+1,len(files),os.path.basename(file)))
    temp = pd.read_csv(file,skiprows=357)
    temp['SerialNumber'] = str(pd.read_csv(file,skiprows=7,nrows=1).iloc[0,1])
    temp['path'] = file
    df = pd.concat([df,temp],ignore_index=True)

df.DateTime = pd.to_datetime(df.DateTime)
for dev in df['SerialNumber'].unique().tolist():
    
    temp = df[df['SerialNumber']==dev]
    duration = max(temp['DateTime']) - min(temp['DateTime'])
    filename = temp['path'].iloc[0].split('.csv')[0]
    filename = value+filename[filename.find('_AU'):]
    count, mean, std, minval, q25, q50, q75, maxval= temp[value].describe()
    textstr = '\n'.join((
        r'$count=%.2f$' % (count, ),        
        r'$duration=%s$' % (str(duration) ),
        r'$range=%.2fnA$' % (maxval-minval, ),
        r'$mean=%.2fnA$' % (mean, ),
        r'$std=%.2fnA$' % (std, ),
        r'$min=%.2fnA$' % (minval, ),
        r'$max=%.2fnA$' % (maxval, )))
    mydpi=96
    fig = plt.figure(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
    gs = GridSpec(1,1)#
    ax =fig.add_subplot(gs[:,:])
    
    uTol = [tolerance['uTol']]*len(temp[value])
    lTol = [tolerance['lTol']]*len(temp[value])
    
    kwargs={'color':'k','linestyle':'-.','alpha':0.75}
    ax.plot(temp['DateTime'],temp[value])
    ax.plot(temp['DateTime'],uTol,**kwargs,label='uTol')
    ax.plot(temp['DateTime'],lTol,**kwargs,label='lTol')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax.grid(b=True)
    ax.set_xlabel('Date')
    ax.set_ylabel('nA')
    ax.set_title(value+' of '+dev)
    ax.legend()
    plt.tight_layout()
    
    plt.savefig(path+'\\'+filename+'.png')
    plt.close(fig)
    
    
    
