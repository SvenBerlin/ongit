# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 07:59:48 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

# Tutorial: https://build-system.fman.io/pyqt5-tutorial
# --> https://doc.qt.io/

import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QMainWindow,QComboBox,QGridLayout,QSizePolicy,QMessageBox, QApplication,QWidget,QLineEdit,QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.figure import Figure
import requests


#%% APP
class APP(QMainWindow):    
    def __init__(self):
        super().__init__()

        self.title = 'SC1000'
        self.topic = None
        self.ip = None
        self.left = 50
        self.top = 50
        self.width = 1400
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
        self.connected = False
        self._displayStyle = 'font: bold 28px;border: 1px solid black;background: white;'
        self.LOGINURL = 'http://{}/cgi-bin/SC1000'
        self.PROTECTEDPAGE = 'http://{}/cgi-bin/SC1000?Mode=9&UserID=1&AUTO_REFRESH=1'
        self.cnt = 0
        self._ids = 'p0 p1 p2 p3 p4 p5 p6 p7'.split() 

        self.initUI()
         
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setStyleSheet("QMainWindow{background-color: rgba(0,152,219,255)};")
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        
        self.logo = QLabel(self)
        self.pixmap = QPixmap(r'logo.px')
        self.logo.setPixmap(self.pixmap)
        self.grid_layout.addWidget(self.logo,0,0,1,1)        
        
        self.topic_label = QLineEdit(self)
        self.topic_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.topic_label.setPlaceholderText('Projektname')
        self.topic_label.setToolTip('Trage den Projektnamen ein')
        # self.grid_layout.addWidget(self.subwidget,0,1,1,1)

        self.ip_label= QLineEdit(self)
        self.ip_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ip_label.setPlaceholderText('IP')
        self.ip_label.setToolTip('Trage IP des SC1000 ein')
        
        self.connect_btn = QPushButton('Connect', self)
        self.connect_btn.setToolTip('Verbinde mit SC1000')
        self.connect_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.connect_btn.clicked.connect(self.establish_connection)
        
        self.elapsed_time = QLabel(self)
        self.elapsed_time.setText('00:00:00')
        self.elapsed_time.setAlignment(Qt.AlignCenter)
        self.elapsed_time.setStyleSheet('font: bold 20px')

        self.elapsed_time_section = QLabel(self)
        self.elapsed_time_section.setText('00:00:00')
        self.elapsed_time_section.setAlignment(Qt.AlignCenter)
        self.elapsed_time_section.setStyleSheet('font: bold 14px')

        self.sub_layout = QGridLayout(self)
        self.sub_layout.addWidget(self.topic_label,0,0,1,2)
        self.topic_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.sub_layout.addWidget(self.ip_label,1,0)
        self.sub_layout.addWidget(self.connect_btn,1,1)
        self.sub_layout.addWidget(self.elapsed_time,2,0,1,1)
        self.sub_layout.addWidget(self.elapsed_time_section,2,1,1,1)
        self.grid_layout.addLayout(self.sub_layout, 0,1,1,1)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid_layout.addWidget(self.canvas,0,3,21,6)


        self.start_btn = QPushButton('START', self)
        self.start_btn.setToolTip('Beginnt eine Messung im gewählten Messintervall')
        self.start_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.grid_layout.addWidget(self.start_btn,21,3,4,2)
        self.start_btn.clicked.connect(self.start_app)
        self.start_btn.setStyleSheet("QPushButton {font: 14px;}") 
                            #          min-width: 5em; \
                            # max-width: 10em;}") 
        
        self.combo_timer= QComboBox(self)
        self.combo_timer.setToolTip('Auswahl des Messintervalls')
        self.combo_timer.setEditable(True)
        for elm in self._setTimer:
            self.combo_timer.addItem(elm)
        line_edit = self.combo_timer.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)         
        self.grid_layout.addWidget(self.combo_timer,21,5,1,2)
        
        self.set_suffix= QLineEdit(self)
        self.set_suffix.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.set_suffix.setToolTip('Suffix für Dateinamen bei neuem Abschnitt')
        self.set_suffix.setPlaceholderText('suffix')
        self.grid_layout.addWidget(self.set_suffix,22,5,1,1)
        
        self.new_file = QPushButton('neuer Abschnitt', self)
        self.new_file.setToolTip('erstellt eine neue Messdatei zur besseren Auseinanderhaltung')
        self.grid_layout.addWidget(self.new_file,22,6,1,1)
        self.new_file.clicked.connect(self.create_new_file)                

        self.plot_btn = QPushButton('Plot anpassen (alles)', self)
        self.plot_btn.setToolTip('Plotte alles, die letzten 50, 100 oder 500 Datenpunkte')
        self.grid_layout.addWidget(self.plot_btn,23,5,1,2) #1,5
        self.plot_btn.clicked.connect(self.plot_interval)
        
        self.screenshot = QPushButton('Screenshot', self)
        self.screenshot.setToolTip('speichert ein Screenshot mit Datum-Zeit-Stempel')
        self.grid_layout.addWidget(self.screenshot,24,5,1,2)
        self.screenshot.clicked.connect(self.take_screenshot)
        
        self.quit_btn = QPushButton('EXIT', self)
        self.quit_btn.setToolTip('Beendet die aktuelle Messung und schließt das Programm')
        self.quit_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.grid_layout.addWidget(self.quit_btn,21,7,4,2)
        self.quit_btn.clicked.connect(self.close_app)
        self.quit_btn.setStyleSheet("QPushButton {font: 14px;}") 
    
        self._ax = self.canvas.figure.subplots()
        self.widget = QWidget()
        self.widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.widget)
        
        self.recent_ip()
        self.show()
        
    def timer(self,threadname):
        start = datetime.now()
        while True:
            end = datetime.now()-start
            print(end)  
            
    def recent_ip(self):
        try:
            f = open('ip.txt','r')
            self.ip = f.read()
            self.ip_label.setText(self.ip)
        except:
            pass
    
    def establish_connection(self):
        self.ip = self.ip_label.text()
        if self.ip == 'IP':
            QMessageBox.about(self, 'Meldung','Bitte IP eingeben')
        else:
            f = open('ip.txt','w+')
            f.write(self.ip)
            f.close()
            self.connect_sc1000()
            while True:
                try:
                    self.setup_probes()
                    break
                except:
                    print('\rZugang aktualisieren%s' % ((self.cnt%6)*'.'+(5-(self.cnt%6))*' '), end = '\r')
                    self.cnt += 1
                    pass
            self.createProbeWindow()
    
    def create_new_file(self):
        self.file = '{}_{}_{}.csv'.format(self.time_label(),self.topic,self.set_suffix.text())
        self.df = pd.DataFrame(columns=['SN', 'actVal', 'Einheit','Notiz', 'DateTime'])
        self.t0_section = datetime.now()
        
    def take_screenshot(self):
        self.canvas.print_figure(self.time_label()+'.jpg')
    
    def close_app(self):
        reply = QMessageBox.question(
                self, "Beenden",
                "Messung wirklich beenden?",
                QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            try:
                # self.canvas_timer.stop()
                # self.browser.quit()
                self.probe_timer.stop()
                del self._r
                # self.thread.exit()
            except:
                pass
            self.close()
            app.quit()
            # sys.exit()
        else:
            pass
    def time_label(self):
        return datetime.now().strftime(format='%Y%m%d_%H%M%S')
        
    def start_app(self):
        if not self.connected:
            QMessageBox.about(self, 'Meldung','Bitte zunächst eine Verbingund mit dem SC1000 herstellen')
        else:
            # self.thread = _thread
            # self.thread.start_new_thread(self.timer,('Timer',))
            self.topic = self.topic_label.text()
            self.probe_timer = QTimer()
            self.probe_timer.setInterval(self._setTimer[self.combo_timer.currentText()])
            self.probe_timer.timeout.connect(self.read_probes)
            self.probe_timer.start()
            self.combo_timer.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.create_new_file()
            self.t0 = datetime.now()
            self.t0_section = datetime.now()
    
    def plot_interval(self):
        self.limit_plot = int((self.limit_plot+1)%4)
        if self.limit_plot == 0:
            self.plot_btn.setText('Plot anpassen (alles)')
        else:
            self.plot_btn.setText('Plot anpassen (die letzten {})'.format(abs(self._limits[self.limit_plot])))
    
    def get_text(self,num):
        return self._display_list[num][1].text()
           
    def connect_sc1000(self):  
        self.LOGINURL = self.LOGINURL.format(self.ip)
        self.PROTECTEDPAGE = self.PROTECTEDPAGE.format(self.ip) 
        login_data = {
            'Mode': '1',
            'SetLanguage': '1',
            'password': 'MAX1000',
            }
        session_requests = requests.Session()
        self._r = session_requests.get(self.LOGINURL) 
        self._r = session_requests.post(self.LOGINURL,data=login_data)
        self._r = session_requests.get(self.PROTECTEDPAGE)
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
                self._ax.grid(True)
                self._ax.set_title(self.topic)
                self._ax.set_xlabel('DateTime',fontsize=8)
                ylabel = '{} {}'.format(df['Groesse'][0],df['Einheit'][0])
                self._ax.set_ylabel(ylabel,fontsize=8)
                self._ax.tick_params(axis='both', which='major', labelsize=8)
                self._ax.legend()
                self._ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y\n%H:%M:%S'))
                self._ax.xaxis.set_tick_params(rotation=45)
                self._ax.set_ylim(min(df['actVal'][von*int(len(self.probes)):])*0.9,max(df['actVal'][von*int(len(self.probes)):])*1.1)
                self.figure.tight_layout()
            self._ax.figure.canvas.draw()     
        except:
            pass
                
    def setup_probes(self):
        self.tables = pd.read_html(self.PROTECTEDPAGE.format(self.ip))
        # self.tables = pd.read_html(self.link.format(self.ip))
        self.numOfProbes = int(len(self.tables)/2)
        self.probes = {}
        for i in range(self.numOfProbes):
            self.probes[self._ids[i]]=str(self.tables[i*2].loc[0,1].split()[-1])
    
    def createProbeWindow(self):
        self._display_list=[]
        for n in range(int(len(self.probes))):
            lst = [QLabel(), QLineEdit(), QLabel()]
            lst[0].setText(self.probes['p'+str(n)])
            lst[0].setStyleSheet('font: bold 16px')
            lst[1].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
            lst[1].setPlaceholderText('Bezeichnung')
            lst[2].setAlignment(Qt.AlignCenter)
            lst[2].setStyleSheet(self._displayStyle)
            self._display_list.append(lst)
            self.grid_layout.addWidget(self._display_list[-1][0],n*3+1,0)
            self.grid_layout.addWidget(self._display_list[-1][1],n*3+1,1,1,1)
            self.grid_layout.addWidget(self._display_list[-1][2],n*3+2,0,2,2)
      

    def read_probes(self):
        try:
            now = datetime.now()
            passed_time = now-self.t0
            passed_time_section = now-self.t0_section
            # self.elapsed_time.setText(passed_time)
            # self.elapsed_time.setText(datetime.strftime(passed_time,'%H:%M:%S'))
            self.elapsed_time.setText(str(passed_time).split('.')[0])
            self.elapsed_time_section.setText(str(passed_time_section).split('.')[0])
            # print(str(passed_time).split('.')[0])               
            self.tables = pd.read_html(self.PROTECTEDPAGE.format(self.ip))
            # self.tables = pd.read_html(self.link.format(self.ip))
    
            for t,p in enumerate(self.probes.values()):
                val = float(self.tables[t*2].loc[1,1].split()[0])
                einheit = self.tables[t*2].loc[1,1].split()[1]
                temp = pd.DataFrame({'SN':[self.tables[t*2].loc[0,1].split()[-1]],
                                      'actVal':[val],
                                      'Groesse':[self.tables[t*2].loc[1,0]],
                                      'Einheit':[einheit],
                                      'Notiz':[self.get_text(t)],
                                      'DateTime':[pd.to_datetime(' '.join(self.tables[t*2].loc[1,1].split()[-2:]))]})
                self.df = self.df.append(temp,ignore_index=True, sort=True)

                self._display_list[t][2].setText(' '.join([str(val),einheit]))
                
            self.df.to_csv(self.file,index=False)
            self._update_canvas()

        except:
            self.connected = False
            self.connect_sc1000()
            pass
 #%%  Main     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = APP()
    sys.exit(app.exec_())

 #%% tbd (https://www.python.org/dev/peps/pep-0350/)
    
# FIXME: Aufteilung in QVB bzw. QHB. <SB d:34w p:2>
# FIXME: Performance: lesen und schreiben im separaten Thread?
# TODO: Theme anpassen (Material) <SB d:35w p:3>
# TODO: Variablen/Instanzen-Namen neu vergeben. <SB d:34w p:2>
# FIXME: Login via requests. <SB d:34w p:1> ERLEDIGT
# FIXME: Display Objekte in Container/Liste. <SB d:34w p:1> ERLEDIGT
# TODO: Daten im dformat. <SB d:34w p:1>
# IDEA: Logging Checkbox (z.B. ohne Grafik, nur Werte)
# IDEA: Abschnitt: Feld für Soll-Wert. Checkbox -> neues Dokument/Eintrag in aktuelle
# IDEA: globaler- und Abschnitts-Timer
# FIXME: SC1000 Zugangsdaten als App-Data (txt?) hinterlegen.
# IDEA: zeitlich: loop > iterrows > apply > vectorize > numpy. <SB d:34w p:3>
# RFE : Abspeichern der CSV Datei und Anzeigen des aktuellen Wertes innerhalb des loops? <SB d:34w p:3>