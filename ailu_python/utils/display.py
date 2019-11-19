import cv2

def draw_and_show(image, rois, name):

    for roi in rois:
        x1 = roi[0]
        y1 = roi[1]
        x2 = roi[2]
        y2 = roi[3]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, image)