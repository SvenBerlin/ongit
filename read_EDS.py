# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 08:12:53 2022

@author: sbergmann
"""

import pandas as pd
def read_EDS(file,start_block):
    df = pd.read_csv(file,sep="?",header=None) # einlesen der Datei als csv (default sucht er nach "," o.ä., funktioniert jedoch nur bei konstanter Spaltenanzahl)
    block = df[df[0].str.contains('\[')] # selektiere die Zeilen die "[" enhalten
    start = block[block[0]==start_block].index[0] # suche den Block ab den wir die Daten analysieren wollen...
    
    block_ = block.loc[start:] # ...kürze entsprechend die Liste auf relevante Blöcke
    
    dfh = pd.DataFrame() # erstelle ein leeres DataFrame (notwendig, damit in der Schleife neue Daten angehängt werden können) 
    for n,idx in enumerate(block_.index): # iteriere über den Index der Liste (enumerate zählt zusätzlich die Schleifendurchgänge)
        try:
            raw = df.loc[idx+1:block_.index[n+1]-1].values.flatten().tolist() # extrahiere die Daten zwischen zwei Blöcken
        except IndexError:
            raw = df.loc[idx+1:].values.flatten().tolist() # wenn am Ende der Liste, nehme den Rest an Daten aus df
            
        columns = [x.split('=')[0] for x in raw if ';;' not in x] # extrahiere aus den Daten die Spaltennamen (ignoriere Kommentare)
        data = [x.split('=')[1] for x in raw if ';;' not in x] # extrahiere aus den Daten die Werte (ignoriere Kommentare)
        temp = pd.DataFrame(data = dict(zip(columns,data)),index=[block_.loc[idx].iloc[0]]) # erstelle ein temporäres DataFrame mit Spaltennamen und dem aktuellen Index (=Testpunkt)
        dfh = pd.concat([dfh,temp],axis=0) # füge das temporäre DataFrame dem df hinzu
    return dfh


file = r"C:\Users\sbergmann\Desktop\Aquarius\co_ac_unit.eds"
start_block = '[2000]'

dfh = read_EDS(file,start_block)
var1 = dfh.loc['[2001sub0]','ObjectType']
dfh.ObjectType == '9'

str_out =""
data =[]
for idx, row in dfh.iterrows():
    if row['ObjectType']=="9":
        parameter = f'{row["ParameterName"]}'
    else:
        sub = f'{row["ParameterName"]}'
        # data.append(f'{parameter}{sub}')
        data.append([parameter,sub])
        str_out += f"self.{data[-1][0].replace(' ','_')}_{data[-1][1].replace(' ','_').replace('(','_').replace(')','')} = node.sdo['{data[-1][0]}']['{data[-1][1]}']\n"
        
with open('readme.txt', 'w') as f:
    f.write(str_out)  
f.close()      


