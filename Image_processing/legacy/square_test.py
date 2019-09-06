import cv2
from time import sleep
img = cv2.imread('F:/AILU_data/images/train/roi1567652094.5718951.png',cv2.IMREAD_COLOR)
cv2.rectangle(img, (262, 67), (437, 368), (0, 255, 0), 3)
def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
viewImage(img)