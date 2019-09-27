import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.data_augmentation.modify_background as modBackground
import ailu_python.utils.display as display

# open video from avi file
cap = cv2.VideoCapture('./data/1569604389.9166079output.avi')

while True:

    # read each frame
    ret, frame = cap.read()

    # load a background image from the example data folder
    background_image = cv2.imread("./data/Image_resources_data_augmentation/DSC03356.jpg")

    # add the background
    frame_with_background = modBackground.black_to_image(frame, background_image)

    # gets the coordinates of the roi
    rois = getROI.using_color(frame)

    # draws the roi on the image
    display.draw_and_show(frame_with_background, rois, 'frame from video')

    # press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break