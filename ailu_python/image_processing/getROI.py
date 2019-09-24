import numpy as np
import cv2

def using_color(image):

    # Makes the depth image Black and White
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # All the pixels that are not white, become black
    ret, threshold = cv2.threshold(gray_image, 10, 10, 0)

    # All white specs that are smaller than 10 by 10 are removed
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

    # Fills the black space between white pixels that are at least 60 pixels close
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

    # cv2.namedWindow('threshold images', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('threshold images', gray_image)

    # Gives us the contours around the object of interest
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # creates an empty list to contain all the contours
    valid_contours = []

    for c in contours:
        # Gets the area of each contours in the image
        area = cv2.contourArea(c)
        # save the x1, y1, x2, y2, coordinates of that contour if it's larger than 1000 pixels
        if area > 3000:
            x, y, w, h = cv2.boundingRect(c)
            xy_coordinates = [x, y, x+w, y+h]
            valid_contours.append(xy_coordinates)

    if valid_contours:
        return valid_contours
    else:
        # If there are no valid contours return this
        return [[0,0,0,0]]