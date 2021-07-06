# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:46:23 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import numpy as np
from scipy.stats import kde
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

def rotate_around_point_highperf(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    
    return qx, qy




file = r'C:\Users\sbergmann\Desktop\python_test\Direct Simulation - IRRA_Kuev_Eingang_001.txt'
df = pd.read_csv(file, sep='\t',skiprows=410)



data = np.array(df)

#zi = k(np.vstack([xi.flatten(), yi.flatten()]))


theta = math.radians(180)    
qdf = pd.DataFrame(columns=df.columns)
arr = np.zeros(data.shape)
arr[:,0:2] = data[:,0:2]

for s in range(len(df)):
    xy = (df.iloc[s,0],df.iloc[s,1])
    qx,qy = rotate_around_point_highperf(xy, theta, origin=(0, 0))
    idx = df[(df['X'] ==qx) & (df['Y'] ==qy)].index[0]
    arr[s,2] = df.iloc[idx,2]
#    arr[s,0] =qx
#    arr[s,1] =qy


theta = math.radians(90)    
arr = np.zeros(data.shape)
arr[:,2] = data[:,2]
for s in range(len(data)):
    xy = data[s,[0,1]]
    qx,qy = rotate_around_point_highperf(xy, theta, origin=(200, 200))
    idx = 0
    for elm in data[:,:2]:
        print(elm)
        if elm[0] == qx and elm[1] == qy:
            arr[s,2] = data[idx,2]
            break
        idx = idx +1
    arr[s,0] =qx
    arr[s,1] =qy


x, y = data[:,[0,1]].T
k = kde.gaussian_kde(data.T)
nbins = 400
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = data[:,[2]]
fig, axes = plt.subplots()
axes=plt.pcolormesh(xi,yi, zi.reshape(xi.shape),shading='gouraud', cmap=plt.cm.RdBu_r)


x, y = arr[:,[0,1]].T
k = kde.gaussian_kde(arr.T)
nbins = 400
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = arr[:,[2]]
fig, axes = plt.subplots()
axes=plt.pcolormesh(xi,yi, zi.reshape(xi.shape),shading='gouraud', cmap=plt.cm.RdBu_r)

theta = np.radians(30)
c, s = np.cos(theta), np.sin(theta)
R = np.array(((c,-s), (s, c)))

###working
arr = np.reshape(data[:,2],(400,400)) 
arr2 = np.zeros(arr.shape)       
for deg in [0,90,180,270]:
    theta = math.radians(deg)  

    for x in range(399):
        for y in range(399):
            xy = (y,x)
            qx,qy = rotate_around_point_highperf(xy, theta, origin=(199, 199))
    #        print(qx,qy)
            arr2[int(qy),int(qx)]=arr2[int(qy),int(qx)]+arr[y,x]

plt.imshow(arr2)
arr4 = arr2[199,200:]
arr5 = arr4/max(arr4)
plt.plot(arr5)
arr6 =[]
for s in range(len(arr5)):
    arr6.append(sum(arr5[:s]))
arr6 = arr6/max(arr6)
plt.plot(list(data[-200:,1]),list(arr6))
plt.title('Area along one slice of light spot')
plt.xlabel('Position (mm)')
plt.ylabel('Area (1)')
plt.grid()

data[-200:,1][:len(arr6[arr6 < 0.9995])][-1]

import cv2

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result    


"""
Lyle Scott, III  // lyle@ls3.io
Multiple ways to rotate a 2D point around the origin / a point.
Timer benchmark results @ https://gist.github.com/LyleScott/d17e9d314fbe6fc29767d8c5c029c362

"""
from __future__ import print_function

import math
import numpy as np


def rotate_via_numpy(xy, radians):
    """Use numpy to build a rotation matrix and take the dot product."""
    x, y = xy
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [x, y])

    return float(m.T[0]), float(m.T[1])


def rotate_origin_only(xy, radians):
    """Only rotate a point around the origin (0, 0)."""
    x, y = xy
    xx = x * math.cos(radians) + y * math.sin(radians)
    yy = -x * math.sin(radians) + y * math.cos(radians)

    return xx, yy


def rotate_around_point_lowperf(point, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "low performance" version since it's recalculating
    the same values more than once [cos(radians), sin(radians), x-ox, y-oy).
    It's more readable than the next function, though.
    """
    x, y = point
    ox, oy = origin

    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

    return qx, qy

def rotate_around_point_highperf(xy, radians, origin=(0, 0)):
    """Rotate a point around a given point.
    
    I call this the "high performance" version since we're caching some
    values that are needed >1 time. It's less readable than the previous
    function but it's faster.
    """
    x, y = xy
    offset_x, offset_y = origin
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = math.cos(radians)
    sin_rad = math.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y

    return qx, qy

if __name__ == '__main__':
    theta = math.radians(90)
    point = (5, -11)

    print(rotate_via_numpy(point, theta))
    print(rotate_origin_only(point, theta))
    print(rotate_around_point_lowperf(point, theta))
    print(rotate_around_point_highperf(point, theta))
