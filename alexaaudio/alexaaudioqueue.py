import collections
from random import shuffle as shuffler


class AlexaAudioQueue(object):

    def __init__(self, urls, loop_tracks=False, shuffle_tracks=False, history_len=30):
        self._urls = urls
        self._queued = collections.deque(urls)
        self._loop_queue = None
        self._history = collections.deque(maxlen=history_len)
        self._current = None
        self._loop_tracks = loop_tracks
        self._shuffle_tracks = shuffle_tracks
        
    def status(self):
        """
        Status of the queue
        """
        status = {
            'Current URL': self.current,
            'Next URL': self.up_next(),
            'History': list(self.history),
            'Loop': self._loop_tracks,
            'Shuffle': self._shuffle_tracks
        }
        return status
    
    def start(self):
        """
        Starts the queue and returns the first track.
        """
        return self.next()
    
    def next(self):
        """
        Immediately ends the current track, moves the queue to the next track and returns that track.
        """
        self.stop()
        next_track = self._get_next()
        if next_track is None and self._loop_tracks is True:
            next_track = self._get_next_if_loop()
        self._current = next_track
        return self._current

    def previous(self):
        """
        Immediately ends the current track, moves the queue to the previous track and returns that track.
        """
        history = self.history.copy()
        try:
            return history.pop()
        except IndexError:
            return None

    def stop(self):
        self._save_to_history()
        self._current = None

    def up_next(self):
        """
        Gets the next song in the queue. Note: This doesn't advance us to the
        next track it only allows us to see what the next song will be.
        """
        next_track = self._peek_next()
        if next_track is None:
            next_track = self._peek_next_if_loop()
        return next_track
    
    def loop(self, value):
        """
        queue.loop(True) will turn on looping so that when this queue finishes it will loop around again. 
        If shuffle is also on the songs will be shuffled again when looping. Note this could mean you get
        the same song twice in a row.
        queue.loop(False) turns off looping and the queue will stop once the last track is played. If we have already
        looped at least once we will continue until the end of the queue.
        """
        self._loop_tracks = value

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, url):
        self._save_to_history()
        self._current = url

    @property
    def shuffle(self):
        return self._shuffle_tracks

    @shuffle.setter
    def shuffle(self, value):
        """
        queue.shuffle(True) turns on shuffling for this queue. All tracks that havn't been played will now
        be shuffled the current playing track is not affected.

        queue.shuffle(False) turns off shuffling - this will now play all songs in order from the current
        song in their original order (even if already played).
        """

        if value is self._shuffle_tracks:
            return
        self._shuffle_tracks = value
        if value:
            q = collections.deque(self._urls)
            shuffler(q)
            self._queued = q
        else:
            # find current in urls
            i = self._urls.index(self.current)
            # set queue to all songs after current
            remaining_urls = self._urls[i + 1:]
            q = collections.deque(remaining_urls)

    @property
    def history(self):
        return self._history

    def _peek_next(self):
        queue_copy = self._queued.copy()
        try:
            return queue_copy.popleft()
        except IndexError:
            return None

    def _peek_next_from_loop_queue(self):
        queue_copy = self._loop_queue.copy()
        try:
            return queue_copy.popleft()
        except IndexError:
            return None

    def _peek_next_if_loop(self):
        next_track = None
        if self._loop_tracks is True:
            if self._loop_queue is None:
                self._create_loop_queue()
            next_track = self._peek_next_from_loop_queue()
        return next_track

    def _get_next_if_loop(self):
        next_track = None
        if self._loop_tracks is True:
            if self._loop_queue is None:
                self._create_loop_queue()
            next_track = self._get_next_from_loop_queue()
            self._queued = self._loop_queue
            self._loop_queue = None
        return next_track

    def _get_next(self):
        try:
            return self._queued.popleft()
        except IndexError:
            return None

    def _get_next_from_loop_queue(self):
        try:
            return self._loop_queue.popleft()
        except IndexError:
            return None

    def _create_loop_queue(self):
        if self._loop_tracks is True:
            q = collections.deque(self._urls)
            if self._shuffle_tracks is True:
                shuffler(q)
            self._loop_queue = q

    def add(self, url):
        self._urls.append(url)
        self._queued.append(url)

    def extend(self, urls):
        self._urls.extend(urls)
        self._queued.extend(urls)

    def _save_to_history(self):
        if self._current:
            self._history.append(self._current)


