import cv2
import numpy as np 
import time
import os



def create_training_data():
    path = os.path.join('./', 'basil_green') #finds the path to dogs or cat
    training_data = []
    for img in os.listdir(path):
        try:
            img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR) #turns images in grayscale
            training_data.append([img_array]) #adds the data in the array
            print('added a picture')
        except Exception as e:
            print('problem')
            pass

    return training_data

def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def red_mask(hsv_img):
    keepl = np.array([1, 247, 88])
    keeph = np.array([11, 257, 108])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])


    redl1 = np.array([0, 100, 100])
    redh1 = np.array([10, 255, 255])
    curr_mask = cv2.inRange(hsv_img, redl1, redh1)
    hsv_img[curr_mask > 0] = ([0,0,0])


    redl2 = np.array([170, 70, 50])
    redh2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_img, redl2, redh2)
    hsv_img[mask2 > 0] = ([0,0,0])
    viewImage(hsv_img) ## 3
    return hsv_img

def green_mask(hsv_img):
    greenl = np.array([39, 67, 202])
    greenh = np.array([79, 107, 242])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([37, 57, 152])
    greenh = np.array([77, 97, 192])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([39, 62, 133])
    greenh = np.array([79, 102, 173])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([35, 57, 178])
    greenh = np.array([75, 97, 218])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([40, 64, 230])
    greenh = np.array([80, 104, 270])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([38, 24, 235])
    greenh = np.array([78, 64, 275])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])


    greenl = np.array([42, 64, 150])
    greenh = np.array([82, 104, 190])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])

    greenl = np.array([38, 100, 50])
    greenh = np.array([75, 255, 255])
    mask2 = cv2.inRange(hsv_img, greenl, greenh)
    hsv_img[mask2 > 0] = ([0,0,0])
    # viewImage(hsv_img) ## 3
    return hsv_img

count = 0

for img in os.listdir('./cucumber'):

    count += 1

    try:
        img = cv2.imread(os.path.join('./cucumber', img), cv2.IMREAD_COLOR)
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # viewImage(hsv_img) ## 1

        # viewImage(hsv_img)

        hsv_img = green_mask(hsv_img)

        # viewImage(hsv_img)

        gray = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)

        # viewImage(gray)

        ret, threshold = cv2.threshold(gray, 0, 255, 0)

        # viewImage(threshold) ## 4

        contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        print(count)

        for c in contours:

            epsilon = 0.1*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            area = cv2.contourArea(c)
            if area > 8000:
                # print("writing new R.O.I")
                x, y, w, h = cv2.boundingRect(c)
                roi = img[y:y+h, x:x+w]
                cv2.imwrite("./isolated_seeds/roi"+str(time.time())+".png", roi)

    except Exception as e:
        print('problem')
        pass