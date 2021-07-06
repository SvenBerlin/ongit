# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:04:14 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

# Tutorial: https://build-system.fman.io/pyqt5-tutorial
# --> https://doc.qt.io/

import pandas as pd
import random
import time
import devdata as dv
date = dv.dvtime(formatmode='dformat_dateiname')
from PyQt5.QtWidgets import QGridLayout,QSizePolicy, QApplication,QWidget,QLineEdit,QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtCore import *
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.figure import Figure

class APP(QWidget):
    
    def __init__(self,link):
        super().__init__()

        self.title = 'SC1000'
        self.file = '{}_Ultraturb_verify.csv'.format(date)
        self.left = 50
        self.top = 50
        self.width = 1200
        self.df = pd.DataFrame(columns=['SN', 'actVal', 'Einheit', 'DateTime'])
        self.height = 800
        self.status = True
        self.link = link
        self.message = ''
        self.ids = 'p0 p1 p2 p3 p4 p5 p6 p7'.split()
        self.pos = {'p0':[self.width*.05,self.height*.15],
                    'p1':[self.width*.30,self.height*.15],
                    'p2':[self.width*.55,self.height*.15],
                    'p3':[self.width*.80,self.height*.15],
                    'p4':[self.width*.05,self.height*.65],
                    'p5':[self.width*.30,self.height*.65],
                    'p6':[self.width*.55,self.height*.65],
                    'p7':[self.width*.80,self.height*.65],}
 
        self.initUI()
            
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        
        self.setupProbes()
        self.createProbeWindow()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid_layout.addWidget(self.canvas,0,2,24,4)
        # self.grid_layout.addWidget(self.canvas,0,1,(int(len(self.probes)-1))*3+2,4)
        self._dynamic_ax = self.canvas.figure.subplots()
        self._timer = self.canvas.new_timer(
            50, [(self._update_canvas, (), {})])
        self._timer.start()

        self.show()
        
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.read_probes)
        self.timer.start()
        
    def _update_canvas(self):
        try:
            df = self.df 
            df['DateTime']=pd.to_datetime(df['DateTime'])
            df['SN']=df['SN'].apply(lambda x: str(x))
            self._dynamic_ax.clear()

            for sn in df['SN'].unique().tolist():
                temp = df[df['SN']==sn]
                self._dynamic_ax.plot(temp['DateTime'],temp['actVal'],label=sn)
                self._dynamic_ax.grid(True)
                self._dynamic_ax.set_title('Ultraturb LED Verifikation')
                self._dynamic_ax.set_xlabel('DateTime')
                self._dynamic_ax.set_ylabel('Trübung FNU')
                self._dynamic_ax.legend()
                self._dynamic_ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
                self._dynamic_ax.xaxis.set_tick_params(rotation=90)
                self._dynamic_ax.set_ylim(min(df['actVal'])*0.9,max(df['actVal'])*1.1)
                # ax1.xaxis_date()
                # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
                self.figure.tight_layout()
            self._dynamic_ax.figure.canvas.draw()     
        except:
            pass
                
    def setupProbes(self):
        self.tables = pd.read_html(self.link)
        self.numOfProbes = int(len(self.tables)/2)
        self.probes = {}
        for i in range(self.numOfProbes):
            self.probes[self.ids[i]]=str(self.tables[i*2].loc[0,1].split()[-1])
    
    def createProbeWindow(self):
        cnt = int(len(self.probes))
        if cnt >0:
            self.label_p0= QLabel()
            self.label_p0.setText(self.probes['p0'])
            self.grid_layout.addWidget(self.label_p0,0,0,) 
            self.p0=QLabel()
            self.p0.setAlignment(Qt.AlignCenter)
            self.p0.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p0,1,0,2,1)            
        if cnt>1:
            self.label_p1= QLabel()
            self.label_p1.setText(self.probes['p1'])
            self.grid_layout.addWidget(self.label_p1,3,0,) 
            self.p1=QLabel()
            self.p1.setAlignment(Qt.AlignCenter)
            self.p1.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p1,4,0,2,1)
        if cnt>2:
            self.label_p2= QLabel()
            self.label_p2.setText(self.probes['p2'])
            self.grid_layout.addWidget(self.label_p2,6,0,) 
            self.p2=QLabel()
            self.p2.setAlignment(Qt.AlignCenter)
            self.p2.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p2,7,0,2,1)
        if cnt>3:
            self.label_p3= QLabel()
            self.label_p3.setText(self.probes['p3'])
            self.grid_layout.addWidget(self.label_p3,9,0,) 
            self.p3=QLabel()
            self.p3.setAlignment(Qt.AlignCenter)
            self.p3.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p3,10,0,2,1)
        if cnt>4:
            self.label_p4= QLabel()
            self.label_p4.setText(self.probes['p4'])
            self.grid_layout.addWidget(self.label_p4,12,0,) 
            self.p4=QLabel()
            self.p4.setAlignment(Qt.AlignCenter)
            self.p4.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p4,13,0,2,1)
        if cnt>5:
            self.label_p5= QLabel()
            self.label_p5.setText(self.probes['p5'])
            self.grid_layout.addWidget(self.label_p5,15,0,) 
            self.p5=QLabel()
            self.p5.setAlignment(Qt.AlignCenter)
            self.p5.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p5,16,0,2,1)
        if cnt>6:
            self.label_p6= QLabel()
            self.label_p6.setText(self.probes['p6'])
            self.grid_layout.addWidget(self.label_p6,18,0,) 
            self.p6=QLabel()
            self.p6.setAlignment(Qt.AlignCenter)
            self.p6.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p6,19,0,2,1)
        if cnt>7:
            self.label_p7= QLabel()
            self.label_p7.setText(self.probes['p7'])
            self.grid_layout.addWidget(self.label_p1,21,0,) 
            self.p7=QLabel()
            self.p7.setAlignment(Qt.AlignCenter)
            self.p7.setStyleSheet('font: bold 28px;border: 1px solid black;' )
            self.grid_layout.addWidget(self.p7,22,0,2,1)
            
    def read_probes(self):
        self.tables = pd.read_html(self.link)

        for t,p in enumerate(self.probes.values()):
            temp = pd.DataFrame({'SN':[self.tables[t*2].loc[0,1].split()[-1]],
                                  'actVal':[float(self.tables[t*2].loc[1,1].split()[0])],
                                  'Einheit':[self.tables[t*2].loc[1,1].split()[1]],
                                  'DateTime':[pd.to_datetime(' '.join(self.tables[t*2].loc[1,1].split()[-2:]))]})
            if (len(self.df) == 0) or (not temp.iloc[-1].equals(self.df.iloc[-1])):
                self.df = pd.concat([self.df,temp])
                self.df.reset_index(drop=True, inplace=True)
                self.df.to_csv(self.file,index=False)
                # print(self.p)
                if t==0:
                    self.p0.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==1:
                    self.p1.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==2:
                    self.p2.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==3:
                    self.p3.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==4:
                    self.p4.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==5:
                    self.p5.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==6:
                    self.p6.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
                if t==7:
                    self.p7.setText(' '.join([str(self.df[self.df['SN']==p]['actVal'].iloc[-1]),
                                    self.df[self.df['SN']==p]['Einheit'].iloc[-1]]))
        
if __name__ == '__main__':
    
    link = 'http://10.130.25.88/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'

    time.sleep(1)
    app = QApplication(sys.argv)
    ex = APP(link)
    sys.exit(app.exec_())
    