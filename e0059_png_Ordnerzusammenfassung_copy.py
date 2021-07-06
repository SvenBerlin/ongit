# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 11:48:39 2018

@author: sbergmann

Nach erfolgreichem tracking von HWC/FI Daten zur Erstellung einer Zusammenfassung
zu verwenden.
Es wird eine Excel Datei nach folgendem Schema erstellt:
    Check               PNG         XLSX            PKL
    -------------------------------------------------------------
    (zur Kontrolle)     (Grafik)    (Excel-Link)    (Pickle-Link)
    ...
    ...
    ...

Es ist lediglich der Pfad des Ordners mit den zusammenzufassenden Dateien
in der Variable "path" anzugeben.   

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import numpy as np
import glob


def png_folder_summary(path):
    '''
    path:   Pfad zu dem Ordner mit den zusammenzufassenden Dateien
    '''
#path = r'C:\Users\sbergmann\Desktop\python_test\tracking_excel\files'
    files = glob.glob(path+'\\*')
    # Auswahl der Prüfmittel auf Basis der erstellten Plots
    pmp = [x for x in files if '.png' in x] # Liste der png Bilder
    pmp = [x.split('\\')[-1].split('.')[0] for x in pmp] # Liste der Prüfmittelpunkte
    png = []
    xlsx = []
    pkl = []
    # suche nach xlsx und pkl Dateien dessen Basisnamen zu den Prüfmittelpunkten passen
    
    for test in pmp:
        if len(glob.glob(path+'\\'+test+'.*'))==3:
            png.append(glob.glob(path+'\\'+test+'.png')[0])
            xlsx.append('=HYPERLINK("'+glob.glob(path+'\\'+test+'.xlsx')[0]+'")')
            pkl.append('=HYPERLINK("'+glob.glob(path+'\\'+test+'.pkl')[0]+'")')
    
    png = pd.Series(png, name ='png')
    pmp = pd.Series(pmp, name ='pmp')
    xlsx = pd.Series(xlsx, name ='xlsx')
    pkl = pd.Series(pkl, name ='pkl')
    # Dataframe mit allen Links und Prüfmittelpunkten; lösche alle unvollständige Reihen
    df = pd.concat([pmp,png,xlsx,pkl],axis=1)#.dropna()
    
    print('----- saving to Excel -----')
    
    writer = pd.ExcelWriter(path + '\\' '__evalutation.xlsx', engine='xlsxwriter')
    workbook = writer.book
    pd.DataFrame().to_excel(writer, sheet_name = 'evaluation')
    worksheet = writer.sheets['evaluation']
    # Erstelle Formate für verschiedene Zellen in der Exceldatei
    header_format = workbook.add_format({'bold': True,'valign': 'buttom',})
    link_format = workbook.add_format({'valign': 'top','font_color':'blue'})
    check_format = workbook.add_format({'align':'center','valign': 'vcenter','font_size':30, })
    # Schreibe Tabellenüberschriften
    for col, title in enumerate('check png xlsx pkl'.split()):
            worksheet.write(0, col, title, header_format)
    # Fülle Zellen der Tabelle
    for row in range(len(df)):
        for col in range(1,len(df.columns)):
            if col == 1: # ==> png Links (speicher PNG in Tabellenzelle)
                worksheet.write(row+1, col-1, '', check_format) # setze Zellenformat für Spalte "check"
                worksheet.set_row(row+1, 400, None) # setze Zellenhöhe für png auf 400 
                worksheet.set_column('B:B', 150, None) # setze Zellenbreite für png auf 150
                worksheet.insert_image(row+1, col, df.iloc[row,col],{'x_scale': 0.5, 'y_scale': 0.5} )
            else: # ...schreibe Link in Zelle und verwende das vorgesehende Format
                worksheet.write(row+1, col, df.iloc[row,col], link_format)
    
    writer.save() 
    workbook.close()     
    print('----- Done -----')   
    
    
