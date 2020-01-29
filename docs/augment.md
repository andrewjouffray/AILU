# AndroBotics Augment Documentation

### Use:

This Application is designed to augment the image data and format the data into a usable dataset for machine learning.

**input:** Path to .AVI files.

**output:** a large dataset of augmented images alond with .xml files containing the pixel positions of objects in the images.

---

### Nomenclature:

**Frame**: A single still image coming from the .avi files that we are processing.

**Objects OF Interest (ooi)**: The object inside the frame.

**Canvas**: This is a randomly generate image with a background and a random number of ooi in it. This is what the ouput image woudld be.

___For each frame, several canvas can be created and several ooi can be inserted into each canvas.___

---

### Options:

Here are a list of options used to configure the augmentation.

- Input directory: Directory containing the .AVI files
- Output directory: Directory where you want the images and xml files to be saved 
- Multiply image: This is the number of canvases created for each frame from the .avi file 
- Number of objects: This is the maximum amount of objects in on canvas 
---
### How it works:

1. Augment will load the video files from the input directory, and iterate through each file.
2. The program will read each frame of the video and for each frame it will take the object of interest
3. The program then creates a certain number of canvases (number defines by "Multiply image")
4. Each canvas is given a random size, and one of the 5 aspec ratios
5. Each canvas copies the object of interest a certain number of time (number defines by "Number of Objects")
6. Each Objects of interest has random modifications applied to it (see modifications)
7. The program gets and save the coordinates of the objects of interest
8. Each canvas is given a background.
9. Each canvas has random modifications applied to it.
10. Each canvas is saved as a .png along with an .XML file of the same name containing the pixel coordinates of each object of interest  
---
 
### Modifications:

**Object Of Interest (ooi) Modifications**


These are modifications that can be applied on an individual ooi, meaning that in the same canvas, several ooi might look different, and have different modifications.

_all this code is located in ./augment_files/ooi.py_
- rorate(angle): Rotates the object a certain amount 0 - 360 degrees
- scale(size): scales the object to a certain percentage 0% - 200%
- affine(): still being worked on, perform affine transformation on the image 
- saturation(maxSaturation): Still being worked on, radomely changes the saturation value 
- changeGamma(value): changes the gamma on the image (brightness)


**Canvas Modifications**

These are modifications that will be applied to the entire canvas, background and ooi in the canvas.

_all this code will be located in ./augment_files/canvas.py_
- loweRes(percent): Lowers the resolution of the image
- blur(kernel size) adds a blur to the image

