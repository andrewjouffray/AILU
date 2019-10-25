import cv2
import sys
# sys.path.insert(1, '../')
import ailu_python.image_processing.masks as masks

def black_to_image(blacked_img_og, background_image):


    # makes a copy of the blacked image
    blacked_img = blacked_img_og.copy()

    # gets dimensions of the blacked_image
    height, width, channels = blacked_img.shape

    # resize the background image to match the blacked out image
    background_image = cv2.resize(background_image, (width, height))


    # get all the blacked pixels
    blk_mask = masks.black_mask_return_mask(blacked_img)

    # all pixels that were not black are going to have the blacked out image on them
    blacked_img[blk_mask != 0] = [0, 0, 0]

    # all pixels that were black are going to have the background image on them
    background_image[blk_mask == 0] = [0, 0, 0]

    # add the two together
    img = background_image + blacked_img


    return img