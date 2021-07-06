# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:16:56 2017

@author: sbergmann
"""

import pandas as pd
import os as os
import os.path
import glob
import matplotlib.pyplot as plt
import numpy as np
import csv


mainfolder=os.path.abspath(r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\Projekte\Doughnut\Lexan_langzeit_Stabilitaet\epa')
folders=[x[0] for x in os.walk(mainfolder)]
#um ersten Ordner zu überspringen
df_temp=pd.DataFrame(columns=[x.split('\\')[-1] for x  in folders[1:]]) 
for dic in range(len(folders)-1):
       
    files = glob.glob(folders[dic+1]+"\\*.csv")
    df=pd.DataFrame()#Initialisierung eines Dataframes für Messungen
    tol=.02#prozentuale Toleranz 
    utol=.1#absolute Toleranz in NTU
    rawData=pd.DataFrame()
    temp=[]
    for i in files:
        with open(i) as csvfile:
            rowid=1
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if '[Log]' in row:
                    break
                else: 
                    rowid=rowid+1
        rawData=pd.read_csv(i,skiprows=rowid)#Einlesen der gesamten Messdaten
        temp.append(np.mean(rawData['ACT_TEMPERATURE_NTC']))
        df['VAAxxx']=pd.DataFrame(rawData['VAAxxx'])
        df['name']=pd.DataFrame(rawData['name'])#speichern der Prüfmittel (name)
        df[i.split("_")[-2]+"_"+i.split("_")[-1].split(".")[0]]=rawData['actVal']
    
    container=df['name'].drop_duplicates().reset_index(drop=True)#löschen der Doppeleinträge der Prüfmittel
    VAA=df['VAAxxx'].drop_duplicates().reset_index(drop=True)
    SN=files[0].split('_')[-3]
    
    df_temp[folders[dic+1].split('\\')[-1]]=pd.Series(temp)
    for y in range(df_temp.shape[1]):
        df_temp.iloc[:,y]=pd.Series([(df_temp.iloc[x,y]+df_temp.iloc[x+1,y])/2 for x in range(len(df_temp)-1)])
    df_temp=df_temp.dropna(axis=0,how='any')
    
    plt.plot(df_temp)
    plt.legend(list(df_temp))
    plt.grid()
    plt.title('Durchschnittstemperatur von je zwei Messungen/Tag')
    plt.xlabel('Messung')
    plt.ylabel('Temperatur °C')
    
    df_sorted=[] #nach VAA sortierte Datensätze
    for j in VAA:
        col=df['name'].loc[df['VAAxxx'] == j].drop_duplicates().reset_index(drop=True)
        name = j
        data=pd.DataFrame()
        for i in col:
            data['VAAxxx']=''
            data[i]=np.mean(df.loc[df['VAAxxx']==j].loc[df.loc[df['VAAxxx']==j]['name']==i])
            data['VAAxxx'].iloc[:]=j
        df_sorted.append(data)
  
    f, axarr = plt.subplots(3,4,figsize=(36,22))
    x=y=0        
    y2=0
    # plot aller sortierten Datensätze in einer 4x3 Übersicht
    
    
    
    for i in range(len(df_sorted)):    
        if df_sorted[i].iloc[0,0]=="PMMA" or df_sorted[i].iloc[0,0]=="GELEX":
            if df_sorted[i].iloc[0,0]=="PMMA":
                c='#009999'
            else:
                c='#ff6666'
            x=1
            y=0
            for k in df_sorted[i].columns[1:]:
                axarr[x,y].scatter(df_sorted[i][k].index.values,df_sorted[i][k].values,marker="o",color=c,s=100, label=df_sorted[i].iloc[0,0])
                axarr[x,y].plot(df_sorted[i][k].index.values,[df_sorted[i][k].mean()*tol+df_sorted[i][k].mean()+utol]*np.size(df_sorted[i][k].index.values),c)
                axarr[x,y].plot(df_sorted[i][k].index.values,[-df_sorted[i][k].mean()*tol+df_sorted[i][k].mean()-utol]*np.size(df_sorted[i][k].index.values),c)
                axarr[x,y].set_title(k)
                axarr[x,y].set_xlabel("DateTime")
                axarr[x,y].grid(b=True, which='major', color='k', linestyle='--', lw=0.5)
                for tick in axarr[x,y].get_xticklabels():
                    tick.set_rotation(90)
                axarr[x,y].legend()
                
                y=y+1
                if y==4:
                    y=0
                    x=x+1
        else:
            x=0
            for k in df_sorted[i].columns[1:]:
                axarr[x,y2].scatter(df_sorted[i][k].index.values,df_sorted[i][k].values,marker="o",color='#ff6666',s=100)
                axarr[x,y2].plot(df_sorted[i][k].index.values,[df_sorted[i][k].mean()*tol+df_sorted[i][k].mean()+utol]*np.size(df_sorted[i][k].index.values),'r')
                axarr[x,y2].plot(df_sorted[i][k].index.values,[-df_sorted[i][k].mean()*tol+df_sorted[i][k].mean()-utol]*np.size(df_sorted[i][k].index.values),'r')
                axarr[x,y2].set_title(k)
                axarr[x,y2].set_xlabel("DateTime")
                axarr[x,y2].grid(b=True, which='major', color='k', linestyle='--', lw=0.5)
                for tick in axarr[x,y2].get_xticklabels():
                    tick.set_rotation(90)
                y2=y2+1
        # Statistik
        dp=len(df_sorted[0])
        df_sorted[i].loc['mean']=df_sorted[i].iloc[0:dp].mean()
        df_sorted[i].loc['std']=df_sorted[i].iloc[0:dp].std()
        df_sorted[i].loc['3s']=df_sorted[i].iloc[0:dp].std()*3
        df_sorted[i].loc['max']=df_sorted[i].iloc[0:dp].max()
        df_sorted[i].loc['min']=df_sorted[i].iloc[0:dp].min()
    #    df_sorted[i].loc['range']=df_sorted[i].loc[:].iloc[0:dp].max()-df_sorted[i].loc[:].iloc[0:dp].min()
    
    # Plot überschrift und speichern der plots    
    dstart=files[0].split("_")[-2]
    dend=files[-1].split("_")[-2]
    date=dstart[:4]+'-'+dstart[4:6]+'-'+dstart[6:]+' to '+dend[:4]+'-'+dend[4:6]+'-'+dend[6:]
    f.suptitle(SN+" - Doughnut - Calibration Stability\n"+date,fontsize=20)
    f.tight_layout()
    f.savefig(folders[dic+1]+'\\'+SN+'.png') 
    # Ausgabe der Messwerte in einem Excel spreadsheet
    df_forExcel=pd.concat(df_sorted,axis=1)
    writer = pd.ExcelWriter(folders[dic+1]+'\\'+SN+'.xlsx', engine='xlsxwriter')
    df_forExcel.to_excel(writer, sheet_name='Data')
    writer.save()              