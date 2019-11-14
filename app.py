# app.py
from flask import Flask, request, jsonify, send_from_directory
from time import sleep
import multiprocessing as mp
from model_manager import start_model, get_model_status
app = Flask(__name__)


@app.route('/app/<path:path>')
def send_js(path):
    return send_from_directory('pages', path)


@app.route('/start-model', methods=['POST'])
def start():
    content = request.get_json()
    key = content["model_key"]
    result = start_model(key)
    return(jsonify(result))


@app.route('/status', methods=['POST'])
def check():
    data = request.get_json()
    print(data)
    result = get_model_status(data["model_key"])
    return(jsonify(result))


@app.route('/stop-model', methods=['POST'])
def stop():
    print("stop!")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
