'''
This is the main file

input: directory containing processed video files from the robot, output directory.

step1: load the video file
step2: for each frame in the video, get the object of interest
step3: create a specified number of canvases with this object
step4: save those canvases in a specified folder along with data about the objects in a separate XML file
step5: repeat until there are no more video files

output: Large number of random training data

'''