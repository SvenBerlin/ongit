# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 07:56:49 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import glob 
import pandas as pd
import os as os
import os.path
import matplotlib.pyplot as plt
#import matplotlib

#path = r'C:\Users\sbergmann\Desktop\Mustang_Mainboard'
#files = glob.glob(path+'\*.csv')
files = glob.glob('*.csv')

df = pd.DataFrame()
for file in files:
    data = pd.read_csv(file)
    week = file.split('\\')[-1].split('.')[0]
    data.insert(loc=0, column='week', value=week)
    df = pd.concat([df, data])
    
data_set = df.week.drop_duplicates().reset_index(drop=True)
df_stats = df.describe()

html_file = glob.glob('*.htm')[0]
bounds=pd.read_html(html_file, skiprows=1)[0]
bounds.columns=bounds.iloc[0]
bounds=bounds.reindex(bounds.index.drop(0))

for data in data_set:
#    new_path = path+'\\'+data
    new_path = data
    if not os.path.exists(new_path):
        os.makedirs(new_path)
#        counter = 0
        for col in df.columns[2:]:
#            counter = counter+1
#            print(counter)
                            
            fig, ax = plt.subplots(figsize=(1920/96,1080/96))
#            ax.plot(df.SerialNumber, df[col])
            try:
                mean_line = [df_stats[col].loc['mean']]*len(df)
                plus_std3 = [mean_line[0]+(df_stats[col].loc['std']*3)]*len(df)
                minus_std3 = [mean_line[0]-(df_stats[col].loc['std']*3)]*len(df)
                plus_std5 = [mean_line[0]+(df_stats[col].loc['std']*5)]*len(df)
                minus_std5 = [mean_line[0]-(df_stats[col].loc['std']*5)]*len(df)
                
                try:
                    lbound = [float(bounds['Lower Limit'][bounds['Test Name']==col].iloc[0])]*len(df)
                    ubound = [float(bounds['Upper Limit'][bounds['Test Name']==col].iloc[0])]*len(df)
                    flag = 0
                except IndexError:
                    flag = 1
                    pass
                
                ax.plot(df.SerialNumber, mean_line, 'r--', label='mean' )
                ax.plot(df.SerialNumber, plus_std3, 'g--', label='+3s')
                ax.plot(df.SerialNumber, minus_std3, 'g--', label='-3s')
                ax.plot(df.SerialNumber, plus_std5, 'b--', label='-5s')
                ax.plot(df.SerialNumber, minus_std5, 'b--', label='-5s')
                
                if flag == 0:
                    ax.plot(df.SerialNumber, lbound, 'k--', label='up lim' )
                    ax.plot(df.SerialNumber, ubound, 'k--', label='lo lim' )
                

            except KeyError:
                pass
            ax.plot(df.SerialNumber, df[col])
            ax.set(xlabel='SerialNumber', ylabel='value',
               title=col)
            ax.set_xticklabels(labels=df.SerialNumber,rotation=90)

            try:
                ax.ticklabel_format(useOffset=False, axis='y')
            except AttributeError:
                pass
            ax.tick_params(axis='x',labelsize=5.5)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            if '/' or '#' or '\\' in col:
               col = col.replace('/','_')
               col = col.replace('#','_')
               col = col.replace('\t','_t')
            fig.savefig(new_path+'\\'+col+'.png')
            plt.close(fig)
