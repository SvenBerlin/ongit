# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:24:17 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import os as os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import glob as glob
import devdata as dv
from datetime import datetime


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def read_data(path):
    files = glob.glob(path+'\LPG*.csv')
    lenfiles = len(files)
    df = pd.DataFrame(columns=['sn', 'datetime','level','temp','check','check_nom','check_utol','check_otol'])
    for n,f in enumerate(files):
        try:
            printProgressBar(n, lenfiles)
            h = pd.read_csv(f,usecols=[1,7,8,9,10])
            # h = pd.read_csv(f, sep='?')
            temp = pd.DataFrame({'sn':[os.path.basename(f).split('.c')[0].split('_')[1]], 
                                 'datetime':[datetime.strptime('_'.join([os.path.basename(f).split('.c')[0].split('_')[2],
                                    os.path.basename(f).split('.c')[0].split('_')[3]]),'%Y%m%d_%H%M')],
                                 'level':[float(h[h.iloc[:,0]=='RoundCuvetteLevel'].values[0][1])],
                                 'temp':[float(h[h.iloc[:,0]=='RoundCuvetteTemp'].values[0][1])],
                                 'check':[float(h[h.iloc[:,0]=='CuvetteCheck'].values[0][1])],
                                 'check_nom':[float(h[h.iloc[:,0]=='CuvetteCheck'].values[0][2])],
                                 'check_utol':[float(h[h.iloc[:,0]=='CuvetteCheck'].values[0][3])],
                                 'check_otol':[float(h[h.iloc[:,0]=='CuvetteCheck'].values[0][4])],
                                 })
            # level39.append(float(df[df.iloc[:,1]=='RoundCuvetteLevel'].values[0][7]))
            # h = dv.messung(f)
            # level39.append(float(h[h['VAAxxx']==vaa[0]]['actVal'].values[0]))
            df = pd.concat([df,temp])
        except:
            pass
    return df

# def read_data(path):
#     files = glob.glob(path+'\LPG*.csv')
#     lenfiles = len(files)
#     df = pd.DataFrame(columns=['sn', 'datetime','level','temp'])
#     for n,f in enumerate(files):
#         try:
#             printProgressBar(n, lenfiles)
#             h = pd.read_csv(f,usecols=[1,7])
#             # h = pd.read_csv(f, sep='?')
#             temp = pd.DataFrame({'sn':[os.path.basename(f).split('.c')[0].split('_')[1]], 
#                                  'datetime':[datetime.strptime('_'.join([os.path.basename(f).split('.c')[0].split('_')[2],
#                                                      os.path.basename(f).split('.c')[0].split('_')[3]]),'%Y%m%d_%H%M')],
#                                  'level':[float(h[h.iloc[:,0]=='RoundCuvetteLevel'].values[0][1])],
#                                  'temp':[float(h[h.iloc[:,0]=='RoundCuvetteTemp'].values[0][1])]})
#             # level39.append(float(df[df.iloc[:,1]=='RoundCuvetteLevel'].values[0][7]))
#             # h = dv.messung(f)
#             # level39.append(float(h[h['VAAxxx']==vaa[0]]['actVal'].values[0]))
#             df = pd.concat([df,temp])
#         except:
#             pass
#     return df
    

dr3900 = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG440'
df39 = read_data(dr3900)
dr6000 = r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441'
df60 = read_data(dr6000)

dr6000 = [r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441\Archiv\2015',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441\Archiv\2016',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441\Archiv\2017',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441\Archiv\2018',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441\Archiv\2019',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG441']
dr3900 = [r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG440\Archiv\2015',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG440\Archiv\2016',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG440\Archiv\2017',
          r'H:\WORKGROUP\Montage\PublicGroup\GERAET\IMG\PG2\LPG440']

df60 = pd.DataFrame()
for path in dr6000:
    df60 = pd.concat([df60,read_data(path)])

df39 = pd.DataFrame()
for path in dr3900:
    df39 = pd.concat([df39,read_data(path)])

