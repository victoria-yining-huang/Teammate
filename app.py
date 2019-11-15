# app.py
from flask import Flask, request, jsonify
from time import sleep
import multiprocessing as mp
import model_manager as mm
app = Flask(__name__)

app.config["APPLICATION_ROOT"] = "/python"


@app.route('/start-model', methods=['POST'])
def start():
    content = request.get_json()
    result = mm.start_model(content)
    return(jsonify(result))


@app.route('/status', methods=['POST'])
def check():
    data = request.get_json()
    key = data["key"]
    result = mm.get_model_status(key)
    return(jsonify(result))


@app.route('/ping', methods=['GET'])
def ping():
    return(jsonify(mm.ping_model()))


@app.route('/stop-model', methods=['POST'])
def stop():
    print("stop!")


if __name__ == '__main__':
    app.run(threaded=False, processes=1)
