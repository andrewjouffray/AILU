# Tools

This is a list of tools used to create the dataset of images needed to train the neural networks.

## Creating a Data-set:

**Step1**: Gather backgrounds. bckgrnds.py

download files from youtuve or personal video file, make sure they do not contain objects that might be objects of interest in them.
example: Do not use a video about cars to create background images for a neural network to recognize cars.

Use the bckgrnd.py tool to process the video files into individual .png files that can be loaded later.


**Step2**: Gather data. record.py

Gathering image data in .avi files using the robots. It is critical that the image quality is as good as possible, in focus and that the background is of a plain color
easily distinguishable from the object of intrest. Remeber to make some tarining data (90%) and testing data (10%)

**Step3**: Extract the ooi. extract.py

Use the extract.py tool to do that. Locate the .avi files you just saved with the robot, find an output directory, launch the program, click on the pixels that you want to keep (click on the left image, not the right one). Then save the color range to keep, and process all the video files, and save them into the output folder.

**Step4**: Augment the data. augment.py

Once all the video files are processed, launch the augment app, locate the extracted .avi files, create an output path and start augmenting. I t is important to know that if you have several classes in your data, you need to output all those classes to the same ouput folder, and only seperate validation data from training data. 

Documentation info [here](../doc/augment.md)

Augment will generate image data with many different resolutions, aspect ratios, brightness, and saturation, scale, and geometric transformations. The output folders are formated to be emmidiately use with the tensorflow object detection API.



   
