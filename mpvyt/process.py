import os
import threading
import time


class MpvProcessObserver(threading.Thread):
    """
    Emit an event when mpv process appears or disappears. Searches for
    processes that have the --input-ipc-server set to sockpath, which allow us
    to be sure that it is the right mpv process.
    """
    def __init__(self, sockpath, handler):
        threading.Thread.__init__(self)
        self.path = sockpath
        self.pid = None
        self.handler = handler

    def search(self):
        needle = '--input-ipc-server={}'.format(self.path)
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            try:
                with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as f:
                    cmdline = f.read().split(b'\x00')
                    if any(c.decode() == needle for c in cmdline):
                        return pid
            except Exception:
                pass
        return False

    def run(self):
        while True:
            self.pid = self.search()
            if self.handler:
                self.handler(self.pid)
                time.sleep(1)
