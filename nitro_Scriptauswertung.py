# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 07:43:17 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import os as os
from os.path import sep as sep
import glob as glob
import devdata as dv
import pandas as pd
date = dv.dvtime(formatmode='dformat_dateiname')

class NITROSCRIPT:
    '''
    Instanz der Klasse NITROSCRIPT. 
    
    Mit Anderen Worten: Erschaffe eine Variable vom Typ NITROSCRIPT um 
    Messdaten abfragen und auswerten zu können.
    Der angebenene Ordner wird auf einen gewählten Dateityp untersucht und die
    Dateien werden mittels devdata eingelesen und für eine Weiterverarbeitung
    in Excel bearbeitet. Die Auswertung erfolgt in einem Excel-Blatt inklusive
    Statistiken und Grafiken. Die Dateien werden mit einem Zeitstempel und der
    Seriennummer des überprüften Geräts versehen.
    Toleranzgrenzen werden definiert in Toleranz nach oben und Unter getrennt,
    Als Operator * für Toleranz in Prozent oder * bzw - für Absolute Abweichung.
    
    Parameter
    ---------
    path : string
        Pfad zu dem Ordner mit den auszuwertenden Messdaten
    
    tol : pandas DataFrame
        Enthält Informationen zu Toleranzen, deren Berechnungen, Achsenbeschriftungen,
        sowie Grafik-Positionen.
    
    ext : string
        Enthält Informationen zu dem gesuchten Dateityp (default: '*.csv')
    
    Ausgabe
    -------
    Instanz von NITROSCRIPT
    
    Attribute
    ---------
        path
        tol
        ext
        wiper
        data
        info
        merged
    
    Es wird die Auswertung in einem Excel Blatt mit Datumsstempel und Seriennummer erstellt.
                
    Funktionen
    ----------
    Siehe Methoden. 
    '''
    _wiper = []
    _data = []
    _info = []
    _merged = None
    
    def __init__(self, path, tol, ext='*.csv'):
        self.path = path
        self.tol = tol
        self.ext = ext
        
    def evaluate(self):
        '''führe ein Ablauf zur Auswertung aus'''
        self.get_files()
        self.read_csv()
        self.get_raw()
        self.split_df()
        self.get_serialnumbers()
        self.set_xlsfile_name()
        self.organize()
        self.create_spreadsheet()
    
    def get_files(self): 
        '''sammle alle Pfade des gewählten Dateityps im Verzeichnis auf'''
        self.files = glob.glob(self.path+sep+self.ext)
        assert (not not self.files), 'Es befinden sich keine Dateien mit der Dateiendung {} im Pfad {}'.format(self.ext,self.path)
        
    def read_csv(self): 
        ''' lese alle gefundenen Dateien mittels Devdata ein'''
        assert (not not self.files), 'Es wurden keine Dateien eingelesen'
        self.dflist = [dv.messung(f) for f in self.files]
    
    def get_info(self,df=None): 
        '''extrahiere Header-Informationen aus DataFrame'''
        if df is None:
            assert (hasattr(self,'dflist')), 'Es wurden keine Dateien eingelesen'
            df = self.dflist[-1]
        return df[(df['block'] == 'Comment') | (df['block'] =='Header')][['Type','actVal']]        
    
    def get_raw(self): 
        '''lese Daten unbearbeitet als csv ein'''
        assert (not not self.files), 'Es wurden keine Dateien eingelesen'
        self.rawlist = [pd.read_csv(f,sep='^', header=None) for f in self.files] # "^" kommt nicht vor, daher eignet sich dieses Zeichen zum Einlesen in Rohfassung
    
    def split_df(self): 
        '''unterteile DataFrame in separate DataFrames und bereite sie auf'''
        for n,df in enumerate(self.dflist): # trenne Wischer-Daten von restlichen
            # wiper = pd.notna(df['WiperDrivingSectionPeakCurrent_mA'])
            # df_wiper = df[(wiper) & (df['block']==df['block'].unique()[-1])][['DateTime','WiperPos','WiperDrivingSectionPeakCurrent_mA']]
            # df_wiper.reset_index(drop=True, inplace=True)
            # self._wiper.append(df_wiper)
            
            # data = pd.notna(df['mExtM2_M1']) 
            # df_data = df[data]
            # df['ErrorCode'][pd.notna(df['ErrMsg'])] = 1
            df.loc[pd.notna(df['ErrMsg']),'ErrorCode'] = 1 # n
            df_data = df[(pd.notna(df['mExtM2_M1'])) | (pd.notna(df['ErrMsg']))][1:] # ignoriere erste Messung (Dark) 
            df_data = df_data[df_data['block']==df_data['block'].unique()[-1]][self.tol['cols']]
            
            df_wiper = df.iloc[df_data.index-1][['DateTime','WiperPos','WiperDrivingSectionPeakCurrent_mA']]
            df_wiper.set_index(df_data.index,drop=True, inplace=True)
            # df_wiper.reset_index(drop=True, inplace=True)
            self._wiper.append(df_wiper)
            
            df_data['WiperDrivingSectionPeakCurrent_mA']=df_wiper['WiperDrivingSectionPeakCurrent_mA']
            self._data.append(df_data)
            
            df_info = self.get_info(df) # rufe Header-Informationen ab und füge Pfad hinzu
            df_info.loc[len(df_info)] = ['File', self.files[n]]
            self._info.append(df_info)
            
    def get_serialnumbers(self): 
        '''extrahiere die Seriennummer aus dem Dateinamen'''
        self.sn = [[s for s in os.path.basename(f).split('_') if 'SN' in s][0] for f in self.files]
    
    def set_xlsfile_name(self): 
        '''erstelle Excel-Dateinamen in Kombination aus der Seriennummer und des Datums'''
        self.xls = ['{}{}{}_{}.xlsx'.format(self.path, sep, date, sn) for sn in self.sn]
        
    def organize(self): 
        '''stelle alle Informationen in einem DataFrame zusammen'''
        self.merged = pd.DataFrame({'ordner':[self.path]*len(self.files),
                                    'Datei':self.files,
                                    'Seriennummer':self.sn,
                                    'df':self.dflist,
                                    'raw':self.rawlist,
                                    'Daten':self._data,
                                    'Wiper':self._wiper,
                                    'Info':self._info,
                                    'xls':self.xls})
        
    def create_spreadsheet(self): 
        '''erstelle für jede eingelesene Datei eine Excelauswertung'''
    # Auswertung erfolgt hier weitesgehend hard encoded. Eine denkbare Verbesserung wäre eine Schablone zu erstellen die dann eingelesen wird
        for idx, df in self.merged.iterrows():
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            writer = pd.ExcelWriter(df['xls'], engine='xlsxwriter')
            # speichere die gesammelten Informationen in separaten Tabellenblättern ab
            df['Info'].to_excel(writer, sheet_name='Header',index=False, header=False)
            df['Daten'].to_excel(writer, sheet_name='Data')
            df['Daten'].to_excel(writer, sheet_name='DataCopy')
            df['raw'].to_excel(writer,sheet_name='RawData',index=False, header=False)
            df['Wiper'].to_excel(writer, sheet_name='Wiper_Data')
            workbook = writer.book
            # füge eine Statistikseite hinzu (Statistik wurde mit Excel-Formeln erstellt, um in der
            # Auswertedatei "live" Manipulationen durchführen zu können)
            worksheet = workbook.add_worksheet('Statistics')
            for  n,col in enumerate(df['Daten']):
                    worksheet.write(0,n+1,col)
                    worksheet.write_formula(1,n+1,'=COUNT(Data!'+letters[n+1]+'2:'+letters[n+1]+str(len(df['Daten']))+')')
                    worksheet.write(8,n+1,uptol[n])
                    worksheet.write(9,n+1,lotol[n])
                    if col not in ['DateTime', 'WiperDrivingSectionPeakCurrent_mA']: # macht manuelles Löschen der nicht gewollten Spalten überflüssig
                    #    worksheet.write_formula(3,n+1,'=STDEV(Data!'+letters[n+1]+'2:'+letters[n+1]+str(len(df))+')')
                        worksheet.write_formula(4,n+1,'=max(Data!'+letters[n+1]+'2:'+letters[n+1]+str(len(df['Daten']))+')')
                        worksheet.write_formula(5,n+1,'=min(Data!'+letters[n+1]+'2:'+letters[n+1]+str(len(df['Daten']))+')')
                        worksheet.write_formula(6,n+1,'=AVERAGE(Data!'+letters[n+1]+'2:'+letters[n+1]+str(len(df['Daten']))+')')
                        worksheet.write_formula(10,n+1,'=Statistics!'+letters[n+1]+'7'+operator[n]+'Statistics!'+letters[n+1]+'9')
                        worksheet.write_formula(11,n+1,'=Statistics!'+letters[n+1]+'7'+operator[n]+'Statistics!'+letters[n+1]+'10')
                        worksheet.write_formula(13,n+1,'=IF('+'Statistics!'+letters[n+1]+'5'+'<'+'Statistics!'+letters[n+1]+'11,"PASS","_fail_")')
                        worksheet.write_formula(14,n+1,'=IF('+'Statistics!'+letters[n+1]+'6'+'>'+'Statistics!'+letters[n+1]+'12,"PASS","_fail_")')
                        worksheet.write_formula(16,n+1,'='+'Statistics!'+letters[n+1]+'5'+'-'+'Statistics!'+letters[n+1]+'6')
                        worksheet.write_formula(18,n+1,'='+'Statistics!'+letters[n+1]+'5'+'-'+'Statistics!'+letters[n+1]+'7')
                        worksheet.write_formula(19,n+1,'='+'Statistics!'+letters[n+1]+'7'+'-'+'Statistics!'+letters[n+1]+'6')
            
            txt = {1:'Anzahl', 4:'max', 5:'min', 6:'Mittelwert',8:'Toleranz',9:'Toleranz',
                    10:'obere Grenze',11:'untere Grenze', 13:'oben OK',14:'unten OK',
                    16:'Spanne',18:'Abw max +',19:'Abw max -'}
            [worksheet.write(elm[0],0,elm[1]) for elm in txt.items()]
            # füge in das Tabellenblatt "Graphics" für jede gewählte Datenspalte ein Linienplot hinzu
            worksheet = workbook.add_worksheet('Graphics')            
            for col in range(df['Daten'].shape[1]-1):
                    chart = workbook.add_chart({'type': 'line'})
                    chart.add_series({
                        'categories': ['Data', 1, 0, len(df['Daten'])+1, 0],
                        'name':       ['Data', 0, col+2],
                        'values':     ['Data', 1, col+2, len(df['Daten'])+1, col+2],
                        'gap':        10,
                    })
                    chart.set_legend({'position': 'bottom'})
                    chart.set_size({'width':1600,'height':600})
                    chart.set_x_axis({'name': self.tol['xlabels'][col]})
                    chart.set_y_axis({'name': self.tol['ylabels'][col], 'major_gridlines': {'visible': True}})
                    worksheet.insert_chart(positions[col], chart)
            # erstelle ein separates Tabellenblatt mit Grafiken zu den Wischerdaten
            worksheet = workbook.add_worksheet('Wiper_Graphs')
            chart = workbook.add_chart({'type': 'line'})
            chart.add_series({
                'categories': ['Wiper_Data', 1, 0, len(df['Wiper'])+1, 0],
                'name':       ['Wiper_Data', 0, 3],
                'values':     ['Wiper_Data', 1, 3, len(df['Wiper'])+1, 3],
                'gap':        10,
            })
            chart.add_series({
                'categories': ['Wiper_Data', 1, 0, len(df['Wiper'])+1, 0],
                'name':       ['Wiper_Data', 0, 2],
                'values':     ['Wiper_Data', 1, 2, len(df['Wiper'])+1, 2],
                'gap':        10,
                'line': {'tranparency':50,'width':1},
                'y2_axis': True,
            })
            
            chart.set_x_axis({'name': 'Time [s]',})# 'date_axis': False, 'num_format': 'yy-mm-dd hh:mm:ss',})
            chart.set_y_axis({'name': 'Current [mA]', 'major_gridlines': {'visible': True}})
            chart.set_y2_axis({'name':'1', })
            chart.set_size({'width':1600,'height':600})
            chart.set_title({'name': 'Wiper','overlay': True,})
            chart.set_legend({'position': 'bottom'})
            
            worksheet.insert_chart('A2', chart)
            writer.save()
            print('{} wurde erstellt...'.format(df['xls']))







