# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:10:12 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import win32api, win32con, win32gui
import time
import numpy as np

class mouse:
    def __init__(self):
        getposition()

    def move(x,y):
        win32api.SetCursorPos((x,y))
    
    def leftclick(x,y):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
    def rightclick(x,y):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def getposition():
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
#        print('\r%s,%s' % (x,y), end = '\r')
        print('\r{},{}\r'.format(x,y),end='\r')
### position
# while True:
#     mouse.getposition()
t = 3
for x in range(t):
    print('{}s remaining'.format(t-x))
    time.sleep(1)
### Linksklick    
start = win32gui.GetCursorInfo()[2]
(x,y) = start
while True:
    if start == win32gui.GetCursorInfo()[2]:
        mouse.leftclick(x,y)
    else:
        break
    time.sleep(0.1)



### viereck
# (x,y) = win32gui.GetCursorInfo()[2]
# t = [(200,0),(200,-200),(0,-200),(100,-300),(200,-200),(0,0),(0,-200),(200,0),] #haus
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
# for i,j in t:
#     win32api.SetCursorPos((x+i,y+j))
#     time.sleep(0.1)

### kreis
# radius = 100
# for deg in range(360):
#     t.append((int(np.cos(deg*np.pi/180)*radius),int(np.sin(deg*np.pi/180)*radius)))

# old = win32gui.GetCursorInfo()[2]
# (x,y) = old
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
# for k,l in t:
#     if old == win32gui.GetCursorInfo()[2]:
#         win32api.SetCursorPos((x-radius+k,y+l))
#         time.sleep(0.0000001)
#         old = win32gui.GetCursorInfo()[2]
#         # print(old)
#     else:
#         break
win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
    
# win32api.SetCursorPos((x+200,y))
# time.sleep(0.05)
# win32api.SetCursorPos((x+200,y-200))
# time.sleep(0.05)
# win32api.SetCursorPos((x,y-200))
# time.sleep(0.05)
# win32api.SetCursorPos((x+100,y-300))
# time.sleep(0.05)
# win32api.SetCursorPos((x+200,y-200))
# time.sleep(0.05)
# win32api.SetCursorPos((x,y))
# time.sleep(0.05)
# win32api.SetCursorPos((x,y-200))
# time.sleep(0.05)
# win32api.SetCursorPos((x+200,y))
# time.sleep(0.05)
# win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x+200,y,0,0)
    
    
# mouse.move(922,422)
# for i in range(10):
#     mouse.leftclick(922,422)
#     time.sleep(0.1)