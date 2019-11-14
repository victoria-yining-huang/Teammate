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
    model_dict["status"] = "done"
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
        if not model_dict["status"] == "running":
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


def get_model_status():
    if model_dict["status"] == "running":
        print("running")
    elif model_dict["status"] == "done":
        print("done")
        print(model_dict["output"])
        model_dict["status"] = "new"
        model_dict["output"] = {}
    elif model_dict["status"] == "new":
        print("not created yet")
