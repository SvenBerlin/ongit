# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:48:15 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import numpy as np

weekday=['Mo','Di','Mi','Do','Fr','Sa','So']
month=[0,3,3,6,1,4,6,2,5,0,3,5]
i_d=6
i_m=8
i_y=2087

print(weekday[np.mod(i_y-1900+int(np.floor((i_y-1900)/4))+month[i_m-1]+(i_d-1),7)])
