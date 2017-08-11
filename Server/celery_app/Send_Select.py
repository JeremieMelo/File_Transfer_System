#-*- encoding=UTF-8 -*-

from socket import *
import struct
import os
from celery import Celery
from celery_app import app
@app.task
def Sendall(fd, data):
    connection = fromfd(fd)
    connection.sendall(send_stream)
