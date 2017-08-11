import time
from celery import Celery
from celery_app import app
@app.task
def add(x, y):
    print(x+y)
    return x + y
