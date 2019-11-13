# app.py
from flask import Flask, request, jsonify, send_from_directory
from time import sleep
from rq import Queue
from worker import conn
from test_worker import test
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


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server


@app.route('/app/<path:path>')
def send_js(path):
    return send_from_directory('pages', path)


@app.route('/ping', methods=['GET'])
def ping():
    return("ping!")


@app.route('/wait', methods=['GET'])
def wait():
    q = Queue(connection=conn)
    job = q.enqueue(test(), 'http://heroku.com')

    if job.is_finished:
        return job.result
    else:
        return "Nay!"


job_id = 0


@app.route('/start', methods=['POST'])
def start():
    q = Queue(connection=conn)
    job = q.enqueue(test(), 'http://heroku.com')


@app.route('/check', methods=['GET'])
def check():
    q = Queue(connection=conn)
    job = q.fetch_job(12)

    if job.is_finished:
        return job.result
    else:
        return "Nay!"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
