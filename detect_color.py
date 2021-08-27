# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:31:22 2021

@author: sbergmann
"""
import cv2
import numpy as np


width=1920
height=1080
fps=60

lower_val = np.array([0,42,176]) 
upper_val = np.array([10,255,255]) 

# cap = cv2.VideoCapture(0)
cap = cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap.set(cv2.CAP_PROP_FOCUS, 6)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) # set the Horizontal resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # Set the Vertical resolution
# cap.set(cv2.CAP_PROP_FPS,fps)
# cap.set(cv2.CAP_PROP_EXPOSURE, 2)

gray = False
save = False

img_counter=0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.bitwise_not(frame)
#        frame = cv2.flip(frame,0)
        # cv2.imshow('frame',frame)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, lower_val, upper_val)
        hasGreen = np.sum(mask)
        if hasGreen > mask.size*255/4:
            print('rot detektiert')
        
        res = cv2.bitwise_and(frame,frame,mask=mask)
        fin = np.hstack((frame,res))

        # cv2.imshow("Res", fin)
        cv2.imshow("Mask", mask)
    else:
        break


cap.release()
cv2.destroyAllWindows()