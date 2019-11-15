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


def init():
    global model_dict
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

    try:
        # if model is inactive
        if not is_running:
            # generate unique key for session
            key = generate_key(30)

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


def get_model_status():

    #         if not process.is_alive():
    #             is_running = False
    #         return({
    #             "Status": "success",
    #             "Body": {
    #                 "ModelIsFinished": False
    #             }
    #         })
    #     else:
    #         return({
    #             "Status": "failed",
    #             "Message": "Invalid key. The model was not started from your session.",
    #             "METHOD": "POST"
    #         })
    # else:
    #         if model_dict["status"] == "finished":
    #             result = model_dict["output"]
    #             init()
    #             return({
    #                 "Status": "success",
    #                 "Body": {
    #                     "ModelIsFinished": True,
    #                     "Output": result
    #                 }
    #             })
    #         else:
    #             return({
    #                 "Status": "failed",
    #                 "Message": "Unknown model state.",
    #                 "METHOD": "POST"
    #             })
    #     else:
    #         if key is None:
    #             return({
    #                 "Status": "failed",
    #                 "Message": "No active model or available model result.",
    #                 "METHOD": "POST"
    #             })
    #         else:
    #             return({
    #                 "Status": "failed",
    #                 "Message": "Invalid key. The model was not started from your session.",
    #                 "METHOD": "POST"
    #             })


start_model({"test": [1, 2, 3]})
key2 = key
stop = False
while not stop:
    sleep(1)
    res = get_model_status(key2)
    print(res)
    if (res["Status"] == "failed"):
        stop = True
