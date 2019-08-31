# import imageio
import xml.etree.cElementTree as ET
from time import time
from cv2 import imwrite
import numpy as np

def save_images(img, rois):
    # print(len(img))
    name = str(time())
    imwrite("./data/realsense/"+name+".png", img)
    FOLDER_NAME = "realsense"

    roi = rois[0]
    print(roi)
    x1 = roi[0]
    y1 = roi[1]
    x2 = roi[2]
    y2 = roi[3]
    print(x1, y1, x2, y2)

    img_np = img
    height = np.size(img_np, 0)
    width = np.size(img_np, 1)

    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = FOLDER_NAME
    ET.SubElement(annotation, "filename").text = name + ".png"
    ET.SubElement(annotation,
                  "path").text = "F:/realsense-python/thresholding/data/" + FOLDER_NAME + "/" + name + ".png"

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "AndroBotics"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(annotation, "segmented").text = "0"

    object0 = ET.SubElement(annotation, "box")
    ET.SubElement(object0, "name").text = "watch"
    ET.SubElement(object0, "pose").text = "Unspecified"
    ET.SubElement(object0, "truncated").text = "0"
    ET.SubElement(object0, "difficult").text = "0"

    bndbox = ET.SubElement(object0, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(x1)
    ET.SubElement(bndbox, "ymin").text = str(y1)
    ET.SubElement(bndbox, "xmax").text = str(x2)
    ET.SubElement(bndbox, "ymax").text = str(y2)

    tree = ET.ElementTree(annotation)
    tree.write("F:/realsense-python/thresholding/data/" + FOLDER_NAME + "/" + name + ".xml")

    return