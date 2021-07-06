# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:48:38 2021

@author: sbergmann
"""

import glob as glob
import os as os
import cv2


def scale_image(input_path,output_path,scale_factor=0.5):
    original_image= cv2.imread(input_path)
    w, h = original_image.shape[:2]
    scaled_image = cv2.resize(original_image, dsize=(int(h*scale_factor),
                                                     int(w*scale_factor)),
                              interpolation=cv2.INTER_CUBIC)
    fname = os.path.join(output_path, f'resized_{os.path.basename(input_path)}')
    cv2.imwrite(fname,output_path)
    
    
path = r'C:\Users\sbergmann\Desktop\Fotos'
sf = 0.5 #percentage

output = os.path.join(path,'out')
try:
    os.mkdir(output)
except FileExistsError:
    pass


files = glob.glob(path+'\\*.*')


for f in files:

    scale_image(f,output)

    img = cv2.imread(f)
    res = cv2.resize(img, dsize=(int(img.shape[1]*sf),int(img.shape[0]*sf)), interpolation=cv2.INTER_CUBIC)
    fname = os.path.join(output, f'resized_{os.path.basename(f)}')
    cv2.imwrite(fname,res)
