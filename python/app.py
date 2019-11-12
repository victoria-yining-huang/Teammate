from flask import Flask
from model import ping
app = Flask(__name__)


@app.route('/')
def hello():
    ping()
    return "Hello World!"


if __name__ == '__main__':
    app.run()
