import cv2
import ailu_python.utils.display as display
import record_files.stream_and_save_color as save

# reads the video file
cap = cv2.VideoCapture(0)

while True:

    # checks if there is an image and gets the image
    ret, color_image = cap.read()
    if ret:

        # gets the dimensions of the image
        height, width, channels = color_image.shape

        # resize it to fix the users screen
        color_image = cv2.resize(color_image, (int(width / 1.5), int(height / 1.5)))

        # show the image to the user
        display.draw_and_show(color_image, [[0,0,0,0]], "Robot Eye")

        k = cv2.waitKey(33)
        # breaks if you press 'p'
        if k == 112:
            break

        # starts saving the stream
        elif k == 115:
            cap.release()

            # path to save the file at
            folder = "C:/Users/andre/Pictures/Video Projects/"
            save.get_video(folder)
    else:
        print("no image")
        cap = cv2.VideoCapture(0)
        ret, color_image = cap.read()


cv2.destroyAllWindows()










