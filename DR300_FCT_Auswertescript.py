# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 07:56:49 2018

@author: sbergmann

Copyright@Hach Lange GmbH 


Skript zur Auswertung der FCT_JABIL Dateien

Skript erstellt zu allen FCT-Tests einen Graphen und fügt die Toleranzen 
hinzu die es aus der dazugehörigen htm Datei bezieht.
(csv Datei und HTML Datei in einen separaten Ordner einfügen und Pfad in
variable "path" angeben)

Paratmeter
----
path: string
    Pfadname zum Ordner mit auszuwertenden Dateien
    
Ausgabe
----
fig: png
    Grafiken über alle Testpunkte des FCTs (abgespeichert in einem neuerstellten Ordner)

"""
#Projektordner
#\\hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\6_Electronics\4_FCT_HWC\FCT_ZBB094_(Mainboard)\FCT_Results_JABIL
import glob 
import pandas as pd
import os as os
import os.path
import matplotlib.pyplot as plt


#files = glob.glob('*.csv')

df = pd.DataFrame()
#for file in files:
#    data = pd.read_csv(file)
#    week = file.split('\\')[-1].split('.')[0]
#    data.insert(loc=0, column='week', value=week)
#    df = pd.concat([df, data])

# dateipfad zum ornder der die csv datei enthält (separaten Ordner erstellen)
#path = r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\6_Electronics\4_FCT_HWC\FCT_ZBB094_(Mainboard)\FCT_JABIL\Mustang_2018_Week38_252LPs_v2'
path = r'\\Hach-lange.ewqg.com\europe\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\6_Electronics\4_FCT_HWC\FCT_ZBB094_(Mainboard)\FCT_Results_JABIL\Mustang_2018_Week50_10Masterboards'

csv_file = glob.glob(path+'\*.csv')[0]

df = pd.read_csv(csv_file)
week = csv_file.split('\\')[-1].split('.')[0]
df.insert(loc=0, column='week', value=week)
#df = pd.concat([df, data])
#    
data_set = df.week.drop_duplicates().reset_index(drop=True)
df_stats = df.describe()
# öffne html Datei (enthält die Grenzen der einzelnen Testparameter)
html_file = glob.glob(path+'\*\*.htm')[0]
#html_file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\6_Electronics\4_FCT_HWC\FCT_ZBB094_(Mainboard)\FCT_JABIL\Mustang_2018_Week38_252LPs\ZBB0941838000345(9-18-2018 12-34-47)-1.htm'
bounds=pd.read_html(html_file, skiprows=1)[0]
bounds.columns=bounds.iloc[0]
bounds=bounds.reindex(bounds.index.drop(0))

for data in data_set:
#    new_path = path+'\\'+data
    new_path = path+'\graphs'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        counter = 0
        for col in df.columns[2:]:
            counter = counter+1
            print(str(counter)+'/'+str(len(df.columns))+': '+col)
                            
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
                    ax.plot(df.SerialNumber, lbound, 'k--', label='up lim' )
                    ax.plot(df.SerialNumber, ubound, 'k--', label='lo lim' )
                except IndexError:
                    pass
                
                ax.plot(df.SerialNumber, mean_line, 'r--', label='mean' )
                ax.plot(df.SerialNumber, plus_std3, 'g--', label='+3s')
                ax.plot(df.SerialNumber, minus_std3, 'g--', label='-3s')
                ax.plot(df.SerialNumber, plus_std5, 'b--', label='-5s')
                ax.plot(df.SerialNumber, minus_std5, 'b--', label='-5s')

            except KeyError:
                pass
            
            # plot der eigentlichen Daten als letztes, damit Datenlinie über alle anderen liegt
            ax.plot(df.SerialNumber, df[col])
            ax.set(xlabel='SerialNumber', ylabel='value',
               title=col)
            ax.set_xticklabels(labels=df.SerialNumber,rotation=90)

            try:
                # Bug-Umgehung: wenn ohne, Grafiken mit konstanten Werten erhalten exponentielle y-Achse
                ax.ticklabel_format(useOffset=False, axis='y') 
            except AttributeError:
                pass
            # kleine Schrift, damit bei vielen Geräten die Seriennummern noch lesbar sind
            ax.tick_params(axis='x',labelsize=5.5)
            plt.grid()
            plt.legend()
            plt.tight_layout()
            # Testnamen enthalten zum Teil verbotene Buchstaben, die nicht als Namen im Windowsdateisystem verwendet werden können
            if '/' or '#' or '\\' in col:
               col = col.replace('/','_')
               col = col.replace('#','_')
               col = col.replace('\t','_t')
            fig.savefig(new_path+'\\'+col+'.png')
            plt.close(fig)