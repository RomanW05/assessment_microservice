from gevent.pywsgi import WSGIServer
from app import create_app

app = create_app()
http_server = WSGIServer(("0.0.0.0", 8001), app)
http_server.serve_forever()