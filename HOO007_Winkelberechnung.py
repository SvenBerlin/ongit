# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 09:05:37 2021

@author: sbergmann
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def grad2bogen(winkel):
    return winkel*math.pi/180

def bogen2grad(bogen):
    return bogen*180/math.pi

def austritt(eintritt,n, kippung,dicke, abstand=500):
    versatz = math.cos(grad2bogen(eintritt))*2*math.tan(grad2bogen(bogen2grad(math.asin(math.sin(grad2bogen(eintritt))/n))-kippung))*dicke
    winkel = bogen2grad(math.asin(math.sin(math.asin(math.sin(grad2bogen(eintritt))/n)-grad2bogen(2*kippung))*n))
    projektion = math.tan(grad2bogen(eintritt-winkel))*abstand-versatz
    return versatz, winkel, projektion

dicke = math.cos(grad2bogen(9))*2.5
eintritt = 9
n=1.49
kippung = 2
abstand=500
print(f'Austrittswinkel({eintritt}°): {round(austritt(eintritt,n,kippung,dicke)[1],3)}°')

# k = np.arange(1.5,2.5,0.01)

kippungen = np.arange(1.5,2.5,0.01)
austrittswinkel =[]
for k in kippungen:
    austrittswinkel.append(austritt(eintritt,n,k,dicke))

df = pd.DataFrame(austrittswinkel,
                  columns=['Versatz', 'Winkel', 'Projektion'])
df['Kippung'] = kippungen

mydpi = 96
fig, ax = plt.subplots(figsize=(1920/mydpi, 1080/mydpi),dpi=mydpi)
ax.plot(df.Kippung, df.Projektion)
ax.axvline(2, linestyle='-.', color='r',linewidth=1)
ax.axhline(52.029, linestyle='-.', color='r',linewidth=1)
ax.text(1.9, 52.029, '52.029mm @ 2°', fontsize='small', va='center', ha='center', backgroundcolor='w')

# major_ticks = np.arange(1.5, 2.5, 0.5)
# minor_ticks = np.arange(1.5, 2.5, 0.1)

ax.set_xticks(np.arange(min(df.Kippung),max(df.Kippung),.1))
ax.set_xticks(np.arange(min(df.Kippung),max(df.Kippung),.05), minor=True)
ax.set_yticks(np.arange(math.floor(min(df.Projektion)),math.ceil(max(df.Projektion)),2))
ax.set_yticks(np.arange(math.floor(min(df.Projektion)),math.ceil(max(df.Projektion)),1), minor=True)

ax.grid(which='both')
ax.grid(which='minor', alpha=0.5)
ax.grid(which='major', alpha=0.85)

ax.set_xlabel('Verkippung')
ax.set_ylabel(f'Abstand der reflektierten Punkte in {abstand}mm Entfernung')


    
