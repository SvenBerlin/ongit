# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 08:51:25 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

# Plot simple sinus function
fig_handle = plt.figure()
x = np.linspace(0,2*np.pi)
y = np.sin(x)
plt.plot(x,y)

# Save figure handle to disk
pickle.dump(fig_handle,open('sinus.pickle','wb'))

fig_handle = pickle.load(open('sinus.pickle','rb'))
fig_handle.show()



#import plotly.plotly as py
#import plotly.graph_objs as go
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#
### Create random data with numpy
##import numpy as np
##
##N = 500
##random_x = np.linspace(0, 1, N)
##random_y = np.random.randn(N)
##
### Create a trace
##trace = go.Scatter(
##    x = random_x,
##    y = random_y
##)
##
##data = [trace]
##
##py.iplot(data)
#
#plot([go.Scatter(x=[1, 2, 3], y=[3, 1, 6])])
