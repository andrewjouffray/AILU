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
    

