# ailu_python.image_processing

### Dependecies:

-   OpenCV for python `pip install opencv-python`

## .getObject

This is the file that handles blackening everything except the object, there are 3 functions available in this file.

### .getObject.using_depth():

This function takes in the images from different cameras and returns a single image.
It will just look for a close object and return that object

#### Arguments:
-   `color_image_og` this is the color image from the sony NEXT 5T
-   `depth_image_og` this is the depth image from the intel realsense D435 i
-   `alpha` this value determines how far can the depth data see, usually set to 0.16

#### Output:

- a single blacked out image with only the object close to the camera showing.
    
___
    
### .getObject.using_depth_and_green():

This is similar except it is used to get an object sitting on the green circle.

#### Arguments:
-   `color_image_og` this is the color image from the sony NEXT 5T
-   `depth_image_og` this is the depth image from the intel realsense D435 i
-   `alpha` this value determines how far can the depth data see, usually set to 0.16

#### Output:

- a single blacked out image with only the object close to the camera and on the green circle showing.
    
___    

### .getObject.using_depth_and_red():

This is similar except it is used to get an object sitting on the red circle.

#### Arguments:
-   `color_image_og` this is the color image from the sony NEXT 5T
-   `depth_image_og` this is the depth image from the intel realsense D435 i
-   `alpha` this value determines how far can the depth data see, usually set to 0.16

#### Output:

- a single blacked out image with only the object close to the camera and on the red circle showing.

## .getROI

This file contains functions that allows you to find the region of pixels around an object of interest 

### .getROI.using_color()

This function simply looks at any pixels that are not white and gets the contours around that object, then
it creates a bounding box around this contour and returns the coordinates.

#### Arguments:
-   `image` This is the image returned by one of the "getObject" functions.

#### Output:
- `[[x1, y1, x2, y2],[x1, y1, x2, y2]]` a list of coordinates for each bounding boxes

## .masks

masks are primarily used by the ".getObject" functions, they simply define a range of colors and create a "picture"
it's more like a 2D array but whatever... where ever the pixels are withing the defines color range
have a value of 1 and all other pixels have a value of 0.

### masks.depth_mask_return_mask()

this is the mask used on the depth color to find the nearest objects

#### Arguments:
-   `hsv_img` this is the depth image converted into H S V values

#### Output:
-   a mask over each light blue pixels (light blue pixels represent close objects)
___
### masks.black_mask_return_mask()

this is the mask used on blacked out image to find all the black pixels

#### Arguments:
-   `img` this is the simple blacked out image from one of the .getObject functions

#### Output:
-   a mask over each black pixels
___
### masks.red_mask_return_hsv()

This is a mask used on blacked out image from the getObject.using_depth(), where we do a second
mask to get all the red pixels.

#### Arguments:
-   `hsv_img` this is the hsv version of the blacked out image from one of the .getObject functions

#### Output:
-   an hsv_image where all red pixels are turned black
___
### masks.green_mask_return_hsv()

This is another mask used on blacked out image from the getObject.using_depth(), where we do a second
mask to get all the green pixels.

#### Arguments:
-   `hsv_img` this is the hsv version of the blacked out image from one of the .getObject functions

#### Output:
-   an hsv_image where all green pixels are turned black
