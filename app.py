# app.py
from flask import Flask, request, jsonify, send_from_directory
from time import sleep
import multiprocessing as mp
from model_manager import start_model, get_model_status
app = Flask(__name__)


@app.route('/app/<path:path>')
def send_js(path):
    return send_from_directory('pages', path)


@app.route('/start', methods=['POST'])
def start():
    content = request.get_json()

    result = start_model(content)

    return(jsonify(result))


@app.route('/check', methods=['POST'])
def check():
    content = request.get_json()

    #status = get_model_status(content)

    return(jsonify({

    }))


@app.route('/stop', methods=['POST'])
def stop():
    print("stop!")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
