# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:26:24 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import time



# class webcam():
#     def __init__(self, width=1920, height=1080, fps=1, fname='webcam', gray=False,save=False):
#         self.width = width
#         self.height = height
#         self.fps = fps 
#         self.fname = fname
#         self.gray = gray
#         self.save = save
        
#         self.set_camera()
        
#     def set_camera(self):
#         self.cap = cv2.VideoCapture(0)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) # set the Horizontal resolution
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) # Set the Vertical resolution
#         self.cap.set(cv2.CAP_PROP_FPS,self.fps)   
#         # self.cap.set(cv2.CAP_PROP_EXPOSURE, 40)
#         self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         self.out = cv2.VideoWriter(self.fname+'.avi',self.fourcc, self.fps, (self.width,self.height))
        
#     def open_camera(self):
#     #     b = threading.Thread(name='background', target=self.background)
#     #     b.start()
        
#     # def background(self):
#         while(self.cap.isOpened()):
#             ret, frame = self.cap.read()
#             if ret==True:
#         #        frame = cv2.flip(frame,0)
#                 if self.gray is True:
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                     frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
#                 if self.save is True:
#                     # write the flipped frame
#                     self.out.write(frame)
 
#                 try:
#                     print('Bildaufnehmen')
#                     self.get_segment(frame)
#                 except:
#                     pass
                
#                 cv2.imshow('frame',frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     self.close_camera()
#                     break
#             else:
#                 break
#             time.sleep(1)
    
#     def close_camera(self):
#         self.cap.release()
#         self.out.release()
#         cv2.destroyAllWindows()

#     def get_segment(self,image):
#         image = imutils.resize(image, height=500)
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         edged = cv2.Canny(blurred, 50, 200, 255)
 
#         # find contours in the edge map, then sort them by their
#         # size in descending order
#         cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
#          	cv2.CHAIN_APPROX_SIMPLE)
#         cnts = imutils.grab_contours(cnts)
#         cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
#         displayCnt = None
#         # loop over the contours
#         for c in cnts:
#          	# approximate the contour
#          	peri = cv2.arcLength(c, True)
#          	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
#          	# if the contour has four vertices, then we have found
#          	# the thermostat display
#          	if len(approx) == 4:
#         		displayCnt = approx
#         		break
        
#         # a=[[1,1.24],[1,.57],[.75,.57],[.75,1.24]]
#         a=[[1,1.45],[1,.72],[.88,.72],[.88,1.45]]
#         displayCnt = np.round(displayCnt.reshape(4, 2)*a)
           
#         # extract the thermostat display, apply a perspective transform
#         # to it
#         warped = four_point_transform(gray, displayCnt.reshape(4, 2))
#         output = four_point_transform(image, displayCnt.reshape(4, 2))
        
#         # threshold the warped image, then apply a series of morphological
#         # operations to cleanup the thresholded image
#         thresh = cv2.threshold(warped, 0, 255,
#          	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
#         thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
#         string = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.')
#         cv2.imshow(tresh)
#         print(string)
#         return thresh, string
    
    
# if __name__ =='__main__':
    
#     cam = webcam()
#     cam.open_camera()

def get_segment(image):
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
     

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
     	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None

    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    	# if the contour has four vertices, then we have found
    	# the thermostat display
    	if len(approx) == 4:
    		displayCnt = approx
    		break
    
    # a=[[1,1.24],[1,.57],[.75,.57],[.75,1.24]]
    # a=[[1,1.45],[1,.72],[.88,.72],[.88,1.45]]
    # displayCnt = np.round(displayCnt.reshape(4, 2)*a)
       
    # extract the thermostat display, apply a perspective transform
    # to it
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    output = four_point_transform(image, displayCnt.reshape(4, 2))
    
    warped = warped[round(warped.shape[0]*.22):round(warped.shape[0]*.56),round(warped.shape[1]*.03):round(warped.shape[1]*.78)]
    output = output[round(output.shape[0]*.22):round(output.shape[0]*.56),round(output.shape[1]*.03):round(output.shape[1]*.78),:]
    
    # threshold the warped image, then apply a series of morphological
    # operations to cleanup the thresholded image
    thresh = cv2.threshold(warped, 0, 255,
     	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    string = pytesseract.image_to_string(thresh, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.')
    cv2.imshow('test',thresh)
    print(string)
    return string

cap = cv2.VideoCapture(0)
for n in range(10):
    ret, frame =cap.read()
    try:
        get_segment(frame)
    except:
        print('no image')
        pass
    time.sleep(1)
cap.release()

# import matplotlib.pyplot as plt
# plt.imshow(output)
cv2.imshow('test',output)


