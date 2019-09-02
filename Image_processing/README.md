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
    ├── Image_resources_data_augmnetation/  // Images that can be used in data augmentation 
    │   ├── background.jpg
    │   ├── DSC03356.JPG
    │   ├── DSC03368.JPG
    │   ├── DSC03412.JPG
    │   └── DSC03421.JPG
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
I you try stream video from the file, and you set it at a different resolution, it will crash.

    # Increases the resolution of the images (update Chunk.py if you change those settings)
    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # This will save the color and depth recording as a .bag
    config.enable_record_to_file('object_detection.bag')