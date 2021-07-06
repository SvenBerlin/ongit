# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:16:48 2021

@author: sbergmann

Tool zur Auswertung von Burnin und log.curr Dateien des DR3900.
Auszuwertende Dateien müssen sich in einem separaten Ordner befinden, dessen 
Pfad in der Variable path anzugeben ist. 
Es wird ein neuer Ordner mit dem Namen "Output_YYYYmmdd_HHMMSS" erstellt,
in dem alle erzeugten Auswertungen abgespeichert werden.

Es werden im Zuge der Auswertung folgende Dateien erzeugt:
    Excel-Spreadsheet ("<nameDesOrdners>.xlsx") - Grafiken, Tabellen inkl.
        Statistiken zu allen relvanten Wellenlängen und Extraseite mit den 
        Abweichungen
    PNG-Grafiken zu allen Wellenlängen und Messwerten aller Geräte
    PNG-Grafiken der log.curr Dateien
    
Parameter
----------

path: string
    dedizierter Pfad des Ordners der alle auszuwertenen Dateien enthält.
"""

import pandas as pd
import glob as glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime,timedelta
import os as os
import numpy as np

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

def outputFolder(path):
    outputPath = os.path.join(path, f'Output_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    os.mkdir(outputPath)
    return outputPath
    
def excelCell(c):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    excel = ''
    cnt = 0
    while True:
        if c-len(letters)>0:
            excel+=letters[cnt]
            cnt += 1
            c = c- len(letters)
        else:
            excel += letters[c]
            break
    return excel

def readBurnin(path):
    files = glob.glob(path+'\\*.csv')
    df = pd.DataFrame()
    numFiles = len(files)
    print(f'start loading {numFiles} files...')
    for n,f in enumerate(files):
        printProgressBar(n,numFiles-1, prefix=f'loading files')
        temp = pd.read_csv(f,skiprows=1)
        temp['file'] = f
        df = pd.concat([df,temp])
    print(f'...{numFiles} successfully loaded')
    print(f'processing data...')
    df.Zeitstempel = pd.to_datetime(df.Zeitstempel)
    print(f'...finished')
    return df

def extractFilter(df,filters=[340,546,900]):
    print(f'start extracting wavelengths {filters}...')
    df_filter = []
    numFiles = df.file.nunique()
    cnt = 0
    for wl in filters:
        df_filter.append(pd.DataFrame())
        # df_filter[-1]['WL']=wl
        for n,f in enumerate(df.file.unique()):
            printProgressBar(cnt,numFiles*len(filters)-1, prefix=f'extracting {wl}nm')
            device = os.path.basename(f).split('_')[2]
            mindex = pd.DataFrame(
                [['Istwert',device],['Ist Mess',device],['Ist Ref',device]],
                columns=['Kanal', 'Seriennummer'])
            index = pd.MultiIndex.from_frame(mindex)
            temp = pd.DataFrame(columns=index)
            for val in ['Istwert', 'Ist Mess', 'Ist Ref']:
                temp[val] = df[(df.file==f) & (df.Messtyp=='Burn_In_Long') & (df.vonScan==wl)][val].reset_index(drop=True)
            df_filter[-1] = pd.concat([df_filter[-1],temp], axis=1)
            cnt += 1
        df_filter[-1]['WL']=wl
    print(f'...finished successfully extracting wavelengths')
    return df_filter

def generateOutput(df_filter, path,outputPath, mydpi=96):
    print(f'start generating outputs...')
    xlsfile = os.path.join(outputPath,f'{os.path.basename(path)}.xlsx')
    writer = pd.ExcelWriter(xlsfile, engine='xlsxwriter')
    workbook = writer.book
    abw_sheet = workbook.add_worksheet('Abweichung')
    abw_chart = workbook.add_chart({'type': 'column'})
    numPlots = len(df_filter)*3*int((df_filter[0].shape[1]-1)/3)
    cnt = 0
    for h in df_filter:
        sheet_name = f'Filter{str(int(h.loc[0,"WL"][0]))}'
        stats = h.describe()
        stats.loc['Delta'] = stats.loc['max']-stats.loc['min']
        stats.loc['Diff'] = stats.loc['Delta']/stats.loc['mean']
        pd.concat([h,stats]).to_excel(writer, sheet_name=sheet_name,index=True, header=True)
        for n,val in enumerate(['Istwert', 'Ist Mess', 'Ist Ref']):
            worksheet = workbook.add_worksheet(f'{str(int(h.loc[0,"WL"][0]))} {val}')  
            chart = workbook.add_chart({'type': 'line'})
            for col in range(int((h.shape[1]-1)/3)):
                chart.add_series({
                    'categories': [sheet_name, 3, 0, len(h)+1, 0],
                    'name':       [sheet_name, 1, col*3+n+1],
                    'values':     [sheet_name, 1, col*3+n+1, len(h)+1, col*3+n+1],
                    'gap':        10,
                })
            chart.set_legend({'position': 'bottom'})
            chart.set_size({'width':1600,'height':600})
            chart.set_x_axis({'name': 'Messpunkt'})
            chart.set_y_axis({'name': 'Messwert', 'major_gridlines': {'visible': True}})
            chart.set_title({'name': sheet_name ,'overlay': False,})
            worksheet.insert_chart('A1', chart)
            
            fig,ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
            title = f'{val} bei {str(int(h.loc[0,"WL"][0]))}nm'
            for dev in h.loc[:,val].columns:
                printProgressBar(cnt,numPlots-1, prefix=f'plotting {title.replace(" ","_")}.png')
                x = h.loc[:,val][dev].index
                y = h.loc[:,val][dev]
                ax.scatter(x, y, s=1,label=dev)
                cnt += 1
            ax.set_xlabel('Messpunkt')
            ax.set_ylabel('Messwert')
            ax.set_title(title)
            ax.grid()
            plt.legend()
            plt.tight_layout()
            fig.savefig(os.path.join(outputPath,f'{title.replace(" ","_")}.png'))
            plt.close()
            
        abw_chart.add_series({
            'categories': [sheet_name, 1, 1, 1, int((h.shape[1]-1)/3)+1],
            'name':       sheet_name,
            'values':     '='+','.join([f'{sheet_name}!{excelCell(c)}{str(len(h)+13)}'for c in np.arange(1,h.shape[1],3) ]),
            'gap':        10,
        })
    
    abw_chart.set_title({'name': 'Abweichung zum Mittelwert in %' ,'overlay': False,})
    abw_chart.set_size({'width':1600,'height':600})
    abw_sheet.insert_chart('A1', abw_chart)
    writer.save()
    print(f'{xlsfile} saved...')
    
    
def crunchLogFiles(path):
    print('start parsing log files...')
    df_curr = pd.DataFrame()
    curr_files = glob.glob(path+'//*.log.curr')
    numFiles = len(curr_files)    
    df_log = pd.DataFrame(columns=['Seriennummer','Position','NullteOrdnung','Schritte','Offset','diff'])    
    for n,f in enumerate(curr_files):
        printProgressBar(n,numFiles-1, prefix='parsing files')
        temp = pd.read_csv(f)
        gitter = [n for n,row in enumerate(temp.iloc[:,0]) if 'Gitter_Dauertest' in row]
        data = pd.DataFrame()
        for elm in gitter:
            for i in range(elm,len(temp)):
                if temp.iloc[i+1,0][0] not in 'Pa':
                    end = i+1
                    break
            
            # data = pd.concat([data,temp.iloc[elm:i]])
            data = pd.concat([data,temp.iloc[elm+1:i,0].reset_index(drop=True)],axis=1,ignore_index=True)
       
        
            for col in data:
                for row in data[col]:
                    try:
                        if 'Position' in row:
                            new_row={}
                            new_row['Seriennummer'] = os.path.basename(f).split('_')[2]
                            new_row['Position'] = int(row.replace(' ','').split('n')[-1])
                        else:
                            new_row['NullteOrdnung'] = int(row.split('(')[1].split(')')[0][:-2])
                            new_row['Schritte'] = int(row.split('Schritte: ')[1].replace(' ','').split('O')[0])
                            new_row['Offset'] = int(row.split('Offset: ')[1].replace(' ','').split('d')[0])
                            new_row['diff'] = int(row.split('diff: ')[1])
                            # k = new_row
                            df_log=df_log.append(new_row,ignore_index=True)
                    except TypeError:
                        pass
    print('...finished parsing')
    print('processing data...')
    df_log = df_log.astype(int)
    print('...finished!')
    return df_log

def generateLogGraphs(df_log,outputPath, mydpi=96):
    print('start generating log-graphs...')
    numPlots = len(df_log.columns[2:])*df_log.Seriennummer.nunique()
    cnt = 0
    for vaa in df_log.columns[2:]:
        title = f'{os.path.basename(path)}_{vaa}'
        fig,ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
        for sn in df_log.Seriennummer.unique():
            printProgressBar(cnt,numPlots-1, prefix=f'plotting {title}.png')
            temp = df_log[df_log['Seriennummer']==sn]
            ax.scatter(temp['Position'],temp[vaa],s =1, label= sn)
            ax.set_xlabel('Position')
            ax.set_ylabel(vaa)
            ax.set_title(title)
            ax.grid()
            ax.legend()
            plt.tight_layout()
            fig.savefig(os.path.join(outputPath,f'{title}.png'))
            cnt += 1
        plt.close()
    print('...finished')

if __name__ == '__main__':
    path = r'C:\Users\sbergmann\Desktop\dr3900burnin'
    outputPath = outputFolder(path)
    
    df = readBurnin(path)
    df_filter = extractFilter(df)
    df_log = crunchLogFiles(path)
    generateOutput(df_filter,path,outputPath)
    generateLogGraphs(df_log,outputPath)
    
    
 