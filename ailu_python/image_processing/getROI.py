import numpy as np
import cv2

"""
Finds the region of interest using the blacked out image
"""
def using_color(image):

    # Makes the color image Black and White
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray_image = cv2.GaussianBlur(gray_image, (3, 3), cv2.BORDER_DEFAULT)
    # All the pixels that are not black, become white
    ret, threshold = cv2.threshold(gray_image,75,255,cv2.THRESH_BINARY)

    # All white specs that are smaller than 10 by 10 are removed
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

    # Fills the black space between white pixels that are at least 60 pixels close
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300, 300))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

    # Uncomment those two lines of you want to see what it looks like:
    # cv2.namedWindow('threshold images', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('threshold images', threshold)

    # Gives us the contours around the object of interest
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # creates an empty list to contain all the contours
    valid_contours = []

    for c in contours:
        # Gets the area of each contours in the image
        area = cv2.contourArea(c)
        # save the x1, y1, x2, y2, coordinates of that contour if it's larger than 3000 pixels
        if area > 500:
            x, y, w, h = cv2.boundingRect(c)
            xy_coordinates = [x, y, x+w, y+h]
            valid_contours.append(xy_coordinates)

    topx = 0
    topy = 0
    topxw = 0
    topyh = 0



    # checks to see if there are valid contours and returns them
    if valid_contours:
        for xy_coordinates in valid_contours:
            if xy_coordinates[0] > topx:
                topx = xy_coordinates[0]

            if xy_coordinates[1] > topy:
                topy = xy_coordinates[1]

            if xy_coordinates[2] > topxw:
                topxw = xy_coordinates[2]

            if xy_coordinates[3] > topyh:
                topyh = xy_coordinates[3]

        bdn_box = [topx, topy, topxw, topyh]

        valid_contours = [bdn_box]
        return valid_contours
    else:
        # If there are no valid contours return this
        return [[0,0,0,0]]

def using_color_on_canvas(image):

    # Makes the color image Black and White
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # gray_image = cv2.GaussianBlur(gray_image, (3, 3), cv2.BORDER_DEFAULT)
    # All the pixels that are not black, become white
    ret, threshold = cv2.threshold(gray_image,10,255,cv2.THRESH_BINARY)

    # All white specs that are smaller than 10 by 10 are removed
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

    # Fills the black space between white pixels that are at least 60 pixels close
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (90, 90))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

    # Uncomment those two lines of you want to see what it looks like:
    # cv2.namedWindow('threshold images', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('threshold images', threshold)

    # Gives us the contours around the object of interest
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # creates an empty list to contain all the contours
    valid_contours = []

    for c in contours:
        # Gets the area of each contours in the image
        area = cv2.contourArea(c)
        if area > 50:
            # save the x1, y1, x2, y2, coordinates of that contour if it's larger than 3000 pixels
            x, y, w, h = cv2.boundingRect(c)
            xy_coordinates = [x, y, x+w, y+h]
            valid_contours.append(xy_coordinates)


    # checks to see if there are valid contours and returns them
    if valid_contours:
        return valid_contours
    else:
        # If there are no valid contours return this
        return [[0,0,0,0]]