import multiprocessing as mp
from time import sleep
import random
import string

manager = mp.Manager()
model_dict = manager.dict()
process = mp.Process()


def generate_key(length):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))


def init_model_dict():
    model_dict["key"] = None
    model_dict["status"] = "ready"
    model_dict["output"] = None


init_model_dict()


def generateTeams(model_input, model_dict):
    print("start")
    sleep(5)
    model_dict["status"] = "finished"
    model_dict["output"] = {
        "test": 1,
        "vals": [1, 2, 3]
    }
    print("stop")


def start_model(content):
    global process
    global model_dict

    try:
        # if model is inactive
        if not process.is_alive() and model_dict["status"] is not "running":
            # generate unique key for session
            key = generate_key(30)

            # update global dictionary
            model_dict["key"] = key
            model_dict["status"] = "running"

            # create model process
            process = mp.Process(target=generateTeams,
                                 args=(content, model_dict))

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
        init_model_dict()
        return({
            "Status": "failed",
            "Message": e,
            "METHOD": "POST"
        })

    # the model started properly, return success and session key
    return({
        "Status": "started",
        "Key": key
    })


def get_model_status(key):
    if process.is_alive():
        if key == model_dict["key"]:
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
        if key == model_dict["key"]:
            if model_dict["status"] == "finished":
                result = model_dict["output"]
                init_model_dict()
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
            if model_dict["key"] is None:
                return({
                    "Status": "failed",
                    "Message": "No active model or available model result.",
                    "METHOD": "POST"
                })
            else:
                return({
                    "Status": "success",
                    "Message": "Invalid key. The model was not started from your session.",
                    "METHOD": "POST"
                })
