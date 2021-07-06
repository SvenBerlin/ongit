# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 11:50:47 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd

path = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Aquarius_9879x\03_05_05_System_Architecture_and_Specification\Aquarius Concepts\3_03_05_05_Photometry\1_Photometer\Nitro_Prinzip\SPEOS\Input\STW9C2SB_5600.csv'
df = pd.read_csv(path,sep=';',header=None)

df.loc[:,0]=[float(x.replace(',','.')) for x in df.loc[:,0]]
df.loc[:,1]=[float(x.replace(',','.')) for x in df.loc[:,1]]
# df.loc[:,1]=df.loc[:,1]*100
df.sort_values(by=[0],inplace=True)
df.reset_index(drop=True,inplace=True)

output=path.split('.')[0]+'.txt'
df.to_csv(output, header=None, index=None, sep='\t', mode='a')

text = ['OPTIS - Spectrum file v1.0\nLED Spectrum\n']

spectrum = output.split('.')[0]+'.spectrum'
file = open(output,'r')

spec = open(spectrum,'w')
spec.writelines(text)
for line in file:
    spec.write(line)

file.close()
spec.close()
