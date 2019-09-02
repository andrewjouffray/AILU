from random import shuffle


IMG_HEIGHT = 480
IMG_WIDTH = 640

# how many cubes per row?
DIVISOR = 16

# cuts an image into little pieces and re-assembles in a random way
# You would need to re-paste the roi on top of that cubed image
def img_cuber(img):
    height_div = int(480 / DIVISOR)
    width_div = int(640 / DIVISOR)
    posY = 0
    posX = 0

    cube_img = []

    # cunts the image into cubes
    for i in range(DIVISOR):
        for j in range(DIVISOR):
            roi = img[posY:posY + height_div, posX:posX + width_div]
            posY += height_div
            cube_img.append(roi)

        posX += width_div
        posY = 0

    # Shuffles the position of those cubes in the image
    shuffle(cube_img)

    posY = 0
    posX = 0

    count = 0

    # Replaces the normal image with the random cubes.
    for i in range(DIVISOR):
        for j in range(DIVISOR):
            img[posY:posY + height_div, posX:posX + width_div] = cube_img[count]
            #             print(count)
            count += 1
            posY += height_div
            cube_img.append(roi)

        posX += width_div
        posY = 0

    return img