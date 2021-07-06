
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 07:39:59 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""



import pandas as pd
from enum import Enum, Flag, auto

class OKFAIL(Enum):
    FAIL = 0.1
    REBUILD = 0.05
    OK = 0.01

vals = [0.05,0.1,0.1,0.01]
pd.Series(vals).apply(lambda x: OKFAIL(x))
[OKFAIL(x).name for x in vals ]     

Animal = Enum('Animal', 'ANT BEE CAT DOG') 
Animal.ANT
list(OKFAIL)

class Color(Flag):
    BLACK = 0
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    WHITE = RED | BLUE | GREEN
    

class Planet(Enum):
    MERCURY = (3.303e+23, 2.4397e6)
    VENUS   = (4.869e+24, 6.0518e6)
    EARTH   = (5.976e+24, 6.37814e6)
    MARS    = (6.421e+23, 3.3972e6)
    JUPITER = (1.9e+27,   7.1492e7)
    SATURN  = (5.688e+26, 6.0268e7)
    URANUS  = (8.686e+25, 2.5559e7)
    NEPTUNE = (1.024e+26, 2.4746e7)
    def __init__(self, mass, radius):
        self.mass = mass       # in kilograms
        self.radius = radius   # in meters
    @property
    def surface_gravity(self):
        # universal gravitational constant  (m3 kg-1 s-2)
        G = 6.67300E-11
        return G * self.mass / (self.radius * self.radius)

Planet.EARTH.value

Planet.EARTH.surface_gravity
    






import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
#arr = [[12345,12345,12345,12345,12345,12345,12345,12345,12345,12345,32453,32453,32453,32453,32453,32453,32453,32453,32453,32453],
#       'one two three four five six seven eight nine ten'.split()*2]
#
#tup = list(zip(*arr))
#index = pd.MultiIndex.from_tuples(tup, names=['sn', 'VAAxx'])
#df = pd.Series(np.random.randn(20), index=index)
#
#
#iterables = [['bar', 'baz', 'foo', 'qux'], ['one', 'two']]
#
#index=pd.MultiIndex.from_product(iterables, names=['first', 'second'])
#df2 = pd.Series(np.random.randn(8), index=index)


df = pd.read_csv(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\DFCA PO4\Daten-Topf\Svens Daten\2mm Blende\dv_blendenversuch20180925_te_2mmBlende_dt_2018-10-05T144645.csv')

df2=df.drop(df.index[np.isnan(df.MESSWERT_LED3)])
df2.sort_values(by=['reg2','reg1'],inplace=True)

plt.plot(df2['MESSWERT_LED3'])



### DOUGHNUT

path = r'C:\Users\Public\Documents\Doughnut_BurnIn_Laserteam\zumMontageordner\defect\VRFY_LXG445.99.10112_AU1870219_SN1870219_20190213_1156.csv'    
h = pd.read_table(path)    
skip = h[h=='[Log]'].dropna().index.values[0]
cols = h.iloc[skip+1][0].split(',')
idx = cols.index('-')
ncol=len(cols)
df = pd.read_csv(path,names=list(range(0,ncol)))
df.drop(columns=idx, inplace=True)
save = 'testDough.csv'
h.to_csv(save,index=False, header=False)

''.join([x+',' for x in h.iloc[skip+1].iloc[0].split(',') if '-' not in x])[:-1]
for num, elm in enumerate(h.iloc[skip+1:].values.tolist()):
    try:
        h.iloc[skip+num+1]=''.join([x+',' for x in elm[0].split(',') if '-' not in x])[:-1]
    except:
        pass
    
    
pythonpath = os.path.abspath(r'C:\Users\Public\Decuments\Python Scripts\forpythonpath')
try:
    sys.path.index(pythonpath) # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(pythonpath)