# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 13:57:10 2019

@author: sbergmann
source: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
Copyright@Hach Lange GmbH 
"""

import numpy as np
from datetime import datetime
import cv2
import threading

# class webcam():
#     def __init__(self, width=1920, height=1080, fps=165, fname='webcam', gray=True,save=False):
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
        
#                 cv2.imshow('frame',frame)
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     self.close_camera()
#                     break
#             else:
#                 break
    
#     def close_camera(self):
#         self.cap.release()
#         self.out.release()
#         cv2.destroyAllWindows()


# if __name__ =='__main__':
    
#     cam = webcam()
#     cam.open_camera()

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

width=1920
height=1080
fps=60
fname = 'Nitro'
fname = fname+'_'+datetime.strftime(datetime.now(),'%y%m%d_%H%M%S')

cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FOCUS, 6)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) # set the Horizontal resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # Set the Vertical resolution
# cap.set(cv2.CAP_PROP_FPS,fps)
# cap.set(cv2.CAP_PROP_EXPOSURE, 2)

gray = True
save = False
# Define the codec and create VideoWriter object
img_counter=0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
#        frame = cv2.flip(frame,0)
        if gray is True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            # frame = increase_brightness(frame, value=100)
        if save is True:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(fname+'.avi',fourcc, fps, (width,height))
            # write the flipped frame
            out.write(frame)
        cv2.imshow('frame',frame)        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_name = "{}_img{}.png".format(fname,img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            
    else:
        break

# Release everything if job is finished
cap.release()
try:
    out.release()
except:
    pass
cv2.destroyAllWindows()




# from pypylon import pylon
# import cv2

# camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# # camera.ExposureTimeAbs = 2000000
# camera.Open()

# # demonstrate some feature access
# new_width = camera.Width.GetValue() - camera.Width.GetInc()
# if new_width >= camera.Width.GetMin():
#     camera.Width.SetValue(new_width)

# numberOfImagesToGrab = 100
# camera.StartGrabbingMax(numberOfImagesToGrab)

# while camera.IsGrabbing():
#     grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
#     cv2.imshow(grabResult)

#     # if grabResult.GrabSucceeded():
#     #     # Access the image data.
#     #     print("SizeX: ", grabResult.Width)
#     #     print("SizeY: ", grabResult.Height)
#     #     img = grabResult.Array
#     #     print("Gray value of first pixel: ", img[0, 0])

#     grabResult.Release()
# camera.Close()


# from pypylon import pylon
# import platform
# # https://github.com/basler/pypylon/blob/master/samples/save_image.py

# num_img_to_save = 1
# img = pylon.PylonImage()
# tlf = pylon.TlFactory.GetInstance()

# cam = pylon.InstantCamera(tlf.CreateFirstDevice())
# cam.Open()
# cam.ExposureTime.SetValue(40000)
# # cam.ExposureAuto.SetValue('Once')
# cam.StartGrabbing()
# for i in range(num_img_to_save):
#     with cam.RetrieveResult(2000) as result:

#         # Calling AttachGrabResultBuffer creates another reference to the
#         # grab result buffer. This prevents the buffer's reuse for grabbing.
#         img.AttachGrabResultBuffer(result)

#         if platform.system() == 'Windows':
#             # The JPEG format that is used here supports adjusting the image
#             # quality (100 -> best quality, 0 -> poor quality).
#             ipo = pylon.ImagePersistenceOptions()
#             quality = 90 - i * 10
#             ipo.SetQuality(quality)

#             filename = "saved_pypylon_img_%d.jpeg" % quality
#             img.Save(pylon.ImageFileFormat_Jpeg, filename, ipo)
#         else:
#             filename = "saved_pypylon_img_%d.png" % i
#             img.Save(pylon.ImageFileFormat_Png, filename)

#         # In order to make it possible to reuse the grab result for grabbing
#         # again, we have to release the image (effectively emptying the
#         # image object).
#         img.Release()

# cam.StopGrabbing()
# cam.Close()