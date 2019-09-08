import numpy as np
import cv2


# The object mask simply looks for pixels in a certain color range and turns them all to a certain color
def object_mask(hsv_img):

    # Color range for light blue
    keepl = np.array([81, 235, 234])
    keeph = np.array([121, 275, 275])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to white
    hsv_img[keep_mask > 0] = ([255,255,255])

    # Returns an image wher all the pixels that were light blue are now all white
    return hsv_img


def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Returns the pixel coordinates for the region of interest in the image
def getROI(depth_image, alpha):

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

    # Changes the depth image from BGR to HSV
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

    # Turns all blue pixels into white pixels
    hsv_depth = object_mask(hsv_depth)

    # Makes the depth image Black and White
    gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)

    # All the pixels that are not white, become black
    ret, threshold = cv2.threshold(gray_depth, 240, 255, 0)
    normal = threshold

    # All white specs that are smaller than 10 by 10 are removed
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

    # Fills the black space between white pixels that are at least 60 pixels close
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)
    filtered = threshold

    # Show images
    images = np.hstack((normal, filtered))
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('threshold images', images)

    # Gives us the contours around the object of interest
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # creates an empty list to contain all the contours
    valid_contours = []

    for c in contours:
        # Gets the area of each contours in the image
        area = cv2.contourArea(c)
        # save the x1, y1, x2, y2, coordinates of that contour if it's larger than 1000 pixels
        if area > 1000:
            x, y, w, h = cv2.boundingRect(c)
            xy_coordinates = [x, y, x+w, y+h]
            valid_contours.append(xy_coordinates)

    if valid_contours:
        return valid_contours
    else:
        # If there are no valid contours return this
        return [[0,0,0,0]]