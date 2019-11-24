import multiprocessing as mp
from time import sleep
import requests
import random
import string
from model import run_model
from flask import Response, jsonify

manager = mp.Manager()
model_dict = manager.dict()
process = mp.Process()


def generate_key(length):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))


def init():
    global model_dict
    model_dict = manager.dict()
    model_dict["key"] = None


def generate_teams(model_input, model_dict):

    print("!! run model")

    result = run_model(
        num_students=model_input["num_students"],
        num_teams=model_input["num_teams"],
        team_size=model_input["team_size"],
        conflicts=model_input["conflicts"],
        gpas=model_input["gpas"],
        ifgpa=model_input["ifgpa"]
    )

    print("!! model finished")

    print(result)

    model_dict["status"] = "finished"
    model_dict["result"] = result

    print("!! process finished")


def start_model(content):
    global process
    global model_dict

    try:
        # if model is inactive
        if not process.is_alive():
            # generate unique key for session
            key = generate_key(30)

            # create model process
            process = mp.Process(target=generate_teams,
                                 args=(content, model_dict))

            # start model process
            process.start()
        # if model is active
        else:
            # return failed message
            return jsonify({
                'Message': 'The model is already running'
            }), 503
    except Exception as e:
        # an error occured starting the model, return failed
        init()
        return jsonify({
            'Message': 'An error occured when starting the model. Error: \n{}'.format(e)
        }), 500

    # the model started properly, return success and session key
    model_dict["key"] = key
    return jsonify({
        'Message': 'The model was started.',
        'Key': key
    }), 200


def get_model_status(req_key):

    if process.is_alive():
        if model_dict["key"] == req_key:
            return jsonify({
                'Message': 'The model is still running',
                'ModelIsFinished': False
            }), 200
        else:
            return jsonify({
                'Message': 'Invalid key. The model was not started from your session.',
            }), 403
    else:
        if model_dict["key"]:
            if model_dict["key"] == req_key:
                result = model_dict["result"]
                init()
                return jsonify({
                    'Message': 'The model is finished.',
                    "ModelIsFinished": True,
                    "Result": result
                }), 200
            else:
                return jsonify({
                    'Message': 'Invalid key. The model was not started from your session.',
                }), 403
        else:
            return jsonify({
                'Message': 'No active model or available model result.',
            }), 404


def ping_model():
    return Response(
        response={
            "Message": "Test",
        },
        status=201)

# start_model({"test": [1, 2, 3]})
# key2 = "key"
# stop = False
# while not stop:
#     sleep(1)
#     res = get_model_status(key2)
#     print(res)
#     if (res["Status"] == "failed"):
#         stop = True
