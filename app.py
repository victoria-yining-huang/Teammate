# app.py
from flask import Flask, request, jsonify, send_from_directory
from time import sleep
from threading import Thread
app = Flask(__name__)


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/', methods=['GET'])
def ping():
    return("The server is active.")


def generateTeams():
    print("start")
    sleep(5)
    print("continue")
    sleep(10)
    print("continue")
    sleep(15)
    print("continue")
    sleep(20)
    print("stop")


@app.route('/start', methods=['POST'])
def start():
    key = request.form.get('key')

    thread = Thread(target=generateTeams)
    thread.start()

    return(jsonify({"Message": "Model started", "METHOD": "POST"}))

    # if param:
    #     return jsonify({
    #         "Message": f"Welcome {name} to our awesome platform!!",
    #         # Add this option to distinct the POST request
    #         "METHOD": "POST"
    #     })
    # else:
    #     return jsonify({
    #         "ERROR": "no name found, please send a name."
    #     })


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
