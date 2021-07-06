# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 08:03:34 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import serial

ser = serial.Serial()
ser.timeout = 3
ser.baudrate = 19200
ser.port = 'COM1'


### Test

ser.open()
ser.is_open
ser.close()
ser.is_open

command = b'x57'
ser.write(command)

command = b'\x58'

in_bin = ser.read()

re = ''
while True:
    in_bin = ser.read()
    in_hex = hex(int.from_bytes(in_bin,byteorder='little')) 
    re = re + in_hex

print(in_hex)