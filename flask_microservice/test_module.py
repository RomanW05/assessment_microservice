import warnings
from app import *
from .tests.test_always_pass import *
import multiprocessing
import requests
import websockets
import asyncio


flask_test_client = app.test_client()

def test_http():
    # log the user in through Flask test client
    # log in via HTTP
    r = flask_test_client.get('/')
    assert r.status_code == 200

def test_socket():
    # log the user in through Flask test client
    # log in via socket
    r = flask_test_client.get('ws:localhost:8000')
    # assert r.status_code == 200



import websocket
def test_socket_111():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000")
    # ws.send("Hello, Server")
    print(ws.recv())
    # ws.getstatus()
    
    assert ws.recv() == 1, ws.getstatus()