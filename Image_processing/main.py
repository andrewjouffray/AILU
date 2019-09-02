# import multiprocessing as mp
import time
# import Workers
import Chunk

# Those are not currently used, but we could have it choose it's resolution and fps
res = [1920, 1080]
fps = 30

if __name__ == '__main__':

    # alpha sets the depth sensitivity of the camera
    alpha = 0.16
    file_path = "./bag_files/object_detection.bag"
    save_dir = "C:/Users/Andrew/Documents/realsense-python/thresholding/AILU/Image_processing/data/"

    image_chunk = []
    roi_chunk = []

    start = time.time()
    # Saves the images from .bag file
    Chunk.loadChunk(file_path, alpha, save_dir)
    end = time.time()
    save_time = end - start
    print(300, "images in:", save_time, "seconds ||", 300 / save_time, "images per second")


