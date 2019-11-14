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

    key = generate_key(30)

    model_dict["key"] = key
    model_dict["status"] = "running"

    try:
        if not process.is_alive():
            process = mp.Process(target=generateTeams,
                                 args=(content, model_dict))
            process.start()
    except Exception as e:
        return({
            "Status": "failed",
            "Message": e,
            "METHOD": "POST"
        })

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
