import cv2

# read video
cap = cv2.VideoCapture('./data/output.avi')
while True:
    ret, frame = cap.read()

    cv2.imshow("frame", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break