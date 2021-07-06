# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:55:20 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import time
class countdown:
    
    def __init__(self,start,acc=1000, launch=True):
        self.start = start
        self.acc = acc
        self.pre = len(str(self.acc))-1
        self.total = self.start*self.acc
        if launch == True:
            self.launch()
    
    def launch(self):
        for i in range(self.total+1):
            print('\r' + str(round(i/self.acc,self.pre)),end='\r')
            time.sleep(1/self.acc)


if __name__ == '__main__':
    # newCountdown = countdown(10)
    # newCountdown.launch()
    countdown(3)