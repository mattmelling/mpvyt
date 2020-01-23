import os

from mpvyt.process import MpvProcessObserver
from mpvyt.observer import MpvObserverThread
from mpvyt.title import TitleLookup


SOCK_PATH = os.environ['MPV_SOCKET_PATH'] \
    if 'MPV_SOCKET_PATH' in os.environ \
       else os.path.join(os.environ['HOME'], '.mpvsocket')
PLAYLIST_PATH = os.environ['MPV_PLAYLIST_PATH'] \
    if 'MPV_PLAYLIST_PATH' in os.environ \
       else os.path.join(os.environ['HOME'], '.mpvplaylist')


class MpvMonitor:
    def __init__(self):
        self.meta_observer = None
        self.process_observer = None
        self.current = None
        self._percent = 0
        self._playlist = []
        self.title_lookup = TitleLookup()

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

    def write_item(self, f, p):
        title = self.title_lookup.lookup(p['filename'])
        if title:
            f.write('# {}\n'.format(title))
            f.write('{}\n'.format(p['filename']))

    def write_playlist(self):
        seen_current = False
        with open(PLAYLIST_PATH, 'w') as f:
            # This is to force mpv to read the playlist as m3u, which allows us
            # to use comments - this is not supported in plaintext playlists.
            f.write('#EXTM3U\n')
            for p in self._playlist:
                if seen_current:
                    self.write_item(f, p)
                if 'current' in p and p['current']:
                    seen_current = True
                    self.write_item(f, p)

    def start(self):
        self.process_observer = MpvProcessObserver(SOCK_PATH,
                                                   self.process_handler)
        self.process_observer.run()


def main():
    o = MpvMonitor()
    o.start()


if __name__ == '__main__':
    main()
