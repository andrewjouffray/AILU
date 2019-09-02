# Image Processing 

### Dependecies:

-   OpenCV for python `pip install opencv-python`
-   Numpy       `pip install numpy`
-   Matplotlib `pip install matplotlib`
-   Pyrealsense2:
You must install the latest Microsoft Visual Studio Community

    `pip install pillow`
    
    `pip install cython`
    
    `pip install pyrealsense2`
    
    
 ## File structure:
 

    Image_processing/
    ├── bag_files/
    │    └── object_detection.bag           // Video file containing the color a depth streams
    ├── data/
    │   └── realsense/                      // Images and XML files saved here
    └── legacy/                             // Old code and test
    │   ├── 3D thresholding.ipynb
    │   ├── 3D thresholding.py
    │   ├── 15framse_test.py
    │   ├── cam_test.ipynb
    │   ├── color_picker.py
    │   ├── Contourer.py
    │   ├── contouring.py
    │   ├── scaling_and_cropping.ipynb
    │   ├── scaling_and_cropping.py
    │   ├── view_mp_test.py
    │   └── viewer.ipynb
    ├── Bag_saver.py                       // Records 10 seconds of footage and saves it as a .bag file
    ├── Chunk.py                           // Loads the .bag file, processes images with utils.py and sends images to Worker.py  
    ├── main.py                            // Main file
    ├── Utils.py                           // Finds the region of intrest 
    ├── viewer.py                          // Streams from either the camera or a .bag file
    └── Worker.py                          // Saves images along with XML files 
    

 ## Recording a .bag file
 
You need the Intel D435i in order to record the .bag file, you don't worry about this step, I will try to upload a .bag
file that you can work with. But to record a .bag file all you need is to call the bag_saver.save_bag() function in order to record a 10s clip.
robot-controls-V2.py uses this function.

When recording the .bag file make sure you remember the setting (resolution and fps)
if you try to stream video from the file, and you set it at a different resolution, it will crash.

Follow this format `config.enable_stream(<type.of.stream>, <width>, <height>, <format>, <fps>)`

This is how you set the resolution:

    # Increases the resolution of the images (update Chunk.py if you change those settings)
    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # I think you can do 60 fps at that resolution
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # This will save the color and depth recording as a .bag
    config.enable_record_to_file('object_detection.bag')
    
## Streaming video 

Streaming is very useful to make sure you have the right frame and the right depth settings to 
properly contour the object.

__alpha__: This variable dictates the depth sensitivity, if you set it at `alpha=0.03` it will target everything, even the background
if you set it at `alpha=1` it will only target object that are super close, a good value for alpha is `alpha=0.16` 

By modifying the alpha value you can make the image processing more or less accurate, feel free to play with it.

To stream from file simply run the `viewer.py` file make sure that you are pointing to the correct
directory for the .bag file and that the file is not setup to stream from the camera:

-   `from_camera = False`

-    `    rs.config.enable_device_from_file(config, "<path to the .bag file>")`

Again make sure that you are streaming from the file at the correct resolution and fps.

## main.py

This is the main file, it simply calls the Chunk.loadChunk() function and records the time that it took
save all 300 images in the .bag file

## Chunk.py
`Chunk.loadChunk(<path to the .bag file>, <alpha value to be used>, <path to save the images and XML files>)`

This file contains the loadChunk() function that loads the .bag file, streams the depth and color images and 
sends the depth image to the Utils.getROI() function to get the region of interest
in the image.
It then calls the Workers.save_images() so actually save the images  

## Utils.py
`utils.getROI(depth_image, alpha)`

Pass the depth image abd the alpha settings, and it will return a list of coordinates of gerions of intrest in the image like this:

`[[x1, y1, x2, y2]]`

## Workers.py
`Workers.save_images(color_image, <list of regions of interest>, <path to save the images and XML files>)`

The save_image() function will save the color image as a png and write an XML file with the same name, containing the 
coordinates of the regions of interest in the image.  