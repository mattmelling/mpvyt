import os

from mpvyt.process import MpvProcessObserver
from mpvyt.observer import MpvObserverThread


SOCK_PATH = os.environ['MPV_SOCKET_PATH'] \
    if 'MPV_SOCKET_PATH' in os.environ \
       else '/home/matt/.mpvsocket'
PLAYLIST_PATH = os.environ['MPV_PLAYLIST_PATH'] \
    if 'MPV_PLAYLIST_PATH' in os.environ \
       else '/home/matt/.mpvplaylist'


class MpvMonitor:
    def __init__(self):
        self.meta_observer = None
        self.process_observer = None
        self.current = None
        self._percent = 0
        self._playlist = []

    def process_handler(self, pid):
        if pid is not False and self.meta_observer is None:
            self.meta_observer = MpvObserverThread(SOCK_PATH)
            self.meta_observer.start()
            self.meta_observer.observe('playlist', self.playlist)
            self.meta_observer.observe('path', self.path)
            self.meta_observer.observe('percent-pos', self.percent)
            self.meta_observer.event_handler(self.event)
        elif self.meta_observer is not None and pid is False:
            self.meta_observer.stop()
            self.meta_observer = None

    def event(self, data):
        self.write_playlist()

    def path(self, path):
        if path != self.current:
            self.current = path
            self.write_playlist()

    def playlist(self, playlist):
        self._playlist = playlist
        self.write_playlist()

    def percent(self, percent):
        self._percent = percent

    def write_playlist(self):
        seen_current = False
        with open(PLAYLIST_PATH, 'w') as f:
            def write_item(p):
                f.write(p['filename'] + '\n')
            for p in self._playlist:
                if seen_current:
                    write_item(p)
                if 'current' in p and p['current']:
                    seen_current = True
                    write_item(p)

    def start(self):
        self.process_observer = MpvProcessObserver(SOCK_PATH,
                                                   self.process_handler)
        self.process_observer.run()


def main():
    o = MpvMonitor()
    o.start()


if __name__ == '__main__':
    main()
