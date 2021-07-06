# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 09:40:11 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import time
import os

def is_locked(filepath):
    #QUELLE: https://www.calazan.com/how-to-check-if-a-file-is-locked-in-python/
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                locked = False
        except IOError:
           locked = True
        finally:
            if file_object:
                file_object.close()
    return locked  


file = r'C:\Users\sbergmann\Desktop\python_test\testfile.xlsx'

while is_locked(file):
    print("Datei nicht geschlossen")
    time.sleep(5)
