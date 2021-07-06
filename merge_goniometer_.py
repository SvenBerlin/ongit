# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:57:51 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
'''
Wertet mehrere in einem Ordner befindlichen Messungen aus.
Wenn Wiederholmessungen von ein und dem selben Typ im Ordner sind, 
wird der Mittelwert über die Dateien gebildet.
--> TypXYZ_Wellenlänge_01 ,TypXYZ_Wellenlänge_02 , TypXYZ_Wellenlänge_03  usw.
Die angegebene Wellenlänge wird verwendet um in einem gewählten Bereich nach
dem Maximum zu suchen.

Es werden die Rohdaten in einem Excelblatt kopiert und ein Blatt mit 
ausgewerteten Mittelwerten für die spektrale Messung und die Winkelverteilung.
In diesen Blättern werden einmal die absoluten und einmal die relativen 
Werte gespeichert.
Auf dem Blatt "Uebersicht" werden neben Plots, Informationen wie Datum,
Anwender, Messbedingungen und Werte zu FWHM ermittelt und gespeichert.

Es kann zudem eine Dunkelmessung hinterlegt werden (unter dem Namen "dark.csv" 
im selben Ordner abzuspeichern). Steht eine Dunkelmessung zur Verfügung, werden von den Messungen
die Dunkelwerte abgezogen.

Angegeben werden müssen:
    path - Pfad zum Ordner der die Messdaten enthält
    wl - Wellenlängebereiche für den Plot [untere Grenze, obere Grenze]
    pws - peak weavelength search (Bandbreite in dem nach einem Maximum gesucht werden soll)
            (in einigen Fällen nötig, bei denen das Rauschen besonders ausgeprägt ist)
    user - Benutzer
    note - Listenaufstellung von Notizen
    pos_only - ersetzt alle negativen Werte aus der spektralen Messung mit dem Wert 0
    
Dateiname des erstellten Excel-Blatts trägt den Namen des Ordners in dem die
Messdateien liegen und wird auch in selbigen abgespeichert.
'''


import pandas as pd
import numpy as np
import glob as glob
import os as os
import math
from datetime import datetime
        
def addSuffix(fname):
    base = fname
    num = 1
    while os.path.isfile(fname):
        prefix='0{}'.format(num)[-2:]
        fname = "{0}_{2}{1}".format(*os.path.splitext(base) + (prefix,))
        num +=1
    return fname

def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))

def half_max_x(data,lim,plot=False):
    results = [['index','x1','x2','fwhm','ymax']]
    for n,col in enumerate(data.columns.to_list()):
        x = list(range(lim[n][0],lim[n][1]))
        y = np.array(data[col].loc[x])
        half = max(y)/2.0
        signs = np.sign(np.add(y, -half))
        ymax = float(x[np.where(np.sign(np.add(y,-max(y)))==0)[0][0]])
        zero_crossings = (signs[0:-2] != signs[1:-1])
        zero_crossings_i = np.where(zero_crossings)[0]
        if len(zero_crossings_i) == 1:
            zero_crossings_i = np.append(zero_crossings_i, 0)
        hmx = [col,
            lin_interp(x, y, zero_crossings_i[0], half),
                        lin_interp(x, y, zero_crossings_i[1], half)]
        hmx += [hmx[2]-hmx[1], ymax]
        results.append(hmx)
    return results

def return_pos(array):
    return pd.Series([x if x > 0 else 0 for x in array])

path = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Aquarius_9879x\03_04_04_04_03_Optics\bis_TG2\Bauteile\Roithner_LED\Goniometermessungen'
wl = [360, 650]
pos_only = True
pws = 80 # peak window search - breite des Bereichs in dem nach einem Peak gesucht werden soll
user = 'Sven Bergmann/EGO'
note = ['Dunkelraum (EGO)',
        'LSC100 Goniometer',
        '365nm @ 3.6V/25mA',
        '385nm @ 3.5V/20mA',
        '390nm @ 3.7V/20mA',
        '395nm @ 3.5V/20mA',
        '400nm @ 3.7V/20mA',
        '405nm @ 3.3V/20mA',
        '410nm @ 3.7V/20mA',
        '415nm @ 3.7V/20mA',
        '435nm @ 3.0V/20mA',
        '450nm @ 3.0V/20mA',
        '470nm @ 20mA',
        '475nm @ 50mA'
        ]

