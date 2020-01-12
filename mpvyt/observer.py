import json
import socket
import threading
import time


class MpvObserverThread(threading.Thread):
    """
    Subscribes to observable properties within mpv and tracks their state.
    """
    def __init__(self, path):
        threading.Thread.__init__(self)
        self._stop = False
        self.path = path
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.observers = {}
        self.observer_id = 1
        self.handler = None

    def event_handler(self, h):
        self.handler = h

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            try:
                self.socket.connect(self.path)
                while not self._stop:
                    try:
                        buf = self.socket.recv(4096).decode()
                        for msg in buf.split('\n'):
                            try:
                                msg = json.loads(msg)
                                self.dispatch(msg)
                            except json.decoder.JSONDecodeError:
                                pass
                    except BlockingIOError:
                        time.sleep(0.1)
            except ConnectionRefusedError:
                # This comes from the connect() call
                time.sleep(3)

    def send(self, mesg):
        self.socket.sendall((json.dumps(mesg) + '\n').encode())

    def dispatch(self, msg):
        if 'event' in msg:
            if msg['event'] == 'property-change':
                if msg['name'] in self.observers:
                    self.observers[msg['name']](msg['data'])
            if msg['event'] == 'seek' or msg['event'] == 'pause':
                self.handler(msg)

    def observe(self, prop, f):
        self.observers[prop] = f
        self.send({
            "command": ["observe_property", self.observer_id, prop]
        })
        self.observer_id += 1
