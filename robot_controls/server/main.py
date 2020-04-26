from flask import Flask
from flask import request, jsonify
import robotControls as robot

app = Flask(__name__)

@app.route('/run', methods = ['POST'])
def run():
    data = request.form
    dataSetName = data["dataSetName"]
    label = data["label"]
    images = int(data["images"])
    track = bool(data["track"])
    lowerLimit = int(data["lowerLimit"])
    rotateLimit = int(data["rotateLimit"])
    lights = int(data["lights"])
    datasetType = data["type"]
    bndBoxes = bool(data["bndBoxes"])
    masks = bool(data["bndBoxes"])

    message = robot.runRobot(dataSetName, label, images, track, lights, lowerLimit, rotateLimit, type, bndBoxes, masks)

    responce = {"message":message, "id":"0001"}
    return jsonify(responce)

app.run()