import websocket
import json
from app import *
import json
import unittest
ws = websocket.WebSocket()

class _Test_dashboard(Dashboard):
    def on_raise_error(self):
        raise AssertionError()

# _dashboard_namespace = socketio.on_namespace(Dashboard(namespace="/test_dashboard"))
socketio.on_namespace(_Test_dashboard(namespace="/test_dashboard"))

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


def test_namespace():
    ws.connect("ws://localhost:8000/dashboard")
    assert ws.connected == True


class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):
        client = socketio.test_client(app)
        self.assertNotEqual(client.eio_sid, None)
        client2 = socketio.test_client(app)
        self.assertTrue(client.is_connected())
        self.assertTrue(client2.is_connected())
        self.assertNotEqual(client.eio_sid, client2.eio_sid)


    def test_connect_namespace(self):
        client = socketio.test_client(app, namespace='/dashboard')
        self.assertTrue(client.is_connected('/dashboard'))
        received = client.get_received('/dashboard')
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'Connected')
        client.disconnect(namespace='/dashboard')
        self.assertFalse(client.is_connected('/dashboard'))


    def test_disconnect_namespace(self):
        client = socketio.test_client(app, namespace='/dashboard')
        client.disconnect('/dashboard')
        self.assertEqual(client.is_connected(), False)


    def test_connect_class_based(self):
        client = socketio.test_client(app, namespace='/dashboard')
        received = client.get_received('/dashboard')
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'Connected')
        client.disconnect('/dashboard')

    def test_connect_class_based_query_string_and_headers(self):
        client = socketio.test_client(
            app, namespace='/dashboard', query_string='foo=bar',
            headers={'Authorization': 'Basic foobar'})
        received = client.get_received('/dashboard')
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'Connected')
        client.disconnect('/dashboard')

    def test_disconnect_class_based(self):
        global disconnected
        disconnected = None
        client = socketio.test_client(app, namespace='/dashboard')
        client.disconnect('/dashboard')
        
        self.assertEqual(client.is_connected('/dashboard'), False)

    def test_send_class_based(self):
        client = socketio.test_client(app, namespace='/dashboard')
        received = client.get_received('/dashboard')
        self.assertEqual(received[0]['args'], 'Connected')
        client.emit('hala', namespace='/dashboard')
        received = client.get_received('/dashboard')
        self.assertEqual(received[0]['args'], 'HALA')


    def test_server_disconnected(self):
        client = socketio.test_client(app, namespace='/dashboard')
        client2 = socketio.test_client(app, namespace='/dashboard')
        client.get_received('/dashboard')
        client2.get_received('/dashboard')
        client.disconnect('/dashboard')
        # client.emit('exit', {}, namespace='/dashboard')
        self.assertFalse(client.is_connected('/dashboard'))
        self.assertTrue(client2.is_connected('/dashboard'))
        with self.assertRaises(RuntimeError):
            client.emit('hello', {}, namespace='/dashboard')
        # client2.emit('exit', {}, namespace='/dashboard')
        client2.disconnect('/dashboard')
        self.assertFalse(client2.is_connected('/dashboard'))
        with self.assertRaises(RuntimeError):
            client2.emit('hello', {}, namespace='/dashboard')



if __name__ == '__main__':
    unittest.main()