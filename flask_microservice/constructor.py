from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from config import config
from engineio.payload import Payload

# Configure app
secret = config()
app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.config['SECRET_KEY'] = secret
app.use_reloader=False
async_mode = None
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
Payload.max_decode_packets = 16