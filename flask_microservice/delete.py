# import websocket
# import _thread
# import time
# import rel

# def on_message(ws, message):
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# def on_open(ws):
#     print("Opened connection")

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://localhost",
#                               on_open=on_open,
#                               on_message=on_message,
#                               on_error=on_error,
#                               on_close=on_close)

#     ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
#     rel.signal(2, rel.abort)  # Keyboard Interrupt
#     rel.dispatch()



import socket

s = socket.socket()         # Create a socket object
host = 'localhost' # Get local machine name
port = 8000                # Reserve a port for your service.

print ('Connecting to ', host, port)
s.connect((host, port))

while True:
#   msg = input('CLIENT >> ')
  s.send('msg')
  msg = s.recv(1024)
  print ('SERVER >> ', msg)