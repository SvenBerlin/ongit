# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:42:18 2021

@author: sbergmann
"""

import pandas as pd
import os as os

path = r'C:\Users\sbergmann\Desktop\Proben1mm.xlsx'
df = pd.read_excel(path,header=None)
df = df.astype(str)
h = pd.DataFrame({'VAAxxx':'NO3_'+df[0]+'_'+'NO2_'+df[1],'SetNo':'202103'})
h.to_excel(os.path.join(os.path.dirname(path),'Satznummern_1mm.xlsx'),index=False)
