# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 09:58:40 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

#TUTORIAL
### BASIC PLOT SETUP
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


sns.axes_style()
sns.set_style("ticks", rc={'axes.axisbelow': 'line',
 'axes.edgecolor': 'k',
 'axes.facecolor': 'w',
 'axes.grid': False,
 'axes.labelcolor': 'k',
 'axes.spines.bottom': True,
 'axes.spines.left': True,
 'axes.spines.right': True,
 'axes.spines.top': True,
 'figure.facecolor': 'w',
 'font.family': ['sans-serif'],
 'font.sans-serif': ['DejaVu Sans',
  'Bitstream Vera Sans',
  'Computer Modern Sans Serif',
  'Lucida Grande',
  'Verdana',
  'Geneva',
  'Lucid',
  'Arial',
  'Helvetica',
  'Avant Garde',
  'sans-serif'],
 'grid.color': '#b0b0b0',
 'grid.linestyle': '-',
 'image.cmap': 'viridis',
 'lines.solid_capstyle': 'projecting',
 'patch.edgecolor': 'k',
 'patch.force_edgecolor': False,
 'text.color': 'k',
 'xtick.bottom': True,
 'xtick.color': 'k',
 'xtick.direction': 'out',
 'xtick.top': False,
 'ytick.color': 'k',
 'ytick.direction': 'out',
 'ytick.left': True,
 'ytick.right': False})

#sns.plotting_context() 
sns.set_context('notebook', font_scale=1,rc={'axes.labelsize': 'medium',
 'axes.linewidth': 0.8,
 'axes.titlesize': 'large',
 'font.size': 10.0,
 'grid.linewidth': 0.8,
 'legend.fontsize': 'medium',
 'lines.linewidth': 1.5,
 'lines.markersize': 6.0,
 'patch.linewidth': 1.0,
 'xtick.labelsize': 'medium',
 'xtick.major.size': 3.5,
 'xtick.major.width': 0.8,
 'xtick.minor.size': 2.0,
 'xtick.minor.width': 0.6,
 'ytick.labelsize': 'medium',
 'ytick.major.size': 3.5,
 'ytick.major.width': 0.8,
 'ytick.minor.size': 2.0,
 'ytick.minor.width': 0.6})

colors = sns.xkcd_rgb
#PLOT
sns_plot = sns.lineplot(np.linspace(0,10,10), np.random.randint(5,10,10))
plt.show()
#sns.despine()
#sns.reset_defaults()
#sns_plot.savefig('output.png')


### Weiterführende Beispiele

df = sns.load_dataset('tips')
df = sns.load_dataset('iris')

def sinplot(flip=1):
    x = np.linspace(0,14,100)
    for i in range(1,5):
        plt.plot(x,np.sin(x + i*.5)*(7-i)*flip)
        
sns.set() #aktiviert seaborn style

# Farbräume
sns.palplot(sns.color_palette(palette='gray',n_colors=5,desat=0.5)) # zeigt aktuelle bzw. angegebene Farbpalette
plt.show()
sns.set_palette(palette='gray',n_colors=4,desat=None,color_codes=False) # setzt Farbpalette, Anzahl bestimmt Kontrast
sinplot() #Funktion für Sinus-Plot (als Beispiel)

# verschiedene Plotmöglichkeiten
sns.distplot(df['total_bill'],hist=True,kde=False) # Übersicht als Histogramm (kde:= Trendlinie)
plt.show()
sns.jointplot(x='total_bill', y='tip',data=df, kind='reg') # SNS erkennt DateFrame
plt.show()
sns.pairplot(df,hue='sex',diag_kind='kde', kind='reg', palette='husl')
plt.show()
sns.stripplot(x='sex',y='total_bill',data=df,jitter=False) #jitter True zur besseren Übersicht
plt.show()
sns.swarmplot(x='sex',y='total_bill',data=df)
plt.show()
sns.boxplot(x='sex',y='total_bill',data=df) #orient='v' oder 'h' für vertikal oder horizontal
plt.show()
sns.violinplot(x='day',y='total_bill',hue='sex',data=df)
plt.show()
sns.barplot(x='day',y='total_bill',hue='sex',data=df)
plt.show()
sns.countplot(x='day',data=df,hue='sex', palette='gray')
plt.show()

# mehrfache statistische plots
df = sns.load_dataset('exercise')
sns.catplot(x='time',y='pulse',hue='kind',kind='box', col='diet',data=df)
plt.show()

df = sns.load_dataset('tips')
sns.regplot(x='total_bill',y='tip',data=df)
sns.lmplot(x='total_bill',y='tip',data=df, kind='reg')
plt.show()

df = sns.load_dataset('anscombe')
sns.lmplot(x='x',y='y',data=df.query('dataset == "I"'),fit_reg=True)
plt.show()
sns.lmplot(x='x',y='y',data=df.query('dataset == "II"'),order=2)
plt.show()

df = sns.load_dataset('tips')
g = sns.FacetGrid(df, col='time')
g = g.map(plt.hist, 'tip') #plt.scatter, etc
#g = g.add_legend()
plt.show()

df = sns.load_dataset('iris')
g = sns.PairGrid(df)
g = g.map(plt.scatter) #plt.scatter, etc
plt.show()

g = sns.PairGrid(df,hue='species')
g = g.map_diag(plt.hist, edgecolor='w') #plt.scatter, etc
g = g.map_offdiag(plt.scatter)
g = g.add_legend()
plt.show()

# subplots
sns.set(style="white", palette="muted", color_codes=True)
rs = np.random.RandomState(10)
d = rs.normal(size=100)
f, ax = plt.subplots(2,2, figsize=(7,7), sharex=True)

sns.distplot(d, kde=False, color="k", ax=ax[0, 0])
sns.distplot(d, hist=False, rug=True, color="k", ax=ax[0, 1])
sns.distplot(d, hist=False, color="k", kde_kws={"shade": True}, ax=ax[1, 0])
sns.distplot(d, color="k", ax=ax[1, 1])

plt.setp(ax, yticks=[])
plt.tight_layout()
plt.show()


