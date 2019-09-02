# import multiprocessing as mp
import time
# import Workers
import Chunk

res = [1920, 1080]
fps = 30
if __name__ == '__main__':

    image_chunk = []
    roi_chunk = []

    start = time.time()
    Chunk.loadChunk("./bag_files/object_detection.bag")
    end = time.time()
    save_time = end - start


    # jobs = []
    # start = time.time()
    # print("img "+str(len(image_chunk)))
    # print("roi "+str(len(roi_chunk)))
    # for i in range(len(image_chunk)):
    #     p = mp.Process(target=Workers.save_images, args=(image_chunk[i],roi_chunk[i],))
    #     jobs.append(p)
    #     p.start()
    # p.join()
    # end = time.time()
    # save_time = end - start
    print(300, "images in:", save_time, "seconds ||", 300 / save_time, "images per second")