try:
    
    files = glob.glob(path+'\*.csv')
    plot_wl = [x-360 for x in wl]
    date_time = datetime.strftime(datetime.now(), '%d.%m.%Y')
    len_note = len(note)
    longest = 0
    for elm in note:
        if len(elm) > longest: longest=len(elm)
    width = math.ceil(longest/8)/3
        
    row_chart = str(6+len_note)
    note = '\n'.join(note)
    
    # excel_file = '{}.xlsx'.format(os.path.basename(path))
    excel_file = path+f'\\{os.path.basename(path)}.xlsx'
    # if os.path.isfile(excel_file): excel_file = addSuffix(excel_file)
    
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    workbook = writer.book
    
    worksheet = workbook.add_worksheet('Uebersicht')
    
    worksheet.write(0,0, date_time)
    worksheet.write(0,1, user)
    worksheet.write(3,1,'Messbedingungen')
    worksheet.insert_textbox(3,3, note, {'x_scale':width, 'y_scale':len_note/6})
    
    chart1 = workbook.add_chart({'type': 'line'})
    chart1.set_title({'name': 'Absolute Intensitäten der spektralen Messung'})
    chart1.set_x_axis({'name': 'Wellenlänge (nm)'})
    chart1.set_y_axis({'name': 'absolute Intensitaet (1)', 'major_gridlines': {'visible': True}})
    
    chart2 = workbook.add_chart({'type': 'line'})
    chart2.set_title({'name': f'Absolute winkelabhängige Intensitäten'})
    chart2.set_x_axis({'name': 'Winkel (deg)'})
    chart2.set_y_axis({'name': 'absolute Intensitaet (1)', 'major_gridlines': {'visible': True}})
    
    chart3 = workbook.add_chart({'type': 'line'})
    chart3.set_title({'name': 'Relative Intensitäten der spektralen Messung'})
    chart3.set_x_axis({'name': 'Wellenlänge (nm)'})
    chart3.set_y_axis({'name': 'relative Intensitaet (1)', 'major_gridlines': {'visible': True}})
    
    chart4 = workbook.add_chart({'type': 'line'})
    chart4.set_title({'name': f'Relative winkelabhängige Intensitäten'})
    chart4.set_x_axis({'name': 'Winkel (deg)'})
    chart4.set_y_axis({'name': 'relative Intensitaet (1)', 'major_gridlines': {'visible': True}})
    
    spectral_sheet = workbook.add_worksheet('mean_spektral')
    angular_sheet = workbook.add_worksheet('mean_winkel')
    
    leds = []
    data = []
    for f in files:
        if 'dark' in os.path.basename(f):
            dark = pd.read_csv(f, header=None)
            dark=dark[dark.columns].apply(pd.to_numeric, errors = 'coerce').combine_first(dark)
        else:
            df = pd.read_csv(f, header=None)
            df=df[df.columns].apply(pd.to_numeric, errors = 'coerce').combine_first(df)
            sheet_name = os.path.basename(f).split('.')[0]
            df.to_excel(writer,sheet_name=sheet_name,index=False, header=False)
            # leds.append(os.path.basename(f).split('_')[0])    
            leds.append(os.path.basename(f).split('.')[0])    
            data.append(df)
        
    
    means_angle=pd.DataFrame()
    means_spectral=pd.DataFrame()
    df = pd.DataFrame({'LED': leds, 'Data':data})
    # leds = df['LED'].unique().tolist()
    leds = df['LED'].apply(lambda x: x.split('_')[0]).unique().tolist()
    pws_all =[]
    for led in leds:
        temp = df[df['LED'].str.contains(led)]
        try:
            pws_wl = int(temp.iloc[0]['LED'].split('_')[-2])
            pws_wl = [pws_wl-round(pws/2),pws_wl+round(pws/2)]
            pws_wl = [x if x>360 else 360 for x in pws_wl]
            pws_wl = [x if x<1000 else 1000 for x in pws_wl]
        except ValueError:
            pws_wl = [360, 1000]
        pws_all.append(pws_wl) 
        # temp = df[df['LED']==led]
        angular = pd.DataFrame()
        spectral = pd.DataFrame()
        for n in temp.index:
            m = temp.loc[n,'Data']
            # pws_wl = temp.loc[n,'LED'].split('_')
            # # typ = pws_wl[0]
            # try:
            #     if len(pws_wl)==2:
            #         pws_wl = int(pws_wl[1][:-2])
            #     else:
            #         # pws_wl = int(pws_wl[-2][:-2])
            #         pws_wl = int(pws_wl[-2])
            #     pws_wl = [pws_wl-round(pws/2),pws_wl+round(pws/2)]
            #     pws_wl = [x if x>360 else 360 for x in pws_wl]
            #     pws_wl = [x if x<1000 else 1000 for x in pws_wl]
            # except ValueError:
            #     pws_wl = [360, 1000]
            # pws_all.append(pws_wl) 
            # pws_wl = led.split('_')
            # # typ = pws_wl[0]
            # try:
            #     if len(pws_wl)==2:
            #         pws_wl = int(pws_wl[1][:-2])
            #     else:
            #         # pws_wl = int(pws_wl[-2][:-2])
            #         pws_wl = int(pws_wl[-2])
            #     pws_wl = [pws_wl-round(pws/2),pws_wl+round(pws/2)]
            #     pws_wl = [x if x>360 else 360 for x in pws_wl]
            #     pws_wl = [x if x<1000 else 1000 for x in pws_wl]
            # except ValueError:
            #     pws_wl = [360, 1000]
            # pws_all.append(pws_wl) 
            
            
            scanrow = m.index[m[0]=='Scan Angle:'][0]
            scan0 = m.loc[scanrow].index[m.loc[scanrow]==0][0]
            startrow = 46
            if 'dark' in locals():
                dark.iloc[startrow:,scan0] = [x if x>0 else 0 for x in dark.iloc[startrow:,scan0]]
                spec = m.iloc[startrow:,scan0] - dark.iloc[startrow:,scan0]
            else:
                spec = m.iloc[startrow:,scan0]
            if pos_only: spec = return_pos(spec)
            # spec = pd.Series([x if x > 0 else 0 for x in spec])
            spectral = pd.concat([spectral, spec],axis=1)
            # angledistr = spec.index[spec==max(spec)][0]
            # angledistr = spec.index[spec==max(spec.iloc[wl[0]:wl[1]])][0]
            angledistr = spec.index[spec==max(spec.iloc[pws_all[-1][0]-360+startrow:pws_all[-1][1]-360+startrow])][0]
            if 'dark' in locals():
                dark.iloc[angledistr, 2:] = [x if x>0 else 0 for x in dark.iloc[angledistr, 2:]]
                angl = m.iloc[angledistr, 2:] - dark.iloc[angledistr, 2:]
            else:
                angl = m.iloc[angledistr, 2:]
            # if pos_only: angl = return_pos(angl)
            # angl = m.iloc[angledistr, 2:] 
            # angl = pd.Series([x if x > 0 else 0 for x in angl])
            angular = pd.concat([angular,angl],axis=1)
        angular['mean_angle'] = angular.mean(axis=1)
        spectral['mean_spectral'] = spectral.mean(axis=1)
        means_angle[led] = angular['mean_angle'].reset_index(drop=True)
        means_angle[led+'_norm'] = means_angle[led]/max(means_angle[led])
        means_spectral[led] = spectral['mean_spectral'].reset_index(drop=True)
        means_spectral[led+'_norm'] = means_spectral[led]/max(means_spectral[led])
    means_angle.set_index(m.iloc[scanrow, 2:], inplace=True, drop=True)
    means_spectral.set_index(m.iloc[startrow:, 0], inplace=True, drop=True)
    
    fwhm = half_max_x(means_spectral[leds], lim=pws_all)
    fwhm = pd.DataFrame(data=fwhm[1:], columns=fwhm[0])
    fwhm.set_index('index',drop=True,inplace=True)
    writer.sheets['Uebersicht'] = workbook.worksheets()[0]
    fwhm.to_excel(writer, sheet_name='Uebersicht', startrow=int(row_chart)+60, startcol=1)
    # [elm for ls in fwhm for elm in ls]
        
    
    writer.sheets['mean_spektral'] = spectral_sheet
    means_spectral.to_excel(writer, sheet_name= 'mean_spektral',index=True, header=True)
    writer.sheets['mean_winkel'] = angular_sheet
    means_angle.to_excel(writer, sheet_name= 'mean_winkel',index=True, header=True)
    
    
    # worksheet = workbook.worksheets()[workbook.worksheets.index('mean_spektral')]
    # worksheet = workbook.worksheets()[workbook.worksheets.index('mean_winkel')]
    
    for n,col in enumerate(means_angle.columns):
        if not '_norm' in col:
            chart1.add_series({
                'categories': ['mean_spektral', 1+plot_wl[0], 0, 1+plot_wl[1], 0],
                'name':       col,
                'values':     ['mean_spektral', 1+plot_wl[0], n+1, 1+plot_wl[1], n+1],
                'gap':        10,
            })
            
            chart2.add_series({
                'categories': ['mean_winkel', 1, 0, len(means_angle)+1, 0],
                'name':       col,
                'values':     ['mean_winkel', 1, n+1, len(means_angle)+1, n+1],
                'gap':        10,
            })
        else:
            chart3.add_series({
                'categories': ['mean_spektral', 1+plot_wl[0], 0, 1+plot_wl[1], 0],
                'name':       col,
                'values':     ['mean_spektral', 1+plot_wl[0], n+1, 1+plot_wl[1], n+1],
                'gap':        10,
            })
            
            chart4.add_series({
                'categories': ['mean_winkel', 1, 0, len(means_angle)+1, 0],
                'name':       col,
                'values':     ['mean_winkel', 1, n+1, len(means_angle)+1, n+1],
                'gap':        10,
            })
        
    chart1.set_size({'width': 800, 'height': 500})
    chart2.set_size({'width': 800, 'height': 500})
    chart3.set_size({'width': 800, 'height': 500})
    chart4.set_size({'width': 800, 'height': 500})
    
    worksheet = workbook.worksheets()[0]
    
    worksheet.insert_chart('B{}'.format(row_chart), chart1)
    worksheet.insert_chart('O{}'.format(row_chart), chart2)
    worksheet.insert_chart('B{}'.format(str(int(row_chart)+30)), chart3)
    worksheet.insert_chart('O{}'.format(str(int(row_chart)+30)), chart4)
    # worksheet.insert_chart('B10', chart1)
    # worksheet.insert_chart('O10', chart2)
    # worksheet.insert_chart('B40', chart3)
    # worksheet.insert_chart('O40', chart4)
        
    writer.save()
finally:
    writer.save()
