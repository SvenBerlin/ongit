# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 09:43:50 2017

@author: sbergmann
- Programm zum Auslesen der CSV-Dateien des Goniometers LCS-100-G-10W
- auszuwertene Messdateien in einen Ordner ablegen und den Ordnerpfad eintragen
  es werden automatisch alle Dateien ausgelesen

files       Liste aller auszuwertenen Dateien
sumdata     globale Liste für alle Abstrahlcharakteristika
radInt      Werte der Abstrahlcharakteristik fü die intensitätsstärkste Wellenlänge
data        lokale liste des aktuell ausgewerteten Datensatzes
specInt     lokale Liste für die spektralen Intensitäten
wl          Liste für die Wellenlängen
maximum     intensitätsstärkste Wellenlänge
currmax     Laufvariable zur Ermittlung von "maximum"
f           Initialisierung der Interpolationsfunktion
xnew        neue, fein aufgelöste Wellenlängen-Schritte
ynew        interpolierte Intensitäten fuer f(xnew)
"""
import os as os
import csv as csv
import glob as glob
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

mainfolder=os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\9_Optics\opt_Bauteile_builds\LED_PCii_420nm_BL-LBVT3N__30_35__C-NB_DS')
#mainfolder=os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\95741_Mustang  Fusion Colorimeter\9_Optics\opt_Bauteile_builds\LED_NSPW310DS\alt')
files = glob.glob(mainfolder+"\\*.csv")
sumdata = [] #globale Liste für alle csv files
globradInt = [] #globale Liste für alle Abstrahlcharakteristika
erg=[]
fwhm=[]
ang_id = 52 
wl_id = 106

for filename in files:
    data = [] #lokale Liste für das jeweils aktuelle csv file
    specInt = [] #Liste für die spektralen Intensitäten
    radInt = []
    wl = [] #Liste für die abgetasteten Wellenlängen
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)# füge alle Reihen einer Datei in einer Liste zusammen        
    sumdata.append(data)# füge alle Listen der Dateien zusammen
"""  FÜR AUTOMATISCHES FINDEN
    #FINDE INTENSITÄTSSTÄRKSTE WELLENLÄNGE    
#    maximum = 0 # variablen zum ermitteln der intensitätsstärksten Wellenlänge
#    currVal = 0 # aktuell verarbeiter Wert
#    for punkte in range(46,np.size(data,0)):
#        currVal = max([float(i) for i in sumdata[-1][punkte][2:]]) # winkelabh. Intensitäten für gemessene Wellenl.
#        if currVal > maximum:
#            maximum = currVal
#            wl_id = punkte # Listenindex der bisher intensitätstärksten Wellenlänge
#            ang_id = np.argmax([float(i) for i in sumdata[-1][punkte][2:]])+2#Listenindex des zur intensiätsstärksten Wellenlänge dazugehörigen Winkels
#    #oder: Wellenlänge selbst bestimmen (360nm-1000nm, id von 46-686)
##   wl_id = 106 #id 106 entspricht 420nm - Auskommentieren stärkste Wellenlänge gesucht werden soll
#    
#    #ERMITTLUNG ALLER MESSERWERTE AN EINER DEFINIERTEN POSITION
#    for punkte in range(46,np.size(data,0)):
#        # (id 52 für 0° oder ang_id: ermittle alle Messwerte an der intensitätsstärksten Position
#        ang_id = 52
#        specInt.append(float(sumdata[-1][punkte][ang_id])) #<<<<<<<<<<<
#        wl.append(int(sumdata[-1][punkte][0]))# ermittle die gemessenen Wellenlängen (einfaches Übertragen)

    # Werte der Abstrahlcharacteristik für intensitätsstärkste Wellenlänge ...
#    radInt.append([float(i) for i in sumdata[-1][wl_id][2:]])    
    # ...oder Werte der Abstrahlcharacteristik für alle Wellenlängen aufsummiert
#    for k in range(46,np.size(data,0)):
#        radInt.append([float(i) for i in sumdata[-1][k][2:]])
#    globradInt.append(np.sum(radInt,0))  
"""
    # ERSTELLE LISTEN DER ABSTRAHLCHARAKTERISTIKEN, DES WELLENLÄNGENBEREICHS UND DER SPEKTREN
    for punkte in range(46,np.size(data,0)):
        specInt.append(float(sumdata[-1][punkte][ang_id])) #<<<<<<<<<<<
        wl.append(int(sumdata[-1][punkte][0]))
        radInt.append([float(i) for i in sumdata[-1][punkte][2:]])
    globradInt.append(np.sum(radInt,0))     
    
    #FWHM - BERECHNUNG
    maxIdx = find_nearest(globradInt[-1],np.max(globradInt[-1]))
    posIdx = find_nearest(globradInt[-1][:maxIdx],np.max(globradInt[-1]/2))
    negIdx = find_nearest(globradInt[-1][maxIdx:],np.max(globradInt[-1]/2))
#    find_nearest(globradInt[-1],np.max(globradInt))
    fwhm.append(round(abs(float(sumdata[-1][8][posIdx+2]))+abs(float(sumdata[-1][8][negIdx+maxIdx+2])),1))
    print('\t\t FHWM: '+str(fwhm[-1])+'°') 
    
    # Interpolation der Messwerte im Bereich des Maximums (+/-10 Winkelschritt vom Maximum)
    f = interpolate.interp1d([float(i) for i in sumdata[-1][8][2:]],radInt[-1],'cubic')
    xnew = np.arange(float(sumdata[-1][8][np.argmax(radInt[-1])+10+2]),
                     float(sumdata[-1][8][np.argmax(radInt[-1])-10+2]),0.1)[::-1]
    ynew = f(xnew)
    print(filename.split('\\')[-1]+':  maximum @ '+sumdata[-1][8][ang_id]+'° (from data)\n\
                 maximum @ '+str(xnew[np.argmax(ynew)])+'° (interpolated)')
    
    #PLOT DER MESSUNGEN
    # plot aller Spektren bei 0°
    plt.figure(0, figsize=(8,6))
    ax1 = plt.plot(wl, specInt, label=filename.split('\\')[-1]+' @ '+sumdata[-1][8][ang_id]+'°')
    plt.title(filename.split('\\')[-1].split('_')[0]+' spectrum')
    plt.xlabel('wavelenght (nm)')
    plt.ylabel('intensity (W/sr-nm)')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    # plot aller Abstrahlcharakteristika (polar)
    plt.figure(1, figsize=(6,6))
    ax2 = plt.subplot(111, projection='polar')
    # absolut
    ax2.plot([float(i)*np.pi/180 for i in sumdata[-1][8][2:]],globradInt[-1], label=filename.split('\\')[-1])
    # normalisiert
#    ax2.plot([float(i)*np.pi/180 for i in sumdata[-1][8][2:]],[i/globradInt[-1][maxIdx] for i in globradInt[-1]], label=filename.split('\\')[-1])
#    ax2.set_xticks(np.pi/180. * np.linspace(180,  -180, 8, endpoint=False)) #erzeugt neuerdings Fehler
    ax2.set_theta_zero_location('N')
    ax2.set_rlabel_position(150)
    ax2.set_title(filename.split("\\")[-1].split("_")[0]+' radiation chraracteristics')
    ax2.grid(True)
    ax2.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.)
    
    #ERGEBNISSE IN TABELLENFORM    
    # erg = [filename, max cd, max I]
    erg.append([filename.split("\\")[-1].split("_")[0],np.max([float(i) for i in sumdata[-1][10][2:]]),
                np.max([float(i) for i in sumdata[-1][11][2:]])])
