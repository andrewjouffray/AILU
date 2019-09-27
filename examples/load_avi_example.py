import cv2

# open video from avi file
cap = cv2.VideoCapture('./data/1569604389.9166079output.avi')
while True:

    # read each frame
    ret, frame = cap.read()

    # show each frame
    cv2.imshow("frame", frame)

    # press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break