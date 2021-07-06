# -*- coding: utf-8 -*-
"""
Created on Mon May  3 11:41:47 2021

@author: sbergmann
"""
'''
Ordnestruktur
-Aquarius_Simulation
        -aquarius_simulation.py
        -data
            -files
        -output
            -für screenshots/Speicherungen
'''



import pandas as pd
import numpy as np
import glob as glob
import os as os
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

def func(x,a,b,c,d,e):
    return a*x**4+b*x**3+c*x**2+d*x+e

def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


reagenz_path = r''

reagenz = {'path':reagenz_path,
            'Ext':100,
            'po4_ch':380,
            'po4_gem':3.268,
            'sd':10,
            'dfca_sd':0,
            'po4_anteil':0,
            'ratio':0,}
reagenz['po4_ch_gem'] = reagenz['po4_ch']/reagenz['Ext']

# led_path = r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\Python\Tools\Aquarius_Simulation\data'
# files_led = glob.glob(led_path+'\\*.csv')
# leds = [dict({'path':f,'df':pd.read_csv(f)} for f in files_led)]

data_path = r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\Python\Tools\Aquarius_Simulation\data'
files = glob.glob(data_path+'\\*.csv')
# LED_BEZEICHNUNG_LAMBDA.csv
# FILTER_BEZEICHNUNG_LAMBDA.csv
# DIODE_BEZEICHNUNG_BEREICH.csv
# REAGENZ_BEZEICHNUNG_BEREICH.csv
data = [dict({'path':f,
              'type':os.path.basename(f).split('_')[0],
              'name':os.path.basename(f).split('_')[1],
              'lambda':os.path.basename(f).split('_')[2].split('.')[0],
              'df':pd.read_csv(f)}) for f in files]

FILTER = [(n,x)[0] for n,x in enumerate(data) if x['type'] == "FILTER"]
LED = [(n,x)[0] for n,x in enumerate(data) if x['type'] == "LED"]
DIODE = [(n,x)[0] for n,x in enumerate(data) if x['type'] == "DIODE"]

i0 = 1000 #mV
delta_konzentration = 4
delta_int = 1
mwk = 0.01
dfca_sd = 17
po4_anteil = 1
ratio = 1/10
reagenz['dfca_sd'] = dfca_sd
reagenz['po4_anteil'] = po4_anteil
reagenz['ratio'] = ratio

c0 = reagenz['po4_ch']*reagenz['po4_anteil']*(1/(1+1/reagenz['ratio']))
po4_ist = np.arange(0,26)*delta_konzentration
c_po4_komplex = (c0+po4_ist/(1+reagenz['ratio'])+mwk)/2-(abs((c0+po4_ist/(1+reagenz['ratio'])+mwk)**2/4-c0*po4_ist/(1+reagenz['ratio'])))**0.5
c = c0-c_po4_komplex
# block korrekt

led = data[2]['df']
led = led.iloc[::2,:]
led = led.iloc[:-3]
led_rel = np.array(led['tau'])
led_abs = led_rel * i0

mean = sum(led.nm * led.tau)
sigma = sum(led.tau * (led.nm - mean)**2)
popt, pcov = curve_fit(func,led.nm , led.tau, p0 = [1, mean, sigma])
x_fit = np.arange(300,901)
y_fit = func(x_fit, *popt)
plt.plot(x_fit,y_fit)

intFilter = data[1]['df']
intFilter_rel = np.array(intFilter['t'])
plt.plot(intFilter_rel)
#photoelement
# lambd = np.arange(300,901)
lambd = np.array(led.nm)
polynom = np.array(data[0]['df']['1'])
rel_e = np.polyval(polynom,lambd)

ref = led_rel*rel_e*intFilter_rel

ext_vana_moly = [(np.array(data[3]['df']['ext_vanadat_molybdat'].iloc[100:]) * (x/reagenz['po4_ch_gem']) * (dfca_sd/reagenz['sd'])) for x in c]
ext_po4_komplex = [(np.array(data[3]['df']['ext_10mg_po4'].iloc[100:]) * (x/reagenz['po4_gem']) * (dfca_sd/reagenz['sd'])) for x in c_po4_komplex]
ext_h2o = np.array(data[3]['df']['ext_h2o'].iloc[100:]) * (dfca_sd/reagenz['sd'])
ext_sum = [ext_vana_moly[i] + ext_po4_komplex[i] + ext_h2o[i] for i in range(len(ext_vana_moly))]


int0_mV = led_abs * rel_e * intFilter_rel * delta_int * 10**-ext_sum[0]
int_reagenz_mV = [led_abs * rel_e * intFilter_rel * delta_int * 10**-i for i in ext_sum]

intC_int0 = [np.sum(i)/np.sum(int0_mV) for i in int_reagenz_mV]
ext_probe = -np.log10(intC_int0)

title = f'Simulations Ergebnis'
setup = f'''SYSTEM-SETUP\n\nSensor: {data[0]["name"]}
LED: {data[2]["name"]} ({data[2]["lambda"]})
Filter: {data[0]["name"]} ({data[0]["lambda"]})'''

mydpi = 96
fig,ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi))
lns1 = ax.plot(po4_ist, ext_probe, label="Ergebnis", marker='o',)
ax.set_xlabel('IST PO4-Konzentration (mg/L)')
ax.set_ylabel('Extinktion (E)')
ax.set_title(title)
ax.grid()
ax.legend()
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.75, 0.9, setup, transform=ax.transAxes,
        verticalalignment='top', bbox=props)
# plt.tight_layout()

### TBD

# interpolation im ganzzahligen Wellenlängenbereich/Umwandlung Goniometerdaten
# gui 
    # Auswahl der Komponenten
    # Einstellungen der Messbereiche
    # Plot + Tabelle
    # Speichern der Grafik bzw. Reports

