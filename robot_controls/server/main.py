from flask import Flask
from flask import request
from robotControls import Compute


import robotControls as robot

app = Flask(__name__)

@app.route('/run', methods = ['POST'])
def run():
    
    thread_a = Compute(request.__copy__())
    thread_a.start()
    return "Processing in background", 200

app.run()