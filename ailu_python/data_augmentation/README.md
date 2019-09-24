# Data Augmentation

Our goal is to take an image and apply random modifications to that image in order to 
multiply the number of images to be used while training the computer model.

I see those as functions called before we save the images in Chunk.py:



    def loadChunk(file_name, alpha, save_dir):
        pipeline = rs.pipeline()
        config = rs.config()
    
        rs.config.enable_device_from_file(config, "./"+file_name)
    
        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        profile = pipeline.start(config)
    
        align_to = rs.stream.color
        align = rs.align(align_to)
    
        im_count = 0
        while True:
    
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
    
            if not aligned_depth_frame or not color_frame:
                print("problem here")
                raise RuntimeError("Could not acquire depth or color frames.")
    
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
    
            # Gets the regions of interest in the image
            rois = utils.getROI(depth_image, alpha)
    
            
            // ADD THE DATA AUGMENTATION SOMEWHERE HERE <==============================================
    
            im_count += 1
            # Saves the images along with their XML files
            Workers.save_images(color_image, rois, save_dir)
    
            # Breaks the loop after 300 image
            if im_count == 300:
                print("STOP")
                break
                
Those functions could be called like this:

`modified_image, new_rois = modification_x(color_image, rois)`

Where the original image is passed along with the position of the object of interest, and new new modified image along with the new 
ROI coordinates is returned.

### Possible modifications:

10 functions each able to modify something specific would be awesome, a combination of those functions could increase even more
the diversity of those images.

Here are possible functions we could create:

-   Change background
- Flip ROI Horizontal / vertical
-   Flip background horizontal / vertical 
- Cubify the background
- Cut half of the ROI and paste it somewhere else in the image 

Feel free to make your own, and ignore the ones you feel would be too difficult or useless.