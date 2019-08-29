# AILU


Points:
-  description of the project
-  how to do object detection
-  the big picture
-  This is a startup, expectations


## Description of the AILU project:

AILU stands for Automated Imaging and Labeling Unit, the purpose of this robot is to take images of object, lots of images of lots of objects.

Why? We want to make robots able to recognize any objects, especially weird and unfamilliar ones, and many companies have werd objects that they want their robots to recognize, currently it's not possible for them to obtain the object detection model that they need. And there is a market wide open for us.

## Object detection

We plan on using the tensorflow object detection API to train our computer models on, this tool is very easy to use and give us great flexibility.

The basics of how to use the API goes as follow:

### 1 Images:
We need a lot of images, especially if we need to recognize a lot of different objects, here is an example of images (the green box will not be used in the actual images)

![exampe_image](test_img1.png)



And an XML file with the same name, that contains the metadata of the object:

    <?xml version="1.0"?>

    -<annotation>
        <folder>realsense</folder>
        <filename>1566946802.2614963.png</filename>
        <path>F:/realsense-python/thresholding/data/realsense/1566946802.2614963.png</path>

        -<source>
            <database>AndroBotics</database>
        </source>

        -<size>
            <width>640</width>
            <height>480</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>

        -<box>
            <name>little box</name> // name of the object
            <pose>Unspecified</pose>
            <truncated>0</truncated>
            <difficult>0</difficult>

            -<bndbox>             // position of the object 
                <xmin>269</xmin>
                <ymin>81</ymin>
                <xmax>495</xmax>
                <ymax>415</ymax>
            </bndbox>
         </box>
    </annotation>



So the data folder ends up looking somethings like this:

![folder](folder_eaxmple.png)


