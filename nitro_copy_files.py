# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 08:19:11 2022

@author: sbergmann
"""

import os as os
import shutil
import glob
import pandas as pd


wf = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MBpilot\Wiederfindung\Auswertung\EP - 2mm\Wiederfindung'
cal = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\07_Test_Messungen\MBpilot\FI_Automat\EP - 2mm'

wf_files = glob.glob(wf+'\\*.csv')

cal_files = glob.glob(cal+'\\*.csv')
df_cal = pd.DataFrame()

for f in cal_files:
    df_cal = pd.concat([df_cal,pd.DataFrame({'path':[f],'sn':[f.split('_')[-6]],'date':[os.path.getmtime(f)]})])
    # df_cal = pd.concat([df_cal,pd.DataFrame({'path':[f],'sn':[f.split('_')[-3]],'date':[os.path.getmtime(f)]})])
df_cal.sort_values("date",inplace=True)
df_cal.drop_duplicates('sn',keep="last",inplace=True)
df_cal.reset_index(drop=True,inplace=True)

copy =[]
for f_wf in wf_files:
    for idx, sn in enumerate(df_cal['sn']):
        if f_wf.split('_')[-3] == sn:
            copy.append(df_cal.loc[idx,"path"])
            
for f in copy:
    print(f)
    shutil.copy2(f,os.path.join(wf,os.path.basename(f)))
        

