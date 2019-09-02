# import imageio
import xml.etree.cElementTree as ET
from time import time
from cv2 import imwrite
import numpy as np


# This function saves the image and write the xml file
def save_images(img, rois, dir):

    # Use the current time in ms as name
    name = str(time())

    # Saves the image
    imwrite(dir+name+".png", img)

    # folder to save the images in
    FOLDER_NAME = "realsense"

    # This will only save the first roi, we need to make it be able so save all the rois in the future.
    roi = rois[0]
    print(roi)
    x1 = roi[0]
    y1 = roi[1]
    x2 = roi[2]
    y2 = roi[3]
    print(x1, y1, x2, y2)

    # get the height a width of image
    img_np = img
    height = np.size(img_np, 0)
    width = np.size(img_np, 1)

    # XML starts here
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = FOLDER_NAME
    ET.SubElement(annotation, "filename").text = name + ".png"
    # This path is important, this is where the XML files will be saved
    ET.SubElement(annotation,
                  "path").text = dir + FOLDER_NAME + "/" + name + ".png"

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "AndroBotics"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(annotation, "segmented").text = "0"

    # Change the name depending on what the object is
    object0 = ET.SubElement(annotation, "box")
    ET.SubElement(object0, "name").text = "watch"
    ET.SubElement(object0, "pose").text = "Unspecified"
    ET.SubElement(object0, "truncated").text = "0"
    ET.SubElement(object0, "difficult").text = "0"

    # This is where the region containing the object is defined
    bndbox = ET.SubElement(object0, "bndbox")
    ET.SubElement(bndbox, "xmin").text = str(x1)
    ET.SubElement(bndbox, "ymin").text = str(y1)
    ET.SubElement(bndbox, "xmax").text = str(x2)
    ET.SubElement(bndbox, "ymax").text = str(y2)

    # Writes the XML file
    tree = ET.ElementTree(annotation)
    tree.write(dir + FOLDER_NAME + "/" + name + ".xml")

    return