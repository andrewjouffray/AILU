import cv2
import sys
sys.path.insert(1, '../')
from image_processing import masks

def black_to_image(color_image_og, depth_image_og, alpha):

    background_image = cv2.imread("../Data_augmentation/Image_resources_data_augmentation/DSC03356.jpg")

    color_image = color_image_og.copy()
    depth_image = depth_image_og.copy()

    height, width, channels = color_image.shape

    background_image = cv2.resize(background_image, (width, height))

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

    # Changes the depth image from BGR to HSV
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

    # Turns all blue pixels into white pixels
    mask = masks.object_mask(hsv_depth)

    # Saves the pixels in the mask, and blacks out all other pixels
    res = cv2.bitwise_and(color_image,color_image, mask=mask)


    blk_mask = masks.black_mask_return_mask(res)

    color_image[blk_mask != 0] = [0, 0, 0]
    background_image[blk_mask == 0] = [0, 0, 0]

    img = background_image + color_image


    return img