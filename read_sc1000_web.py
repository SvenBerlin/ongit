# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:08:39 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import time
import devdata as dv
date = dv.dvtime(formatmode='dformat_dateiname')

df = pd.DataFrame(columns=['SN', 'actVal', 'Einheit', 'DateTime'])
link = 'http://10.130.25.88/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'

while True:
    tables = pd.read_html(link)
    for t in range(int(len(tables)/2)):
        temp = pd.DataFrame({'SN':[tables[t*2].loc[0,1].split()[-1]],
                             'actVal':[float(tables[t*2].loc[1,1].split()[0])],
                             'Einheit':[tables[t*2].loc[1,1].split()[1]],
                             'DateTime':[pd.to_datetime(' '.join(tables[t*2].loc[1,1].split()[-2:]))]})
    
        if (len(df) == 0) or (not temp.iloc[-1].equals(df.iloc[-1])):
            df = pd.concat([df,temp])
            df.reset_index(drop=True, inplace=True)
            df.to_csv('{}_Ultraturb_verify.csv'.format(date),index=False)
    
            if len(df) ==1:
                print(df.tail(1))
            else:
                print(df.tail(1).to_string(header=False))
    time.sleep(1)