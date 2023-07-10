import warnings
from app import *

from tests.test_always_pass import *
from flask_socketio import SocketIO
from socketIO_client import SocketIO, LoggingNamespace
import asyncio
import websockets
from pywsitest import WSTest, WSResponse




# socket_client = socketio.test_client(app)
flask_test_client = app.test_client()

    

def test_http():
    # log the user in through Flask test client
    # log in via HTTP
    r = flask_test_client.get('/')
    assert r.status_code == 200


# def test_url(url, data=""):
#     async def inner():
#         async with websockets.connect(url) as websocket:
#             await websocket.send(data)
#     return asyncio.get_event_loop().run_until_complete(inner())

# test_url("ws://127.0.0.1:8000")

# async def test_socket():
#     ws_test = (WSTest("wss://localhost:8000").with_response(WSResponse().with_attribute("body")))
#     await ws_test.run()

#     assert ws_test.is_complete()

import asyncio
from websockets.sync.client import connect

def hello():
    with app.app_context():
        with connect("ws://localhost:8000") as websocket:
            websocket.send("Hello world!")
            message = websocket.recv()
            print(f"Received: {message}")

backround_task_manager()
print('starting server')
socketio.run(app, port=8000)

hello()