#    
## -*- coding: utf-8 -*-
#"""
#Created on Mon Oct 29 11:48:39 2018
#
#@author: sbergmann
#
#Nach erfolgreichem tracking von HWC/FI Daten zur Erstellung einer Zusammenfassung
#zu verwenden.
#Es wird eine Excel Datei nach folgendem Schema erstellt:
#    Check               PNG         XLSX            PKL
#    -------------------------------------------------------------
#    (zur Kontrolle)     (Grafik)    (Excel-Link)    (Pickle-Link)
#    ...
#    ...
#    ...
#
#Es ist lediglich der Pfad des Ordners mit den zusammenzufassenden Dateien
#in der Variable "path" anzugeben.   
#
#Copyright@Hach Lange GmbH 
#"""
#
#import pandas as pd
#import numpy as np
#import glob
#
#
#def png_folder_summary(path):
#    '''
#    path:   Pfad zu dem Ordner mit den zusammenzufassenden Dateien
#    '''
##path = r'C:\Users\sbergmann\Desktop\python_test\tracking_excel\files'
#    files = glob.glob(path+'\\*')
#    # Auswahl der Prüfmittel auf Basis der erstellten Plots
#    png = [x for x in files if '.png' in x] # Liste der png Bilder
#    pmp = [x.split('\\')[-1].split('.')[0] for x in png] # Liste der Prüfmittelpunkte
#    xlsx = []
#    pkl = []
#    # suche nach xlsx und pkl Dateien dessen Basisnamen zu den Prüfmittelpunkten passen
#    for test in pmp:
#        flag_xlsx = 0 #flags zur Kontrolle über fehlende Dateien (nur komplette Sets (png,xlsx und pkl))
#        flag_pkl = 0
#        for f in files:
#            if test in f:
#                # speicher gematchte Dateipfade als Hyperlinks
#                if '.xlsx' in f:
#                    xlsx.append('=HYPERLINK("'+f+'")')
#                    flag_xlsx = 1
#                if '.pkl' in f:
#                    pkl.append('=HYPERLINK("'+f+'")')
#                    flag_pkl = 1
#        # wenn für Prüfmittelpunkt xlsx oder pkl NICHT gefunden wurde, schreibe nan in Zelle
#        if flag_xlsx == 0:
#            xlsx.append(np.nan)
#        if flag_pkl == 0:
#            pkl.append(np.nan)
#    
#    png = pd.Series(png, name ='png')
#    pmp = pd.Series(pmp, name ='pmp')
#    xlsx = pd.Series(xlsx, name ='xlsx')
#    pkl = pd.Series(pkl, name ='pkl')
#    # Dataframe mit allen Links und Prüfmittelpunkten; lösche alle unvollständige Reihen
#    df = pd.concat([pmp,png,xlsx,pkl],axis=1).dropna()
#    
#    print('----- saving to Excel -----')
#    
#    writer = pd.ExcelWriter(path + '\\' '__evalutation.xlsx', engine='xlsxwriter')
#    workbook = writer.book
#    pd.DataFrame().to_excel(writer, sheet_name = 'evaluation')
#    worksheet = writer.sheets['evaluation']
#    # Erstelle Formate für verschiedene Zellen in der Exceldatei
#    header_format = workbook.add_format({'bold': True,'valign': 'buttom',})
#    link_format = workbook.add_format({'valign': 'top','font_color':'blue'})
#    check_format = workbook.add_format({'align':'center','valign': 'vcenter','font_size':30, })
#    # Schreibe Tabellenüberschriften
#    for col, title in enumerate('check png xlsx pkl'.split()):
#            worksheet.write(0, col, title, header_format)
#    # Fülle Zellen der Tabelle
#    for row in range(len(df)):
#        for col in range(1,len(df.columns)):
#            if col == 1: # ==> png Links (speicher PNG in Tabellenzelle)
#                worksheet.write(row+1, col-1, '', check_format) # setze Zellenformat für Spalte "check"
#                worksheet.set_row(row+1, 400, None) # setze Zellenhöhe für png auf 400 
#                worksheet.set_column('B:B', 150, None) # setze Zellenbreite für png auf 150
#                worksheet.insert_image(row+1, col, df.iloc[row,col],{'x_scale': 0.5, 'y_scale': 0.5} )
#            else: # ...schreibe Link in Zelle und verwende das vorgesehende Format
#                worksheet.write(row+1, col, df.iloc[row,col], link_format)
#    
#    writer.save() 
#    workbook.close()     
#    print('----- Done -----')   