# Data_augmentation

This is where a lot of work needs to be done.

[Go back](../../)

### Dependecies:
-   OpenCV for python `pip install opencv-python`

##Project description:
Add new functions to the `ailu_python.data_augmentation` module, this is extremely important.

###functions needed:
- duplicate the ROIs
- rotate the ROIs
- scale up or down the ROIs
- perform geometric transformations on the ROIs
- change the backgrounds

###Basic process:

load the .avi file'

    
    import cv2
    
    cap = cv2.VideoCapture('./data/output.avi')
    while True:
        ret, frame = cap.read()
    
        cv2.imshow("frame", frame)
    
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
                
 get the ROI:


    rois = getROI.using_color(blacked_color_img)
    
 Do the modifications needed:

This is where we are now.