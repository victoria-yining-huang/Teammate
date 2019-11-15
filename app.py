# app.py
import string
import random
from flask import Flask, request, jsonify, send_from_directory
from time import sleep
import multiprocessing as mp
app = Flask(__name__)


@app.route('/app/<path:path>')
def send_js(path):
    return send_from_directory('pages', path)


@app.route('/start-model', methods=['POST'])
def start():
    content = request.get_json()
    result = start_model(content)
    return(jsonify(result))


@app.route('/status', methods=['POST'])
def check():
    data = request.get_json()
    key = data["key"]
    result = get_model_status(key)
    return(jsonify(result))


@app.route('/stop-model', methods=['POST'])
def stop():
    print("stop!")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)


manager = mp.Manager()
model_dict = manager.dict()
process = mp.Process()
is_running = False
key = None


def generate_key(length):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))


def init():
    global is_running
    global key
    global model_dict

    is_running = False
    key = None
    model_dict = manager.dict()


def generateTeams(model_input, model_dict, key):
    print("start")
    sleep(10)
    model_dict["status"] = "finished"
    model_dict["output"] = {
        "test": 1,
        "vals": [1, 2, 3]
    }
    print("stop")


def start_model(content):
    global process
    global is_running
    global key

    try:
        # if model is inactive
        if not is_running:
            # generate unique key for session
            key = generate_key(30)
            is_running = True

            # create model process
            process = mp.Process(target=generateTeams,
                                 args=(content, model_dict, key))

            # start model process
            process.start()
        # if model is active
        else:
            # return failed message
            return({
                "Status": "failed",
                "Message": "Model is already running",
                "METHOD": "POST"
            })
    except Exception as e:
        # an error occured starting the model, return failed
        init()
        return({
            "Status": "failed",
            "Message": e,
            "METHOD": "POST"
        })

    # the model started properly, return success and session key
    return({
        "Status": "success",
        "Message": "The model was started.",
        "Key": key
    })


def get_model_status(req_key):
    global is_running

    if is_running:
        if req_key == key:
            if not process.is_alive():
                is_running = False
            return({
                "Status": "success",
                "Body": {
                    "ModelIsFinished": False
                }
            })
        else:
            return({
                "Status": "failed",
                "Message": "Invalid key. The model was not started from your session.",
                "METHOD": "POST"
            })
    else:
        if req_key == key:
            if model_dict["status"] == "finished":
                result = model_dict["output"]
                init()
                return({
                    "Status": "success",
                    "Body": {
                        "ModelIsFinished": True,
                        "Output": result
                    }
                })
            else:
                return({
                    "Status": "failed",
                    "Message": "Unknown model state.",
                    "METHOD": "POST"
                })
        else:
            if key is None:
                return({
                    "Status": "failed",
                    "Message": "No active model or available model result.",
                    "METHOD": "POST"
                })
            else:
                return({
                    "Status": "failed",
                    "Message": "Invalid key. The model was not started from your session.",
                    "METHOD": "POST"
                })
