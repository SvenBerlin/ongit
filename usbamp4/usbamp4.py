# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 09:51:29 2022

@author: sbergmann
"""
import minimalmodbus
import serial
import serial.tools.list_ports
import time
import pandas as pd
from datetime import datetime


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


class USBAMP4:
    
    def __init__(self,baudrate=115200,port='COM17',slave=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,):
        self.baudrate = baudrate
        self.port = port
        self.slave = slave
        self.parity = parity
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = False
        self.timeout = 1
        self.connected = False
        self.status = None
        self.device = 'unknown'
        self.sn = 'unknown'
        self.range = None
        self.lastline = ''
        self.ranges = {0:'1nA',
                       1:'30nA',
                       2:'1uA',
                       3:'30uA',}

        
        self.connect()

    def connect(self):
        self.instrument = minimalmodbus.Instrument(self.port, self.slave)
        # self.ser = serial.Serial()
        self.instrument.serial.baudrate = self.baudrate
        self.instrument.serial.port = self.port
        self.instrument.serial.parity = self.parity
        self.instrument.serial.stopbits = self.stopbits
        self.instrument.serial.bytesize = self.bytesize
        self.instrument.serial.timeout = self.timeout
        self.instrument.address = self.slave
        self.instrument.mode = minimalmodbus.MODE_RTU 
        self.init_commands()
        for i in range(10):
          try:
              self.device = f'{self.read("vendor")} {self.read("typ")}'
              self.sn = str(self.read('sn'))
              self.range = self.read('get_range')
              self.connected = True 
              break
          except: pass
        if not self.connected: 
            print("connecting failed")
        
    def init_commands(self)  :   
        self.com = {"vendor":(self.instrument.read_string,[],{'registeraddress':110,'functioncode':3}),
            "typ": (self.instrument.read_string,[],{'registeraddress':118, 'functioncode':3}),
            "sn":(self.instrument.read_long,[],{'registeraddress':104, 'functioncode':3,}),
            "temperature":(self.instrument.read_string,[],{'registeraddress':126, 'functioncode':3}),
            "cycle":(self.instrument.read_register,[],{'registeraddress':2000, 'functioncode':3,}),
            "status": (self.instrument.read_register,[],{'registeraddress':2001, 'functioncode':3,}),
            "tstamp": (self.instrument.read_long,[],{'registeraddress':2002, 'functioncode':3,}),
            "caldate": (self.instrument.read_long,[],{'registeraddress':1030, 'functioncode':3,}),
            "get_range" : (self.instrument.read_register,[],{'registeraddress':137, 'functioncode':3,}),
            "set_range" : (self.instrument.write_register,[],{'registeraddress':137, 'functioncode':6,}),
            0: (self.instrument.read_float,[],{'registeraddress':2004, 'functioncode':3,'byteorder':0}),
            1 : (self.instrument.read_float,[],{'registeraddress':2006, 'functioncode':3,'byteorder':0}),
            2: (self.instrument.read_float,[],{'registeraddress':2008, 'functioncode':3,'byteorder':0}),
            3: (self.instrument.read_float,[],{'registeraddress':2010, 'functioncode':3,'byteorder':0}),
            }
        

    def read(self,choice):
        # if choice == 'measure':
        #     func, args,kwargs= self.com['get_range']
        #     choice = func(*args,**kwargs)
        func, args,kwargs= self.com[choice]
        self.lastline = func(*args,**kwargs)
        print(f'{choice}: {self.lastline}')
        return self.lastline
        
    def write(self,choice,value):
        func, args,kwargs= self.com[choice]
        kwargs['value'] = value
        self.lastline = func(*args,**kwargs)
        print(f'{choice}: {self.lastline}')
        return self.lastline

    def measure(self,auto_range=True,typ='usbamp4__Strommessung', vaa='test_sample',SetNo=0, register=1, name='test_measurement'):
        for i in range(4):
            func, args,kwargs= self.com['status']
            self.status = func(*args,**kwargs)
            if self.status == 0:
                func, args,kwargs= self.com[self.range]
                actVal = func(*args,**kwargs)
                self.lastline = actVal
                t = datetime.now().isoformat()
                cols=['Type','name','VAAxxx','SetNo','DateTime','actVal','Unit','check','Register','sn']
                dat = [typ, name, vaa,SetNo, t, actVal, self.ranges[i], self.status, register, self.sn]
                df=pd.DataFrame(data=dat).T
                df.columns=cols
                # print(self.lastline)
                # return self.lastline
                return df
            elif i < 4:
                self.write('set_range',i)    
                print(f'measuring range is set to {i}({self.ranges[i]})')
            else:
                print("measurement out of devices range")
if __name__=='__main__':
    import matplotlib.pyplot as plt
    
    
    dt = 0.1
    k1 = USBAMP4(port="COM17")
    df = pd.DataFrame()
    
    mydpi = 96
    fig, ax = plt.subplots(figsize=(800/mydpi,600/mydpi),dpi=mydpi)
    ax.set_xlabel("Messung (1)")
    ax.set_ylabel("Photostrom (A)")
    ax.grid()
    plt.tight_layout()

    cnt = 0
    while True:
        df = pd.concat([df,k1.measure()],ignore_index=True)
        print(df[['SetNo','VAAxxx','actVal','Unit', 'Register','check']].tail(1).values)
        try:
            if cnt == 0:
                ax.set_title(f'{df["Type"][0]}_{df["name"][0]}_{df["VAAxxx"][0]}')
            ax.scatter(cnt,df.actVal.iloc[-1],color='blue')
            plt.pause(dt)
            cnt += 1
        except: pass
        time.sleep(dt)

if False:
    import minimalmodbus
    import serial
    
    instrument = minimalmodbus.Instrument('COM17', 1)  # port name, slave address (in decimal)
    instrument.serial.port = 'COM17'                     # this is the serial port name
    instrument.serial.baudrate = 115200         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_EVEN
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 1        # seconds
    instrument.address = 1                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    #nstrument.clear_buffers_before_each_transaction = True
    vendor = instrument.read_string(registeraddress=110, functioncode=3)  # Registernumber, number of decimals
    typ = instrument.read_string(registeraddress=118, functioncode=3)  # Registernumber, number of decimals
    sn = instrument.read_long(registeraddress=104, functioncode=3,)
    sensor = instrument.read_string(registeraddress=126, functioncode=3)  # Registernumber, number of decimals
    temperature = instrument.read_float(registeraddress=2014, functioncode=3,byteorder=0)
    cycle = instrument.read_register(registeraddress=2000, functioncode=3,)
    status = instrument.read_register(registeraddress=2001, functioncode=3,)
    tstamp = instrument.read_long(registeraddress=2002, functioncode=3,)
    caldate = instrument.read_long(registeraddress=1030, functioncode=3,)
    rang = instrument.read_register(registeraddress=137, functioncode=3,)
    instrument.write_register(registeraddress=137, value=2, functioncode=6,)
    data = instrument.read_float(registeraddress=2004, functioncode=3,byteorder=0)
    data = instrument.read_float(registeraddress=2006, functioncode=3,byteorder=0)
    data = instrument.read_float(registeraddress=2008, functioncode=3,byteorder=0)
    data = instrument.read_float(registeraddress=2010, functioncode=3,byteorder=0)

        # {"vendor":instrument.read_string(registeraddress=110, functioncode=3),
        #  "typ": instrument.read_string(registeraddress=118, functioncode=3),
        #  "sn":instrument.read_long(registeraddress=104, functioncode=3,),
        #  "temperature":instrument.read_string(registeraddress=126, functioncode=3),
        #  "cycle":instrument.read_register(registeraddress=2000, functioncode=3,),
        #  "status": instrument.read_register(registeraddress=2001, functioncode=3,),
        #  "tstamp": instrument.read_long(registeraddress=2002, functioncode=3,),
        #  "caldate": instrument.read_long(registeraddress=1030, functioncode=3,),
        #  "get_range" : instrument.read_register(registeraddress=137, functioncode=3,),
        #  "data_0": instrument.read_float(registeraddress=2004, functioncode=3,byteorder=0),
        #  "data_1" : instrument.read_float(registeraddress=2006, functioncode=3,byteorder=0),
        #  "data_2": instrument.read_float(registeraddress=2008, functioncode=3,byteorder=0),
        #  "data_3": instrument.read_float(registeraddress=2010, functioncode=3,byteorder=0),
        #  }