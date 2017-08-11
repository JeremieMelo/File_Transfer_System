import time
from celery import Celery
from celery_app import app
@app.task
def multiply(x, y):
    time.sleep(3)
    return x * y
