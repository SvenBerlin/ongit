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
            'INIT\n',
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
        self.offs = '0.000'
        
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
        self.error = self.read().strip()
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
        rawactVal = float(curr[0][:-1])
        actVal= rawactVal - self.offs
        unit = curr[0][-1]
        t = self.time + datetime.timedelta(seconds=float(curr[1]))
        
        cols=['Type','name','VAAxxx','DateTime','actVal','Unit','rawactVal','offsetactVal','check','Register','sn']
        dat = [typ, name, vaa, t, actVal, unit,rawactVal,float(self.offs), self.readErr(), register, self.sn]
        df=pd.DataFrame(data=dat).T
        df.columns=cols
        return df

    def getOffset(self):
        self.send('INIT\n')
        time.sleep(0.2)
        self.send(':CALC2:NULL:ACQ\n')
        time.sleep(0.2)
        self.send('CALC2:NULL:OFFS?\n')
        self.offs = float(self.read())

    def reset(self):
       self.send(':SYST:PRES\n')
       self.resetTimer()
     
    def setUp(self, preset,):
        for setting in Presets[preset].value:
            self.send(setting)
            time.sleep(0.2)
        self.send('CALC2:NULL:OFFS?\n')
        self.offs = float(self.read())
    def close(self):
        if self.connected:
            self.send(':SYST:LOC\n')
            self.ser.close()
            self.connected = False
            print(f'{self.port} is now closed.')
        else:
            print(f'{self.port} is already closed.')
            
    
            
if __name__ == '__main__':

    import cv2
    import numpy as np
    
    def trigger():
        width=1920
        height=1080
        fsize = 200
        
        lower_val = np.array([146,44,176]) 
        upper_val = np.array([177,255,255]) 
        # lower_val = np.array([0,42,176]) 
        # upper_val = np.array([10,255,255]) 
        
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) # set the Horizontal resolution
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # Set the Vertical resolution

        
        while(cap.isOpened()):
            ret, frame = cap.read()
            frame = frame[int(height/2-fsize):int(height/2+fsize),int(width/2-fsize):int(width/2+fsize)]
            if ret==True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_val, upper_val)
                hasColor = np.sum(mask)
                if hasColor > mask.size*255/4:
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()






    
    k1 = keithley6485(port='COM11')
    k1.connect()
    k1.setUp('CURR')
    
    ftime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M')
    typ = 'keithley6485__Strommessung'
    basename = 'AQ_Photometer'
    vaa = 'Testprobe'
    register = 0
    dt = 0.1
    cnt = 1

    
    df = pd.DataFrame()
    input(f"Offset (Keithley): {k1.offs}. Enter um Messungen zu starten...")
    try: 
        while True:
            print('warte auf Trigger durch LRP...')
            trigger()
            
            if cnt%2 != 0:
                name = f'{basename}_NULL'
                print(f'Offset (Keithley): {k1.offs}\n{name}')
                k1.getOffset()
            else:
                name = f'{basename}_MESS_{int(cnt/2)}'
                print(name)
            for register in range(10):
                try:
                    # print(register)
                    h=k1.measure(vaa,register,name)
                    df = pd.concat([df,h],ignore_index=True)
                    print(df[['VAAxxx','actVal','Unit', 'Register','check']].tail(1))
                except ValueError:
                    pass
                time.sleep(dt)#
            cnt += 1
    except: pass
    finally:
        df.to_csv(f'{basename}_{ftime}.csv',index=False)
        k1.close()
        
        
        
        
### manuell
    # k1 = keithley6485(port='COM11')
    # k1.connect()
    # k1.setUp('CURR')
    
    # ftime = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M')
    # typ = 'keithley6485__Strommessung'
    # name = 'Aquarius_Photometer_Mess'
    # vaa = 'Testprobe'
    # _vaa =''
    # register = 0
    # dt = 1
    
    # wdh = 20
    
    # df = pd.DataFrame()
    # input(f"Nullung erfolgt (Offset: {k1.offs}). Enter um Messungen zu starten...")
    # try: 
    #     while True:
    #         vaa = input('VAAxxx eingeben ("q" zum beenden, "offset" um neuen Offset zu speichern): ') or "Testprobe"
    #         if vaa == _vaa:
    #             register +=1
    #         else:
    #             register = 0
    #         _vaa = vaa
    #         if vaa =="q":
    #             break
    #         elif vaa == "offset":
    #             k1.setUp('CURR')
    #         else:
    #             for i in range(10):
    #                 try:
    #                     h=k1.measure(vaa,register,name)
    #                     df = pd.concat([df,h],ignore_index=True)
    #                     print(df[['VAAxxx','actVal','Unit', 'Register','check']].tail(1))
    #                 except ValueError:
    #                     pass
    #                 time.sleep(dt)
    # finally:
    #     df.to_csv(f'{name}_{ftime}.csv',index=False)
    #     k1.close()      
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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

# rawactVal
# offsetactVal
# actVal

    
# k1.send('SYST:KEY 16\n')
# k1.send('SYST:KEY 8\n')
# k1.send('SYST:KEY 2\n')
# CURR = [':CONF:CURR\n', #sets up device to measure current
#             ':SYST:ZCH 1\n',
#             ':SYST:ZCOR 1\n',
#             ':SYST:ZCH 0\n',
#             ':CALC2:NULL:ACQ\n',
#             ':CALC2:NULL:STAT 1\n',
#             ':SENS:AVER 1\n']


# k1.send('SYST:KEY 7\n')
# k1.send(':CONF:CURR\n')
# k1.send('SYST:ZCH 1\n')
# k1.send('SYST:ZCOR 1\n')
# k1.send('SYST:ZCH 0\n')
# k1.send('CALC2:NULL:ACQ\n')
# k1.send('CALC2:NULL:STAT 0\n')
# k1.send(':SENS:AVER 1\n')


# k1.send(':READ?\n')
# k1.send('*CLS\n')
# offs = k1.read()
# offs = offs.split(',')
# offs = offs[0][:-1]
# if offs[0] == '+': offs = offs[1:]
# k1.send(f'CALC2:NULL:OFFS {offs}\n')
# k1.send('CALC2:NULL:OFFS?\n')
# k1.send('CALC2:NULL:STAT?\n')
# k1.send('CALC2:FEED SENS\n')
# k1.send('INIT\n')
# k1.send('CALC2:DATA?\n')


# k1.send('SYST:ZCOR:ACQ\n')
# k1.send('CONF:CURR\n')
# k1.send('CONF:CURR\n')
