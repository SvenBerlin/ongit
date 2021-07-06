# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:33:03 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pickle
import matplotlib.pyplot as plt
import mplcursors

def show_figure(fig):

    # create a dummy figure and use its
    # manager to display "fig"  
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

#pickle.dump(fig, open('205nm_filter.fig.pickle', 'wb'))

# Einzelwellenlängen DR6000
# 205nm-bis Nov
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Nitro - Wassmansdorf_205nm_vom_16052019_104353_bis_16112019_173231.fig.pickle'
# 215nm-bis Nov
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\Nitro - Wassmansdorf_215nm_vom_16052019_104353_bis_16112019_173231.fig.pickle'
# 230nm-bis Nov
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\Nitro - Wassmansdorf_230nm_vom_16052019_104353_bis_16112019_173231.fig.pickle'
# 254nm-bis Nov
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\Nitro - Wassmansdorf_254nm_vom_16052019_104353_bis_16112019_173231.fig.pickle'

# DR6000 Conourplot: bis Nov
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\Nitro - Wassmansdorf_Contourplot_vom_16052019_104353_bis_16112019_173231.fig.pickle'

# Nitratax
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Nitratax - Wassmannsdorf_vom_20180118_bis_20191120.fig.pickle'

# Nitratax vs. DR6000
file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\dr6000VSnitratax - Wassmannsdorf_vom_20190617_bis_20190620.fig.pickle'

file = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\process\Nitro_98481\03_05_06_03_Optical_Engineering\a01_Theorie\nitro\example\plots\Update_Dez2019\Nitro - Schnitt über die Wellenlängen 205nm 215nm 230nm 254nm.fig.pickle'
figx = pickle.load(open(file, 'rb'))
mplcursors.cursor(hover=True)

show_figure(figx)
figx.show()

# data = figx.axes[0].lines[0].get_data()
