import cv2

# Splits the roi into two and puts it in different places of the image
def shrear(img, rois):

    for roi in rois:

        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)