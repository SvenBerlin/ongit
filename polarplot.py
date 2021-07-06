# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:58:30 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import os as os
import matplotlib.pyplot as plt
import math
import pandas as pd

file = r'C:\Users\sbergmann\Desktop\copyto\Mappe1.xlsx'
df = pd.read_excel(file)
df['Theta'] = df['Theta'].apply(lambda x: x*(math.pi/180))
df['r'] = df['r'].apply(lambda x: x*1000)

ax = plt.subplot(111, projection='polar')
ax.plot(df.Theta, df.r)
# ax.set_rmax(2)
# ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks

ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.set_theta_zero_location("N")
pos=ax.get_rlabel_position()
ax.set_rlabel_position(pos-90)
ax.set_ylabel('mW', rotation=-90,)
ax.grid(True)

ax.set_title('Osram PLCC 2  HSMW-A101-R50J1', va='bottom')
plt.show()