if __name__ == '__main__':
    ordner = os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\Technik\Python\emv\Nitro')
    ext = '*EE*_*.csv'
    cols=['DateTime',
          'WiperDrivingSectionPeakCurrent_mA',
          'mExtM2_M1',
          'mExtM3_M1',
          'mExtM3_M2',
          'TemperatureFlashBoard',
          'HumidityFlashboard',
          'TemperatureMainboard',
          'HumidityMainboard',
          'MonitorVoltage_12V_Mainboard',
          'MonitorVoltage_12V_Flashboard',
          'MonitorVoltage_12V_WiperMotor',
          'DVCC_MonitorVoltage',
          'AVCC_MonitorVoltage',
          'AVEE_MonitorVoltage',
          'ADCVoltageActGain_M1',
          'ADCVoltageActGain_M2',
          'ADCVoltageActGain_M3',
          'ErrorCode',]
    
    uptol = ['+',0,20,20,20,1.5,1.1,1.5,1.1,1,1,1,0.05,0.05,0.05,1.07,1.07,1.07,0]
    lotol = ['-',0,-20,-20,-20,-1.5,0.9,-1.5,0.9,-1,-1,-1,-0.05,-0.05,-0.05,0.93,0.93,0.93,0]
    operator = ['+','+','+','+','+','+','*','+','*','+','+','+','+','+','+','*','*','*','*',]
    # positions = ['A2','A34','A66', 'A96','A128','A160', 'A192', 'A224','A256','A146','A162', 'A178','A194','A210', 'A226','A242','A258','A274','A290']
    xlabels = ['Time [s]', 'Time [s]', 'Time [s]', 'Time [s]', 'Time [s]', 'Time [s]', 'Time [s]', 'Time [s]', 'Time [s]','Time [s]','Time [s]','Time [s]', 'Time [s]', 'Time [s]', 'Time [s]','Time [s]', 'Time [s]', 'Time [s]']
    ylabels = ['Current [mA]', 'mExt', 'mExt','mExt','Temperature [C°]', 'Humidity[%]','Temperature [C°]', 'Humidity[%]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]','Voltage [V]']
    pos = 2
    positions =[('A'+str(pos+(32*n))) for n in range(len(xlabels))]
    
    tol = pd.DataFrame.from_dict({'cols':cols, 
                        'uptol':uptol,
                        'lotol':lotol,
                        'operator':operator,
                        'positions':positions,
                        'xlabels':xlabels,
                        'ylabels':ylabels},orient='index').T
    
    obj = NITROSCRIPT(ordner, tol, ext)
    obj.evaluate()