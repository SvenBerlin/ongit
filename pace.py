# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 08:32:11 2017

@author: sbergmann
"""
import math
import numpy as np
import sys

class sports:
    results = []    
    def swim(pace,time):        
        print('\nSWIMMING')
        while (pace != 0 and time != 0) or (pace == 0 and time == 0):
            distance = float(input('enter a distance in m: '))
            pace = float(input('enter a pace in sec/100m: '))
            time = float(input('enter the desired time in min: '))
        
            if pace != 0:
                results = [math.floor(((distance/100)*pace)/60),'m',round(((((distance/100)*pace)/60)%1)*60),'s']
            if time != 0:
                results = [math.floor((time*60)/(distance/100)),'sec/100m']
            sports.err(pace,time)
        return results
    
    def bike(pace,time):
        print('\nBIKING')
        while (pace != 0 and time != 0) or (pace == 0 and time == 0):
            distance = float(input('enter a distance in km: '))
            pace = float(input('enter a pace in km/h: '))
            time = float(input('enter the desired time in min: '))
            
            if pace != 0:
                results = [math.floor(distance/pace),'h',math.floor(((distance/pace)%1)*60),'m'
                           ,math.floor((((distance/pace)%1)*60)%1*60),'s']
            if time != 0:
                results = [round(distance/(time/60),2),'km/h']
            sports.err(pace,time)
        return results
    
    def run(pace,time):
        print('\nRUNNING')
        while (pace != 0 and time != 0) or (pace == 0 and time == 0):
            distance = float(input('enter a distance in km: '))
            pace = float(input('enter a pace in sec/km: '))
            time = float(input('enter the desired time in min: '))
            
            if pace != 0:
                results = [math.floor((((distance)*pace)/60)),'m',round(((((distance)*pace)/60)%1)*60),'s']
            if time != 0:
                results = [math.floor(time/distance),'m',math.floor(((time/distance)%1)*60),'s']
            sports.err(pace,time)        
        return results
    
    def err(pace, time):
        if pace != 0 and time != 0:
            print('you have to enter only one value either pace or time')
        if pace == 0 and time == 0:
            print('you have to enter something')
            
chose=1
print('this application will calculate pace or time for different sports\n')
while chose != 0:
    chose = int(input('swim [1], bike[2], run[3] or tri [4] - quit [0] '))
    if chose == 1:
        results = sports.swim(0,0)
    if chose == 2:
        results = sports.bike(0,0)
    if chose == 3:
        results = sports.run(0,0)
    if chose == 4:
        results = sports.swim(0,0)
        results.append('  ')
        results = results + sports.bike(0,0)
        results.append('  ')
        results = results + sports.run(0,0)
    if chose == 0:
        pass
    for i in range(0,np.size(results)):
        sys.stdout.write(str(results[i]))