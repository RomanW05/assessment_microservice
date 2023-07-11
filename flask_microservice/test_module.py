from .tests.test_always_pass import *
import websocket
import json


# Declare socket
ws = websocket.WebSocket()


def test_socket_headers():
    ws.connect("ws://localhost:8000")
    r = json.dumps(ws.getheaders())
    headers_dictionary = json.loads(r)
    assert headers_dictionary["upgrade"] == 'websocket', ws.getheaders()
    assert ws.connected == True, 'Not connected even thou headers show "upgrade":"websocket"'
    assert ws.getstatus() == 101, ws.getstatus()
    ws.close()


def test_socket_connection():
    ws.connect("ws://localhost:8000")
    assert ws.connected == True
    ws.close()
    ws.getstatus()
    assert ws.connected == False


def test_socket_data():
    ws.connect("ws://localhost:8000")
    assert ws.connected == True
    
    result = ws.recv()
    print(result)
    # emit('message', {'count': price, 'data': 'message sent'}, broadcast=True, namespace='')
    assert 1 == 2, result