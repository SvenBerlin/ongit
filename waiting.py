# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 08:35:42 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import time
class wait_state:
    WAITING = 'WAITING'
    PROCEED = 'PROCEED'
    ERROR = 'ERROR'

class wait:
    def __init__(self, text,sleep=.5):
        self.text = text
        self.dots = '.....'
        self.states = {'WAITING':wait_state.WAITING,
                       'PROCEED':wait_state.PROCEED,
                       'ERROR':wait_state.ERROR,}
        self.state = self.states['WAITING']
        self.count = 0
        self.sleep = sleep
        
    def printing(self):
        if self.state == wait_state.WAITING:
            print('\r%s' % (self.text+self.dots[:self.count%len(self.dots)]), end = ' '*int(len(self.dots)-self.count%len(self.dots)))
            self.count += 1
            time.sleep(self.sleep)
    
    def set_state(self,state):
        self.state = self.states[state]
        if self.state == wait_state.WAITING:
            self.printing()
        elif self.state == wait_state.ERROR:
            print('An Error occured')
            

if __name__ =='__main__':
    
    process = wait('Warte auf neue Daten')
    i = 0
    # while process.state == process.states['WAITING']:
    #     process.set_state('WAITING')
    #     if i >10:
    #         process.set_state(process.states['PROCEED'])
    #     i += 1
        
    while i<10:
        process.printing()
        i += 1