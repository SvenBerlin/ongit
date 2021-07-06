# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 10:58:19 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Doughnut\18_FAST\81909 Hamamatsu Verification\1_Verification\Doughnut_BTiso_600calib\Analyse\FI_after_AUmb_change\SingleMeas__Calib_20NtuCuv_TM_Ref_nAmpere.xlsx')
h = df[df['cat1']=='iso'][df[df['cat1']=='iso']['cat2']=='LPG']
h = df[df['cat1']=='iso']
#h_s = h[h['cat3']=='serie']
#h_e = h[h['cat3']=='ebv']
#stats = h.groupby(by='cat3').describe()['actVal'][['mean','std']]
#med = h.groupby(by='cat3').median()['actVal']
#std = h.groupby(by='cat3').std()['actVal']*3
#med_ebv = pd.Series([med.loc['ebv']]*len(h),name='median_ebv')
#med_ser = pd.Series([med.loc['serie']]*len(h),name='median_ser')
#std_ebv = pd.Series([std.loc['ebv']]*len(h),name='std_ebv')
#std_ser = pd.Series([std.loc['serie']]*len(h),name='std_ser')
#nom = pd.Series([h['NomVal'].iloc[0]]*len(h),name='nom')
#upTol = pd.Series([h['upTol'].iloc[0]]*len(h),name='upTol')
#loTol = pd.Series([h['loTol'].iloc[0]]*len(h),name='loTol')
#stats = pd.concat([nom,upTol,loTol,med_ebv,med_ser,std_ebv,std_ser],axis=1)

med = h.groupby(by='cat3').median()['actVal']
std = h.groupby(by='cat3').std()['actVal']*3
med_ebv = pd.DataFrame({'val':[med.loc['ebv']]*len(h),'stat':['median_e']*len(h),'cat':['median_e']*len(h),'date':h['date'].reset_index(drop=True)})
med_ser = pd.DataFrame({'val':[med.loc['serie']]*len(h),'stat':['median_s']*len(h),'cat':['median_s']*len(h),'date':h['date'].reset_index(drop=True)})
std_ebv = pd.DataFrame({'val':[med.loc['ebv']+std.loc['ebv']]*len(h),'stat':['std_e']*len(h),'cat':['std_e']*len(h),'date':h['date'].reset_index(drop=True)})
std_ser = pd.DataFrame({'val':[med.loc['serie']+std.loc['serie']]*len(h),'stat':['std_s']*len(h),'cat':['std_s']*len(h),'date':h['date'].reset_index(drop=True)})
std_ebv_n = pd.DataFrame({'val':[med.loc['ebv']-std.loc['ebv']]*len(h),'stat':['std_e_n']*len(h),'cat':['std_e']*len(h),'date':h['date'].reset_index(drop=True)})
std_ser_n = pd.DataFrame({'val':[med.loc['serie']-std.loc['serie']]*len(h),'stat':['std_s_n']*len(h),'cat':['std_s']*len(h),'date':h['date'].reset_index(drop=True)})
nom = pd.DataFrame({'val':[h['NomVal'].iloc[0]]*len(h),'stat':['nom']*len(h),'cat':['nom']*len(h),'date':h['date'].reset_index(drop=True)})
upTol = pd.DataFrame({'val':[h['upTol'].iloc[0]]*len(h),'stat':['upTol']*len(h),'cat':['nom']*len(h),'date':h['date'].reset_index(drop=True)})
loTol = pd.DataFrame({'val':[h['loTol'].iloc[0]]*len(h),'stat':['loTol']*len(h),'cat':['nom']*len(h),'date':h['date'].reset_index(drop=True)})

stats = pd.concat([nom,upTol,loTol,med_ebv,med_ser,std_ebv,std_ser,std_ebv_n,std_ser_n],axis=0)
#stats['date']=h['date'].reset_index(drop=True)

sns.set()
f, ax =plt.subplots(1,1)
colors = 'green green green orange blue orange blue orange blue orange blue'.split()
sns.scatterplot(x='date',y='actVal', hue='cat3',data=h, ax=ax)
#sns.lineplot(x='date', y='val',data=stats,hue='cat',units='stat',estimator=None,legend=False, color=colors)
sns.lineplot(x='date', y='val',data=nom, color='green',alpha=.5)
sns.lineplot(x='date', y='val',data=upTol, color='green',alpha=.5,)
sns.lineplot(x='date', y='val',data=loTol, color='green',alpha=.5)
sns.lineplot(x='date', y='val',data=med_ebv, color='orange',alpha=.5)
sns.lineplot(x='date', y='val',data=med_ser, color='blue',alpha=.5)
sns.lineplot(x='date', y='val',data=std_ebv, color='orange',alpha=.5)

sns.lineplot(x='date', y='val',data=std_ebv_n, color='orange',alpha=.5)
sns.lineplot(x='date', y='val',data=std_ser, color='blue',alpha=.5)
sns.lineplot(x='date', y='val',data=std_ser_n, color='blue',alpha=.5)
#ax.lines[0].set_linestyle("--")
#sns.lineplot(x='date', y='val',data=stats[stats[]]
#stats.plot(ax=ax)
#sns.scatterplot(x='date',y='actVal',data=h_s, colors='red')
plt.title('Doughnut LPG/LXG iso ref_nAmpere')
plt.xlim(h['date'].min(),h['date'].max())
plt.show()