#!/usr/bin/env python
# coding: utf-8

# In[33]:


import cv2
import numpy as np 
import time
import os


# In[34]:


def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# In[35]:


#ranges of hsv colors that can be identified 
#[ 93 235 234] [133 275 274] close-up blue

def object_mask(hsv_img):
    keepl = np.array([93, 235, 234])
    keeph = np.array([133, 275, 274])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img


# In[36]:


def main():
    
    img_depth = cv2.imread("C:/Users/Andrew/Documents/realsense-python/thresholding/imgs/depth.png", cv2.IMREAD_COLOR)
    img_color = cv2.imread("C:/Users/Andrew/Documents/realsense-python/thresholding/imgs/color.png", cv2.IMREAD_COLOR)
    viewImage(img_depth)
    viewImage(img_color)
            
    

main()
