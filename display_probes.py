# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:04:14 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

# Tutorial: https://build-system.fman.io/pyqt5-tutorial
# --> https://doc.qt.io/

import pandas as pd
# import random
# import time
import devdata as dv
date = dv.dvtime(formatmode='dformat_dateiname')
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QComboBox,QGridLayout,QSizePolicy,QMessageBox, QApplication,QWidget,QLineEdit,QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from PyQt5 import QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.figure import Figure
from selenium import webdriver
#%% APP
class APP(QMainWindow):
    
    def __init__(self,link,topic):
        super().__init__()

        self.title = 'SC1000'
        self.topic = None
        self.ip = None
        # self.file = '{}_{}.csv'.format(date,self.topic)
        self.left = 50
        self.top = 50
        self.width = 1400
        # self.df = pd.DataFrame(columns=['SN', 'actVal', 'Einheit','Notiz', 'DateTime'])
        self.height = 800
        self._limits = [0,-50,-100,-500]
        self._setTimer = {'1 Sekunde':1000,
                          '5 Sekunden': 5000,
                          '10 Sekunden': 10000,
                          '30 Sekunden': 30000,
                          '60 Sekunden': 60000,
                          '5 Minuten': 300000,
                          '10 Minuten': 600000,}
        self.limit_plot = 0
        self.status = True
        self.browser = None
        self.connected = False
        self._displayStyle = 'font: bold 28px;border: 1px solid black;background: white;'
        self.link = link
        self.cnt = 0
        self.message = ''
        self.ids = 'p0 p1 p2 p3 p4 p5 p6 p7'.split() 
        

        self.initUI()
         
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setStyleSheet("QMainWindow{background-color: rgba(0,152,219,255)};")
                              
        
        self.grid_layout = QGridLayout(self)
        # self.connectSC1000()
        self.setLayout(self.grid_layout)
        # while True:
        #     try:
        #         self.setupProbes()
        #         break
        #     except:
        #         print('\rZugang aktualisieren%s' % ((self.cnt%6)*'.'+(5-(self.cnt%6))*' '), end = '\r')
        #         self.cnt += 1
        #         pass
        # self.createProbeWindow()
        
        self.logo = QLabel(self)
        self.pixmap = QPixmap(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\FAST\Fast - Verifizierungen 3010\ULTRATURB LED\Optik\py\logo.px')
        # self.logo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.logo.setPixmap(self.pixmap)
        self.grid_layout.addWidget(self.logo,0,0,1,1)
        
        
        self.topicLabel = QLineEdit(self)
        self.topicLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.topicLabel.setText('Projektname')
        self.topicLabel.setToolTip('Trage den Projektnamen ein')
        # self.grid_layout.addWidget(self.subwidget,0,1,1,1)

        self.ip_label= QLineEdit(self)
        self.ip_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ip_label.setText('IP')
        # self.ip_label.text('IP')
        self.ip_label.setToolTip('Trage IP des SC1000 ein')
        
        self.conbtn = QPushButton('Connect', self)
        self.conbtn.setToolTip('Verbinde mit SC1000')
        self.conbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.conbtn.clicked.connect(self.establish_connection)

        self.subBox = QGridLayout(self)
        self.subBox.addWidget(self.topicLabel,0,0)
        self.subBox.addWidget(self.ip_label,1,0)
        self.subBox.addWidget(self.conbtn,1,1)
        self.grid_layout.addLayout(self.subBox, 0,1,1,1)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid_layout.addWidget(self.canvas,0,3,21,6)


        self.startbtn = QPushButton('START', self)
        self.startbtn.setToolTip('Beginnt eine Messung im gewählten Messintervall')
        self.startbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.grid_layout.addWidget(self.startbtn,21,3,4,2)
        self.startbtn.clicked.connect(self.start_app)
        self.startbtn.setStyleSheet("QPushButton {background-color: rgba(230,230,230,255); \
                                    border-style: outset; \
                                    border-width: 2px; \
                                    border-color: gray;\
                                    font: 14px; \
                                    border-radius: 10px;}") 
        
        self.comboTimer= QComboBox(self)
        self.comboTimer.setToolTip('Auswahl des Messintervalls')
        self.comboTimer.setEditable(True)
        for elm in self._setTimer:
            self.comboTimer.addItem(elm)
        line_edit = self.comboTimer.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)         
        self.grid_layout.addWidget(self.comboTimer,21,5,1,2)
        
        self.setSection= QLineEdit(self)
        self.setSection.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSection.setToolTip('Suffix für Dateinamen bei neuem Abschnitt')
        self.grid_layout.addWidget(self.setSection,22,5,1,1)
        
        self.newFile = QPushButton('neuer Abschnitt', self)
        self.newFile.setToolTip('erstellt eine neue Messdatei zur besseren Auseinanderhaltung')
        self.grid_layout.addWidget(self.newFile,22,6,1,1)
        self.newFile.clicked.connect(self.create_new_file)                

        self.pltbtn = QPushButton('Plot anpassen (alles)', self)
        self.pltbtn.setToolTip('Plotte alles, die letzten 50, 100 oder 500 Datenpunkte')
        self.grid_layout.addWidget(self.pltbtn,23,5,1,2) #1,5
        self.pltbtn.clicked.connect(self.limitplot)
        
        self.screenshot = QPushButton('Screenshot', self)
        self.screenshot.setToolTip('speichert ein Screenshot mit Datum-Zeit-Stempel')
        self.grid_layout.addWidget(self.screenshot,24,5,1,2)
        self.screenshot.clicked.connect(self.take_screenshot)
        
        self.quitbtn = QPushButton('EXIT', self)
        self.quitbtn.setToolTip('Beendet die aktuelle Messung und schließt das Programm')
        self.quitbtn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.grid_layout.addWidget(self.quitbtn,21,7,4,2)
        self.quitbtn.clicked.connect(self.close_app)
        self.quitbtn.setStyleSheet("QPushButton {background-color: rgba(230,230,230,255); \
                                    border-style: outset; \
                                    border-width: 2px; \
                                    border-color: gray;\
                                    font: 14px; \
                                    border-radius: 10px;}") 
    
        self._ax = self.canvas.figure.subplots()
        self.widget = QWidget()
        self.widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.widget)
        
        self.recent_ip()
        self.show()
    
    def recent_ip(self):
        try:
            f = open('ip.bin','r')
            self.ip = f.read()
            self.ip_label.setText(self.ip)
        except:
            pass
    
    def establish_connection(self):
        self.ip = self.ip_label.text()
        if self.ip == 'IP':
            QMessageBox.about(self, 'Meldung','Bitte IP eingeben')
        else:
            f = open('ip.bin','w+')
            f.write(self.ip)
            f.close()
            self.connectSC1000()
            while True:
                try:
                    self.setupProbes()
                    break
                except:
                    print('\rZugang aktualisieren%s' % ((self.cnt%6)*'.'+(5-(self.cnt%6))*' '), end = '\r')
                    self.cnt += 1
                    pass
            self.createProbeWindow()
    
    def create_new_file(self):
        self.file = '{}_{}_{}.csv'.format(dv.dvtime(formatmode='dformat_dateiname'),self.topic,self.setSection.text())
        self.df = pd.DataFrame(columns=['SN', 'actVal', 'Einheit','Notiz', 'DateTime'])
        
    def take_screenshot(self):
        self.canvas.print_figure(dv.dvtime(formatmode='dformat_dateiname')+'.jpg')
    
    def close_app(self):
        reply = QMessageBox.question(
                self, "Beenden",
                "Messung wirklich beenden?",
                QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            try:
                # self.canvas_timer.stop()
                self.probe_timer.stop()
                self.browser.quit()
            except:
                pass
            self.close()
            app.quit()
            # sys.exit()
        else:
            pass
        
    def start_app(self):
        # self.canvas_timer = self.canvas.new_timer(
        #     self._setTimer[self.comboTimer.currentText()], [(self._update_canvas, (), {})])
        # self.canvas_timer.start()
        
        # self.connectSC1000()
        # self.createProbeWindow()
        if not self.connected:
            QMessageBox.about(self, 'Meldung','Bitte zunächst eine Verbingund mit dem SC1000 herstellen')
        else:
            self.topic = self.topicLabel.text()
            self.probe_timer = QTimer()
            self.probe_timer.setInterval(self._setTimer[self.comboTimer.currentText()])
            self.probe_timer.timeout.connect(self.read_probes)
            self.probe_timer.start()
            self.comboTimer.setEnabled(False)
            self.create_new_file()
    
    def limitplot(self):
        self.limit_plot = int((self.limit_plot+1)%4)
        if self.limit_plot == 0:
            self.pltbtn.setText('Plot anpassen (alles)')
        else:
            self.pltbtn.setText('Plot anpassen (die letzten {})'.format(abs(self._limits[self.limit_plot])))
    
    def get_text(self,num):
        if num == 0:
            return self.info_p0.text()
        if num == 1:
            return self.info_p1.text()
        if num == 2:
            return self.info_p2.text()
        if num == 3:
            return self.info_p3.text()
        if num == 4:
            return self.info_p4.text()
        if num == 5:
            return self.info_p5.text()
        if num == 6:
            return self.info_p6.text()
        if num == 7:
            return self.info_p7.text()        
        
    def connectSC1000(self):        
        LOGINURL = 'http://{}/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'.format(self.ip)
        chromedriver = 'C:\\chromedriver.exe'
        if self.browser is None:
            self.browser = webdriver.Chrome(chromedriver)
        try: 
            self.browser.get(LOGINURL)
            self.password = self.browser.find_element_by_name("password")
            self.button = self.browser.find_elements_by_xpath('//input[@type="submit"]')[0]
        except:
            self.connected = True
        if not self.connected:
            self.password.send_keys("MAX1000")        
            self.button.click() 
            self.connected = True
    
    def _update_canvas(self):
        try:
            df = self.df 
            df['DateTime']=pd.to_datetime(df['DateTime'])
            df['SN']=df['SN'].apply(lambda x: str(x))
            self._ax.clear()

            for sn in df['SN'].unique().tolist():
                temp = df[df['SN']==sn]
                von = self._limits[self.limit_plot]
                self._ax.plot(temp['DateTime'][von:],temp['actVal'][von:],label=sn)
                # self._ax.plot(temp['DateTime'],temp['actVal'],label=sn)
                self._ax.grid(True)
                self._ax.set_title(self.topic)
                self._ax.set_xlabel('DateTime')
                ylabel = '{} {}'.format(df['Groesse'][0],df['Einheit'][0])
                self._ax.set_ylabel(ylabel)
                self._ax.legend()
                self._ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y - %H:%M:%S'))
                self._ax.xaxis.set_tick_params(rotation=45)
                self._ax.set_ylim(min(df['actVal'][von*int(len(self.probes)):])*0.9,max(df['actVal'][von*int(len(self.probes)):])*1.1)
                self.figure.tight_layout()
            self._ax.figure.canvas.draw()     
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
            self.label_p0.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p0,1,0) 
            self.info_p0= QLineEdit(self)
            self.info_p0.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p0,1,1,1,1) 
            self.p0=QLabel()
            self.p0.setAlignment(Qt.AlignCenter)
            self.p0.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p0,2,0,2,2)            
        if cnt>1:
            self.label_p1= QLabel()
            self.label_p1.setText(self.probes['p1'])
            self.label_p1.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p1,4,0) 
            self.info_p1= QLineEdit(self)
            self.info_p1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p1,4,1,1,1) 
            self.p1=QLabel()
            self.p1.setAlignment(Qt.AlignCenter)
            self.p1.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p1,5,0,2,2)
        if cnt>2:
            self.label_p2= QLabel()
            self.label_p2.setText(self.probes['p2'])
            self.label_p2.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p2,7,0) 
            self.info_p2= QLineEdit(self)
            self.info_p2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p2,7,1,1,1) 
            self.p2=QLabel()
            self.p2.setAlignment(Qt.AlignCenter)
            self.p2.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p2,8,0,2,2)
        if cnt>3:
            self.label_p3= QLabel()
            self.label_p3.setText(self.probes['p3'])
            self.label_p3.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p3,10,0,)
            self.info_p3= QLineEdit(self)
            self.info_p3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p3,10,1,1,1) 
            self.p3=QLabel()
            self.p3.setAlignment(Qt.AlignCenter)
            self.p3.setStyleSheet(self._displayStyle)
            self.grid_layout.addWidget(self.p3,11,0,2,2)
        if cnt>4:
            self.label_p4= QLabel()
            self.label_p4.setText(self.probes['p4'])
            self.label_p4.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p4,13,0,) 
            self.info_p4= QLineEdit(self)
            self.info_p4.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p4,13,1,1,1) 
            self.p4=QLabel()
            self.p4.setAlignment(Qt.AlignCenter)
            self.p4.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p4,14,0,2,2)
        if cnt>5:
            self.label_p5= QLabel()
            self.label_p5.setText(self.probes['p5'])
            self.label_p5.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p5,16,0,) 
            self.info_p5= QLineEdit(self)
            self.info_p5.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p5,16,1,1,1) 
            self.p5=QLabel()
            self.p5.setAlignment(Qt.AlignCenter)
            self.p5.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p5,17,0,2,2)
        if cnt>6:
            self.label_p6= QLabel()
            self.label_p6.setText(self.probes['p6'])
            self.label_p6.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p6,19,0,) 
            self.info_p6= QLineEdit(self)
            self.info_p6.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p6,19,1,1,1) 
            self.p6=QLabel()
            self.p6.setAlignment(Qt.AlignCenter)
            self.p6.setStyleSheet(self._displayStyle)
            self.grid_layout.addWidget(self.p6,20,0,2,2)
        if cnt>7:
            self.label_p7= QLabel()
            self.label_p7.setText(self.probes['p7'])
            self.label_p7.setStyleSheet('font: bold 16px')
            self.grid_layout.addWidget(self.label_p7,22,0,)
            self.info_p7= QLineEdit(self)
            self.info_p7.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            self.grid_layout.addWidget(self.info_p7,22,1,1,1) 
            self.p7=QLabel()
            self.p7.setAlignment(Qt.AlignCenter)
            self.p7.setStyleSheet(self._displayStyle )
            self.grid_layout.addWidget(self.p7,23,0,2,2)
            
    def read_probes(self):

        try:                
            self.tables = pd.read_html(self.link)
    
            for t,p in enumerate(self.probes.values()):
                val = float(self.tables[t*2].loc[1,1].split()[0])
                einheit = self.tables[t*2].loc[1,1].split()[1]
                temp = pd.DataFrame({'SN':[self.tables[t*2].loc[0,1].split()[-1]],
                                      'actVal':[val],
                                      'Groesse':[self.tables[t*2].loc[1,0]],
                                      'Einheit':[einheit],
                                      'Notiz':[self.get_text(t)],
                                      'DateTime':[pd.to_datetime(' '.join(self.tables[t*2].loc[1,1].split()[-2:]))]})
                # if (len(self.df) == 0) or (not temp.iloc[-1].equals(self.df.iloc[-1])):
                self.df = self.df.append(temp,ignore_index=True, sort=True)

                if t==0:
                    self.p0.setText(' '.join([str(val),einheit]))
                if t==1:
                    self.p1.setText(' '.join([str(val),einheit]))
                if t==2:
                    self.p2.setText(' '.join([str(val),einheit]))
                if t==3:
                    self.p3.setText(' '.join([str(val),einheit]))
                if t==4:
                    self.p4.setText(' '.join([str(val),einheit]))
                if t==5:
                    self.p5.setText(' '.join([str(val),einheit]))
                if t==6:
                    self.p6.setText(' '.join([str(val),einheit]))
                if t==7:
                    self.p7.setText(' '.join([str(val),einheit]))

            self.df.to_csv(self.file,index=False)
            self._update_canvas()

        except:
            self.connected = False
            self.connectSC1000()
            pass
 #%%  Main     
if __name__ == '__main__':

    link = 'http://10.130.22.122/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'
    topic = 'Ultraturb_verification'


    app = QApplication(sys.argv)
    ex = APP(link,topic)
    sys.exit(app.exec_())

 #%% tbd
# Aufteilung in QVB bzw. QHB 
# zeitlich: loop > iterrows > apply > vectorize > numpy
# Abspeichern der CSV Datei und Anzeigen des aktuellen Wertes innerhalb des loops?