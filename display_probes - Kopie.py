# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:04:14 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

# Tutorial: https://build-system.fman.io/pyqt5-tutorial
# --> https://doc.qt.io/

#from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout
#import sys
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QPalette
import pandas as pd
import random
import time
import devdata as dv
date = dv.dvtime(formatmode='dformat_dateiname')
import threading
import numpy as np


from PyQt5.QtWidgets import QSizePolicy,QFrame, QHBoxLayout,QMainWindow,QApplication,QWidget,QPushButton,QAction,QLineEdit,QMessageBox,QLabel,QDialog
#from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtTest, QtWidgets, QtCore, QtGui


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates
from matplotlib import rcParams
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import glob as glob

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class APP(QMainWindow):
    
    def __init__(self,link):
        super().__init__()
        
#        self.initUI()
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
        self.statusBar().showMessage('Ready')
        
        
        self.qbtn = QPushButton('Quit',self)
        self.qbtn.move(self.width*.85,self.height*.85)
        self.qbtn.clicked.connect(QApplication.instance().quit)
        
        menuquit = QAction('Quit',self)
        menuquit.setShortcut('Ctrl+q')
        menuquit.setStatusTip('Exit application')
        menuquit.triggered.connect(QApplication.instance().quit)
        
        self.setupProbes()
        self.createProbeWindow()

        self.show()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.read_probes)
        self.timer.start()
        
            
    def test(self):
        for i in range(2):
            if i ==0:
                self.p0.setText(str(np.random.randint(10)))
            if i ==1:
                self.p1.setText(str(np.random.randint(10)))
                
    def animate(self,i):
        try:
            df = pd.read_csv(self.file)
            df['DateTime']=pd.to_datetime(df['DateTime'])
            df['SN']=df['SN'].apply(lambda x: str(x))
        
            ax1.clear()
            for sn in df['SN'].unique().tolist():
                temp = df[df['SN']==sn]
                ax1.plot(temp['DateTime'],temp['actVal'],label=sn)
                ax1.grid(True)
                ax1.set_title('Ultraturb LED Verifikation')
                ax1.set_xlabel('DateTime')
                ax1.set_ylabel('Trübung FNU')
                ax1.legend()
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
                ax1.xaxis.set_tick_params(rotation=90)
                ax1.set_ylim(min(df['actVal'])*0.9,max(df['actVal'])*1.1)
                # ax1.xaxis_date()
                # ax1.xaxis.set_major_locator(plt.MaxNLocator(20))
                plt.tight_layout()
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
            self.p0=QLineEdit(self)
            self.p0.setAlignment(Qt.AlignCenter)
            self.p0.setStyleSheet('font: bold 28px;' )
            self.p0.move(self.pos['p0'][0],self.pos['p0'][1])
            self.p0.resize(self.width*0.2,self.height*.2)
            self.label_p0= QLabel(self)
            self.label_p0.setText(self.probes['p0'])
            self.label_p0.move(self.pos['p0'][0],self.pos['p0'][1]-5) 
        if cnt>1:
            self.p1=QLineEdit(self)
            self.p1.setAlignment(Qt.AlignCenter)
            self.p1.setStyleSheet('font: bold 28px;' )
            self.p1.move(self.pos['p1'][0],self.pos['p1'][1])
            self.p1.resize(self.width*0.2,self.height*.2)
            self.label_p1= QLabel(self)
            self.label_p1.setText(self.probes['p1'])
            self.label_p1.move(self.pos['p1'][0],self.pos['p1'][1]-5) 
        if cnt>2:
            self.p2=QLineEdit(self)
            self.p2.setAlignment(Qt.AlignCenter)
            self.p2.setStyleSheet('font: bold 28px;' )
            self.p2.move(self.pos['p2'][0],self.pos['p2'][1])
            self.p2.resize(self.width*0.2,self.height*.2)
            self.label_p2= QLabel(self)
            self.label_p2.setText(self.probes['p2'])
            self.label_p2.move(self.pos['p2'][0],self.pos['p2'][1]-5) 
        if cnt>3:
            self.p3=QLineEdit(self)
            self.p3.setAlignment(Qt.AlignCenter)
            self.p3.setStyleSheet('font: bold 28px;' )
            self.p3.move(self.pos['p3'][0],self.pos['p3'][1])
            self.p3.resize(self.width*0.2,self.height*.2)
            self.label_p3= QLabel(self)
            self.label_p3.setText(self.probes['p3'])
            self.label_p3.move(self.pos['p3'][0],self.pos['p3'][1]-5)
        if cnt>4:
            self.p4=QLineEdit(self)
            self.p4.setAlignment(Qt.AlignCenter)
            self.p4.setStyleSheet('font: bold 28px;' )
            self.p4.move(self.pos['p4'][0],self.pos['p4'][1])
            self.p4.resize(self.width*0.2,self.height*.2)
            self.label_p4= QLabel(self)
            self.label_p4.setText(self.probes['p4'])
            self.label_p4.move(self.pos['p4'][0],self.pos['p4'][1]-5) 
        if cnt>5:
            self.p5=QLineEdit(self)
            self.p5.setAlignment(Qt.AlignCenter)
            self.p5.setStyleSheet('font: bold 28px;' )
            self.p5.move(self.pos['p5'][0],self.pos['p5'][1])
            self.p5.resize(self.width*0.2,self.height*.2)
            self.label_p5= QLabel(self)
            self.label_p5.setText(self.probes['p5'])
            self.label_p5.move(self.pos['p5'+str(p)][0],self.pos['p5'][1]-5) 
        if cnt>6:
            self.p6=QLineEdit(self)
            self.p6.setAlignment(Qt.AlignCenter)
            self.p6.setStyleSheet('font: bold 28px;' )
            self.p6.move(self.pos['p6'][0],self.pos['p6'][1])
            self.p6.resize(self.width*0.2,self.height*.2)
            self.label_p6= QLabel(self)
            self.label_p6.setText(self.probes['p6'])
            self.label_p6.move(self.pos['p6'][0],self.pos['p6'][1]-5)
        if cnt>7:
            self.p7=QLineEdit(self)
            self.p7.setAlignment(Qt.AlignCenter)
            self.p7.setStyleSheet('font: bold 28px;' )
            self.p7.move(self.pos['p7'][0],self.pos['p7'][1])
            self.p7.resize(self.width*0.2,self.height*.2)
            self.label_p7= QLabel(self)
            self.label_p7.setText(self.probes['p7'])
            self.label_p7.move(self.pos['p7'][0],self.pos['p7'][1]-5) 
            
    def read_probes(self):
        self.tables = pd.read_html(self.link)
        
        # while True:
            # print('jo')
        for t,p in enumerate(self.probes.values()):
            temp = pd.DataFrame({'SN':[self.tables[t*2].loc[0,1].split()[-1]],
                                  'actVal':[float(self.tables[t*2].loc[1,1].split()[0])],
                                  'Einheit':[self.tables[t*2].loc[1,1].split()[1]],
                                  'DateTime':[pd.to_datetime(' '.join(self.tables[t*2].loc[1,1].split()[-2:]))]})
            # self.p0.setText(str(temp[temp['SN']==p]['actVal'][0]))
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
    