#!/usr/bin/env python
# coding: utf-8

# In[41]:


import cv2
import numpy as np 
import time
import os


# In[42]:


def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# In[43]:


IMG_HEIGHT = 360
IMG_WIDTH = 640

vertical_margin = int(360 / 9)
horizonal_margin = int(640 / 12)

height = int(360 * 0.91)
length = int(640 * 0.88)


# In[44]:


def main():
    

    img_depth = cv2.imread("./imgs/depth.png", cv2.IMREAD_COLOR)
    img_color = cv2.imread("./imgs/color.png", cv2.IMREAD_COLOR)
    old_depth = img_depth
    croped_depth = img_depth[vertical_margin:height, horizonal_margin:length]
    img_depth = cv2.resize(croped_depth,(640,360))
    images = np.hstack((img_color, old_depth, img_depth))
    viewImage(images)
    


# In[45]:


main()

