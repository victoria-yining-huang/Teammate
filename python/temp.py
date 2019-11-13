from model import wait
from rq import Queue
from worker import conn


def start():
    q = Queue(connection=conn)
    result = q.enqueue(wait, 'http://heroku.com')
    return(result)


start()