def plot_data(df, title,year=None):
    if year is not None:
        df = df[df['datetime']>datetime(year,1,1)]
    df.sort_values(by='datetime',inplace=True,)# ignore_index=True) 
    mydpi=96
    fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
    ax2 = ax1.twinx()
    lns1 = ax1.scatter(df['datetime'],df["level"], label="RoundCuvetteLevel",color='mediumseagreen')
    lns2 = ax2.scatter(df['datetime'],df["temp"], label="RoundCuvetteTemp",color='steelblue')
    
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('RoundCuvetteLevel (V)')
    ax2.set_ylabel('RoundCuvetteTemp (°C)')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
    ax1.xaxis.set_tick_params(rotation=45)
    #    ax1.set_aspect('equal')
    #    ax1.locator_params(axis='y',tight=True,nbins=10)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax2.xaxis.set_major_locator(plt.MaxNLocator(20))
    #    ax2.locator_params(axis='y', nbins=10)
    #    ax2.locator_params(axis='x', nbins=10)
    ax1.set_title(title)
    ax1.grid()
    # lns = lns1+lns2
    # labs = [l.get_label() for l in lns]
    # ax1.legend(lns, labs, loc=0)
    fig.legend()
    # ax1.legend()
    fname = '{}_level_temp_{}_bis_{}'.format(title,datetime.strftime(min(df.datetime), '%Y%m%d'),datetime.strftime(max(df.datetime), '%Y%m%d'))
    fig.savefig(fname+'.png')
    # pickle.dump(fig, open(r'plots\\'+fname+'.fig.pickle', 'wb'),protocol=1)
    
    fig,ax1 = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
    ax1.scatter(df['datetime'],df["check"], label="actVal",color='mediumseagreen')
    ax1.plot(df['datetime'],df["check_nom"], label="NomVal",linestyle='--',color='red')
    ax1.plot(df['datetime'],df["check_utol"], label="uTol",linestyle='-.',color='red')
    ax1.plot(df['datetime'],df["check_otol"], label="oTol",linestyle='-.',color='red')
    
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('CuvetteCheck (V)')
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
    ax1.xaxis.set_tick_params(rotation=45)
    #    ax1.set_aspect('equal')
    #    ax1.locator_params(axis='y',tight=True,nbins=10)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
    #    ax2.locator_params(axis='y', nbins=10)
    #    ax2.locator_params(axis='x', nbins=10)
    ax1.set_title(title)
    ax1.grid(True)
    # lns = lns1+lns2
    # labs = [l.get_label() for l in lns]
    # ax1.legend(lns, labs, loc=0)
    ax1.legend()
    # ax1.legend()
    fname = '{}_CuevetteCheck_{}_bis_{}'.format(title,datetime.strftime(min(df.datetime), '%Y%m%d'),datetime.strftime(max(df.datetime), '%Y%m%d'))
    fig.savefig(fname+'.png')


# files39 = glob.glob(dr3900+'\LPG*.csv')
# files60 = glob.glob(dr3900+'\LPG*.csv')

# vaa = ['RoundCuvetteLevel', 'RoundCuvetteTemp']
# level39 =[]
# temp39=[]
# df39 = pd.DataFrame(columns=['sn', 'datetime','level','temp'])
# len39 = len(files39)
# for n,f in enumerate(files39):
#     try:
#         printProgressBar(n, len39)
#         h = pd.read_csv(f,usecols=[1,7])
#         # h = pd.read_csv(f, sep='?')
#         temp = pd.DataFrame({'sn':[os.path.basename(f).split('.c')[0].split('_')[1]], 
#                              'datetime':[datetime.strptime('_'.join([os.path.basename(f).split('.c')[0].split('_')[2],
#                                                  os.path.basename(f).split('.c')[0].split('_')[3]]),'%Y%m%d_%H%M')],
#                              'level':[float(h[h.iloc[:,0]=='RoundCuvetteLevel'].values[0][1])],
#                              'temp':[float(h[h.iloc[:,0]=='RoundCuvetteTemp'].values[0][1])]})
#         # level39.append(float(df[df.iloc[:,1]=='RoundCuvetteLevel'].values[0][7]))
#         # h = dv.messung(f)
#         # level39.append(float(h[h['VAAxxx']==vaa[0]]['actVal'].values[0]))
#         df39 = pd.concat([df39,temp])
#     except:
#         pass