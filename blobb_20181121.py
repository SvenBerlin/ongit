# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 13:20:12 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class blobb:  
    def __init__(self,x,y,):
        self.xpos = x
        self.ypos = y
        self.xlast = np.array([x])
        self.ylast = y
        self.area = 1
        
    def add_to_area(self, x, y,):
        self.xpos = (self.xpos*self.area + x)/(self.area+1)
        self.ypos = (self.ypos*self.area + y)/(self.area+1)
        self.area = self.area + 1
        self.xlast = np.append(self.xlast,x)
        
    def merge_areas(self, m_area, f=False):
        self.xpos = (m_area.xpos*m_area.area + self.xpos*self.area)/(m_area.area + self.area)
        self.ypos = (m_area.ypos*m_area.area + self.ypos*self.area)/(m_area.area + self.area)
        self.area = (m_area.area + self.area)
        if f == True:
            self.xlast = np.append(self.xlast,m_area.xlast)

def get_frame(frame):
    frame = r'C:\Users\sbergmann\Desktop\python_test\dice.jpg'
    img = Image.open(frame)    
    img_arr = np.array(img)
    img_bin = adaptive_binary(img_arr)
#    img_bin = binary_img(img_arr)    
    img_morph = morph(img_morph, ftype='dilatation')
    img_morph = morph(img_bin, ftype='closing')
    xcords, ycords = blobb_detection(img_morph)
    
def blobb_detection(img):
    height, width = img.shape
#    width, height = img.size
#    img_arr = np.array(img)
#    img = np.array((img_arr[:,:,0]+img_arr[:,:,1]+img_arr[:,:,2])/3)
#    img_arr = np.array(img)
    tag = 'area_'
    counter = 1
    for y in range(0,height):  # gehe durch jede Zeile
        # gebe Liste von Objekten aus vorangegangener Zeile
        obj_last_row = [obj for obj in locals() if ('area_' in obj and y-eval(obj+'.ylast')==1)]
        x = 0 # setze x = 0 (erste Spalte in Zeile)
        rem_obj =[] # Liste mit zu löschenden Objekten
        act_row =[] # Liste mit Objekten aus aktueller Zeile
        
        while x < width: # gehe durch alle Pixel einer Reihe durch     
            if img[y,x] == 0: #wenn Pixelwert größer 0
                exec(tag+str(counter)+'=blobb(x,y)') # erstelle vorerst neue area
                act_row.append(tag+str(counter)) # füge Objekt zur Liste der aktuellen Zeile hinzu
#                x = x+1 # inkrementiere x
                while img[y,x]==1 and x < width:  # solange angrenzende Pixel auch >0, add to area
                    exec(tag+str(counter)+'.add_to_area(x,y)') # füge Pixel zum aktuellen Objekt hinzu
                    x = x +1 # inkrementiere x
                counter = counter +1 # inkrementiere Objekt-Zähler
            x = x+1 # inkrementiere x
        if len(obj_last_row)>0:
            for obj in obj_last_row: # gehe die Objekte aus vorangegangener Zeile einzeln durch
                last_meet_act = [] # Liste mit Objekten aus aktueller Zeile die zu einem bestimmten Obj aus vorangehender Zeile passen
                for objx in eval(obj+'.xlast'): # gehe jede Pixelposition jedes vorangegenagen Objektes durch
                    for row_obj in act_row: # gehe jedes Objekt aus der aktuellen Zeile durch
                        for rowx in eval(row_obj+'.xlast'): # gehe jeden Pixel jedes Objektes der aktuellen Zeile durch
                            if abs(objx-rowx)<=1 and row_obj not in last_meet_act: # prüfeob Pixel sich berühren und ob Ojekt bereits behandelt
                                last_meet_act.append(row_obj) # füge row-Objekt zur Liste hinzu            
                if len(last_meet_act) > 0: #wenn mindestens ein row_objekt Verbindung zu vorangegangnes Objekt besitzt 
                    exec(last_meet_act[0]+'.merge_areas('+obj+')') # füge zusammen
                    rem_obj.append(obj) # setze vorangegangenes Objekt auf Löschliste
                    if len(last_meet_act) > 1: # wenn mehrere row-Objekte mit Objekt in Verbindung treten
                        for mobj in last_meet_act[1:]: # füge weitere Objekte dem ersten Objekt hinzu
                            exec(last_meet_act[0]+'.merge_areas('+mobj+',True)')
                            rem_obj.append(mobj) # setze row Objekt auf die Löschliste
    
        for obj in rem_obj: # gehe alle Objekte in der Löschliste durch 
            try:
                exec('del '+obj) #...und lösche sie
            except:
                pass
            
    # entnehme allen verbleibenen Objekten die x und y Position
    xcords = [eval(obj+'.xpos') for obj in locals() if 'area_' in obj]
    ycords = [eval(obj+'.ypos') for obj in locals() if 'area_' in obj]
    # plot der Grafik mit den ermittelten Schwerpunkten/Erkennungsmerkmale
    plt.imshow(img)
    plt.scatter(x=xcords,y=ycords, c='red', marker='x', s=10)
    
    return xcords, ycords


def adaptive_binary(img, c=20, size = 5):
    img_gray = np.array((img[:,:,0]+img[:,:,1]+img[:,:,2])/3)
    size = int(np.floor(size/2))
#    img = img_gray
    height, width = img_gray.shape
    img_copy = np.copy(img_gray)
    for y in range(0,height):
        for x in range(0,width):
            if y-size<0:
                ymin = 0
            else:
                ymin = y-size
            if y+size>height:
                ymax = height
            else:
                ymax = y+size
            if x-size<0:
                xmin = 0
            else:
                xmin = x-size
            if x+size>width:
                xmax = height
            else:
                xmax = x+size
            sub = img_gray[ymin:ymax,xmin:xmax]
            th = sub.mean()-c
            if th<0:
                th = 0
            if img_gray[y,x] <= th:
                img_copy[y,x] = 0
#                img[y,x] = 0
            else:
                img_copy[y,x] = 1
#                img[y,x] = 25
#    frame = Image.fromarray(img_copy).convert('L')
#    matplotlib.image.imsave('new.png',frame)         
    
    return img_copy
                
def morph(img,ftype,size=3):
    
    if ftype == 'dilatation':
        val = [0]
    elif ftype == 'erosion':
        val = [1]
    elif ftype == 'opening':
        val = [1,0]
    elif ftype == 'closing':
        val = [0,1]
    else:
        print('Failure')
    
    size = int(np.floor(size/2))
#    img = img_gray
    height, width = img.shape
    img_copy = np.copy(img)
    for v in val:
        img_copy = np.copy(img)
        for y in range(0,height):
            for x in range(0,width):
                if y-size<0:
                    ymin = 0
                else:
                    ymin = y-size
                if y+size>height:
                    ymax = height
                else:
                    ymax = y+size
                if x-size<0:
                    xmin = 0
                else:
                    xmin = x-size
                if x+size>width:
                    xmax = height
                else:
                    xmax = x+size
                sub = img[ymin:ymax+1,xmin:xmax+1]
                if v in sub:
                    img_copy[y,x] = v
        img = np.copy(img_copy)     
                
    return img_copy      
        
#    s = np.arange(-int(np.floor(size/2)),int(np.floor(size/2))+1)
#    s = np.array([s,s,s])
#    
#    
#    plt.imsave('filename.png',img_copy2, cmap=cm.gray)

def binary_img(img):
    height, width = img.shape
    img_gray = np.array((img[:,:,0]+img[:,:,1]+img[:,:,2])/3)
    img_bin = (img_gray<1).astype(int)
    return img_bin
    