import web_app
import threading
import time

def main():
    import web_app
    webapp_thread = threading.Thread(target=run_web_app)
    webapp_thread.start()
    # webapp_thread = threading.Thread(target=run_web_app, args=(i,))

    while web_app.connected==False:
        print ("waiting for client to connect")
        time.sleep(1)
        pass

    print ("Connected...")
    time.sleep(3)
    print ("Trying to print dummy message...")
    web_app.socket_onload("Dummy")

def run_web_app():
    web_app.socketio.run(web_app.app)

if __name__ == '__main__':
    main()