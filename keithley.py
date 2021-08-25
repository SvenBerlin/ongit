# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 14:24:47 2021

@author: sbergmann
""" 
'''
ASCII data format (p. 172/section 13-4 in manual):
    +1.040564E-06A, +2.236299E+02,+1.380000E+02
    Reading    Unit  Timestamp      Status
    

'''

#https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
import serial
import serial.tools.list_ports
import pandas as pd
import time
import datetime
from enum import Enum


class Presets(Enum):
    # CURR = ['CONF:CURR\n','SYST:KEY 8\n','SYST:KEY 16\n','SYST:KEY 8\n','SYST:KEY 7\n','SYST:KEY 2\n']
    CURR = [':CONF:CURR\n', #sets up device to measure current
            ':SYST:ZCH 1\n',
            ':SYST:ZCOR 1\n',
            ':SYST:ZCH 0\n',
            ':CALC2:NULL:ACQ\n',
            ':CALC2:NULL:STAT 1\n',
            ':SENS:AVER 1\n']

def showports():
    ''' for debugging
    '''
    ports = []
    for p in serial.tools.list_ports.comports():
        print(p.device+', ',end='')
        print(p.serial_number)
        print(p.description)
        ports.append(p.device)
    return(ports)

class keithley6485:
    
    def __init__(self,baudrate=9600,port='COM8',parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,):
        self.baudrate = baudrate
        self.port = port
        self.parity = parity
        self.stopbits = stopbits
        self.xonxoff = False
        self.dt = 0.1
        self.timeout = 2
        self.connected = False
        self.status = 'closed'
        self.device = 'unknown'
        self.sn = 'unknown'
        self.lastline = ''
        
        # self.connect()

    def connect(self):
        self.ser = serial.Serial()
        self.ser.baudrate = self.baudrate
        self.ser.port = self.port
        self.ser.parity = self.parity
        self.ser.stopbits = self.stopbits
        self.ser.xonxoff = self.xonxoff
        self.ser.timeout = self.timeout

        try:
            self.ser.open()
            if self.ser.isOpen(): 
                # self.ser.write('*IDN?\n'.encode('utf-8'))
                self.send('*IDN?\n') # identification query
                # self.read()
                self.device = self.read()
                self.sn = self.device.split(',')[2]
                # self.device = self.send('*IDN?\n')
                self.connected = True
                self.status = 'connected'
                self.reset()
                print(f'{self.ser.name} open: {self.device}')
                self.clearErr()  
                
        except serial.SerialException as e:
            if e.errno ==13:
                print(f"could not open port '{self.ser.port}'")
            pass
    
    def clearErr(self):
        self.send('*CLS\n') #clear messages from error queue
        self.readErr()
        print('error queue cleared')
        
    def send(self,code):
        self.ser.write(code.encode('utf-8'))
        # return self.read()
        
    def read(self):
         self.lastline = self.ser.readline().decode("utf-8")
         return self.lastline
    
    def resetTimer(self):
        self.send(':SYST:TIME:RES\n')
        self.time = datetime.datetime.now()
        
    def readErr(self):
        self.send(':SYST:ERR?\n:')
        self.error = self.read()
        self.send('*CLS\n')
        return self.error
        
    def measure(self, vaa='test_sample', register=1, name='test_measurement'):
        '''messung aus zeit, typ, VAA,volt, fehlereintrag, Register
        
        Parameter
        ---------
        VAA: string
            beschreibt die Probe
        Register: integer
            beschreibt den Messschritt (z.B. laufende Nummer)
        name: string
            beschreibt die Messart, zum Beipiel 'Meas', 'Ref'
        
        Ausgabe
        -------
        string
        '''
        self.send(':READ?\n')
        time.sleep(self.dt)
        curr = self.read()
        curr = curr.split(',')
        
        typ = 'keithley6485__Strommessung'
        actVal = float(curr[0][:-1])
        unit = curr[0][-1]
        t = self.time + datetime.timedelta(seconds=float(curr[1]))
        
        cols=['Type','name','VAAxxx','DateTime','actVal','Unit','check','Register','sn']
        dat = [typ, name, vaa, t, actVal, unit, self.readErr(), register, self.sn]
        df=pd.DataFrame(data=dat).T
        df.columns=cols
        return df

    
    def reset(self):
       self.send(':SYST:PRES\n')
       self.resetTimer()
     
    def setUp(self, preset):
        for setting in Presets[preset].value:
            self.send(setting)
            time.sleep(0.2)
    
    def close(self):
        if self.connected:
            self.send(':SYST:LOC\n')
            self.ser.close()
            self.connected = False
            print(f'{self.port} is now closed.')
        else:
            print(f'{self.port} is already closed.')
            
    
            
if __name__ == '__main__':
    
    k1 = keithley6485()
    k1.connect()
    k1.setUp('CURR')

    typ = 'keithley6485__Strommessung'
    name = 'Aquarius_Photometer_Mess'
    vaa = 'Testprobe'
   
    dt = 1
    
    df = pd.DataFrame()
    try: 
        for register in range(10):
            try:
                h=k1.measure(vaa,register,name)
                df = pd.concat([df,h],ignore_index=True)
                print(df[['VAAxxx','actVal','Unit', 'Register','check']].tail(1))

            except ValueError:
                pass
            time.sleep(dt)
    finally:
        k1.close()
        
# dfh = df[['VAAxxx','actVal','Unit', 'Register','check']]        
# format_row = "{:>10}" * (len(dfh.columns) +1 )
# print(format_row.format("", *dfh.columns))
# for idx, row in dfh.iterrows():
#     print(format_row.format(" ",*row.tolist()))
 #tbd

# sync: datetime mit Gerätetimer zeit = datetime.datetime.strptime(tstamp, '%d.%m.%Y %H:%M:%S')

# check = error code
# register = index (zb. Messserie)
# sn vom Keithley
# Type = 'keithley6485__Strommessung'
# name = Label vom Bediener (Mess/Ref z.B.)
# VAAxxx = Probe
# 

   
    
# k1.send('SYST:KEY 16\n')
# k1.send('SYST:KEY 8\n')
# k1.send('SYST:KEY 7\n')
# k1.send('SYST:KEY 2\n')

# k1.send('SYST:PRES\n')
# k1.send('SYST:ZCH 1\n')
# k1.send('SYST:ZCOR 1\n')
# k1.send('SYST:ZCH 0\n')
# k1.send('CALC2:NULL:ACQ\n')
# k1.send('CALC2:NULL:STAT 1\n')
# k1.send('SENS:MED 1\n')

# k1.send('SYST:ZCOR:ACQ\n')
# k1.send('CONF:CURR\n')
# k1.send('CONF:CURR\n')
