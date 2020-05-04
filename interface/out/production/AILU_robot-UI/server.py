from flask import Flask, json
from flask import request
import time

companies = [{"status": "ready", "name": "AILU robot 0001"}]

api = Flask(__name__)

@api.route('/status', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/next', methods=['POST'])
def post_companies():
    print("robot is waking up")
    time.sleep(1)
    print(request.data)
    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run()