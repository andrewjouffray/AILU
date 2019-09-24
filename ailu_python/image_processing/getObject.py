import cv2
import ailu_python.image_processing.masks as masks

"""============================================================
    to be used with the mirror only
   ============================================================"""
# returns a black image with only the object of interest visible
def using_depth(color_image_og, depth_image_og, alpha):

    color_image = color_image_og.copy()
    depth_image = depth_image_og.copy()

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

    # Changes the depth image from BGR to HSV
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

    # Creates a mask over all light blue pixels
    mask = masks.depth_mask_return_mask(hsv_depth)

    # Saves the pixels in the mask, and blacks out all other pixels
    img = cv2.bitwise_and(color_image,color_image, mask=mask)

    return img


"""============================================================
    to be used with the red circle on the mirror
   ============================================================"""
def using_depth_and_red(color_image_og, depth_image_og, alpha):

    # copy the input images (to not modify the originals)
    color_image = color_image_og.copy()
    depth_image = depth_image_og.copy()

    # apply color to the depth image
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

    # Changes the depth image from BGR to HSV
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

    # Creates a mask over all light blue depth pixels
    mask = masks.depth_mask_return_mask(hsv_depth)

    # pixels in the mask save their color and all others are blacked out
    blacked_out_image = cv2.bitwise_and(color_image,color_image, mask=mask)

    # convert the blacked_out_image into an hsv image
    hsv_color = cv2.cvtColor(blacked_out_image, cv2.COLOR_BGR2HSV)

    # turn all red pixels into black pixels
    masked_red = masks.red_mask_return_hsv(hsv_color)

    #turn the hsv image back into a color image
    color_image = cv2.cvtColor(masked_red, cv2.COLOR_HSV2BGR)

    return color_image

"""============================================================
    to be used with the green circle on the mirror
   ============================================================"""
# returns a black image with only the object of interest visible
def using_depth_and_green(color_image_og, depth_image_og, alpha):

    color_image = color_image_og.copy()
    depth_image = depth_image_og.copy()


    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alpha), cv2.COLORMAP_JET)

    # Changes the depth image from BGR to HSV
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)


    # Creates a mask over all light blue depth pixels
    mask = masks.depth_mask_return_mask(hsv_depth)

    # Saves the pixels in the mask, and blacks out all other pixels
    res = cv2.bitwise_and(color_image,color_image, mask=mask)

    hsv_color = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    masked_red = masks.green_mask_return_hsv(hsv_color)
    color_image = cv2.cvtColor(masked_red, cv2.COLOR_HSV2BGR)

    return color_image