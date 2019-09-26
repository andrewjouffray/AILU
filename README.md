# AILU

_The information disclosed in the document is confidential and you are not allowed to
 share or distribute it with anyone._
 
## Description:

The AILU module has the goal of helping us isolate objects of interest that need to be
imaged, as well as finding teh region of interest around that object and finally 
augmenting the data to allow for more accurate computer models in diverse environments.

## Organization & Links

The module is called ailu_python and includes functions to process the images, augment data, and 
other utilities.

Module: [ailu_python](ailu_python):
-   [ailu_python.image_processing](ailu_python/image_processing/README.md) 
-   [ailu_python.data_augmentation](ailu_python/data_augmentation/README.md)
-   [ailu_python.utils](ailu_python/utils/README.md)

robot_controls:
-  [basic files to control the AILU robot](robot_controls/README.md)

examples:
-   several simple examples on how to use the ailu_python module
-   test data that you can use

## General process 

### Step1: obtain the data

We obtain data by simply having the robot film around the object in small video files
of about 20 seconds. We use both depth video from intel realsense and color video from 
a sony camera.

This is what the raw images look like: 


### Step2: process the data

Once we have those images we can process them to get a precise image of the object, with all the 
rest completely blacked out.

For this steps we use ailu_python.image_processing.getObject.using_depth_and_green(). To get the object of interest.

This is what the result looks like:

We then save all those images into a video file.

### Step3: augment the data

Now that we have a video file with hundreds of blacked out images, we can find teh ROI, modify it
and then put a new background instead of the black pixels