import numpy as np
import cv2


# The object mask simply looks for pixels in a certain color range and turns them all to a certain color
def object_mask(hsv_img):

    # Color range for light blue[ 76 235 235] [116 275 275]
    keepl = np.array([76, 235, 235])
    keeph = np.array([116, 275, 275])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to white
    hsv_img[keep_mask > 0] = ([255,255,255])

    # Returns an image wher all the pixels that were light blue are now all white
    return hsv_img

def red_exclution_object_mask(hsv_img):

    #[-18 203 185] [ 22 243 225]
    #[-20 235 235] [ 20 275 275]
    # Color range for red [-18 171 175] [ 22 211 215]


    keepl = np.array([-18, 171, 175])
    keeph = np.array([22, 211, 215])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([255,255,255])

    keepl = np.array([-18, 203, 185])
    keeph = np.array([22, 243, 225])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([255,255,255])

    keepl = np.array([-20, 235, 235])
    keeph = np.array([20, 275, 275])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img


def green_exclution_object_mask(hsv_img):

    # Color range for light blue[ 76 235 235] [116 275 275]
    keepl = np.array([76, 235, 235])
    keeph = np.array([116, 275, 275])
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

    # # Show images
    # images = np.hstack((gray_depth, filtered))
    # cv2.namedWindow('threshold images', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('threshold images', images)

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

def getROI_red_exclution(color_image_og, rois):
    color_image = color_image_og.copy()
    roi = rois[0]
    if roi != [0,0,0,0]:
        ogx1 = roi[0]
        ogy1 = roi[1]
        ogx2 = roi[2]
        ogy2 = roi[3]
        cv2.rectangle(color_image, (ogx1, ogy1), (ogx2, ogy2), (0, 0, 255), 80)
        roi_color = color_image[ogy1:ogy2, ogx1:ogx2]

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

        # Changes the depth image from BGR to HSV
        color_HSV = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)

        # Turns all blue pixels into white pixels
        color_HSV = red_exclution_object_mask(color_HSV)

        # Makes the depth image Black and White
        gray_color = cv2.cvtColor(color_HSV, cv2.COLOR_BGR2GRAY)

        # All the pixels that are not white, become black
        ret, threshold = cv2.threshold(gray_color, 240, 255, cv2.THRESH_BINARY_INV)
        # normal = threshold
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)
        # Show images
        # # images = np.hstack((gray_depth, filtered))
        # cv2.namedWindow('threshold images', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('threshold images', threshold)

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
                xy_coordinates = [x+ogx1, y+ogy1, x+w+ogx1, y+h+ogy1]
                valid_contours.append(xy_coordinates)

        if valid_contours:
            return valid_contours
        else:
            # If there are no valid contours return this
            return [[0,0,0,0]]
    else:
        return [[0, 0, 0, 0]]

def draw_and_show(image, roi):
    roi = roi[0]
    x1 = roi[0]
    y1 = roi[1]
    x2 = roi[2]
    y2 = roi[3]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('color_image', image)