import numpy as np
import cv2


# looks or pixels in a certain range of color and returns a mask
def depth_mask_return_mask(hsv_img):

    # Color range for light blue[ 76 235 235] [116 275 275]
    keepl = np.array([76, 235, 235])
    keeph = np.array([116, 275, 275])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)

    return keep_mask

# looks or pixels in a certain range of color and returns a mask
def black_mask_return_mask(img):

    # Color range for black
    keepl = np.array([0, 0, 0])
    keeph = np.array([116, 0, 0])
    keep_mask = cv2.inRange(img, keepl, keeph)

    # Returns an image where all the pixels that were light blue are now all white
    return keep_mask

def green_mask_return_mask(hsv_img):

    # gets all pixels in that range of green
    keepl = np.array([20, 50, 50])
    keeph = np.array([90, 255, 255])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)

    return keep_mask


# Looks or pixels in a certain range of color and returns an hsv_image with those pixels blacked out
def red_mask_return_hsv(hsv_img):

    # gets all pixels in that range of red
    keepl = np.array([-18, 171, 175])
    keeph = np.array([22, 211, 215])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    keepl = np.array([-18, 203, 185])
    keeph = np.array([22, 243, 225])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    keepl = np.array([-20, 235, 235])
    keeph = np.array([20, 275, 275])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    keepl = np.array([0, 70, 50])
    keeph = np.array([10, 255, 225])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    keepl = np.array([170, 70, 50])
    keeph = np.array([180, 255, 255])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    return hsv_img

# Looks or pixels in a certain range of color and returns an hsv_image with those pixels blacked out
def green_mask_return_hsv(hsv_img):

    # gets all pixels in that range of green
    keepl = np.array([30, 100, 50])
    keeph = np.array([90, 255, 255])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    return hsv_img

def blue_mask_return_hsv(hsv_img):

    # gets all pixels in that range of green
    keepl = np.array([95, 40, 40])
    keeph = np.array([140, 255, 255])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # turns them all to black
    hsv_img[keep_mask > 0] = ([0,0,0])

    return hsv_img