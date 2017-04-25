class AlexaAudioQueue(object):

    def __init__(self, urls, loop=False, shuffle=False, history_len=30):
		self._urls = urls
		self._queued = collections.deque(urls)
		self._loop_queue = None
		self._history = collections.deque(maxlen=history_len)
		self._current = None
		self._loop = loop
		self._shuffle = shuffle
        
    def status(self):
        """
        Status of the queue
        """
		status = {
			'Current Position': self.current_position,
			'Current URL': self.current,
			'Next URL': self.up_next,
			'Previous': self.previous,
			'History': list(self.history),
			'Loop': self.loop,
			'Shuffle': self.shuffle
		}
		return status   
    
    def start(self):
        """
        Starts the queue and returns the first track.
        """
        return self.next()
    
    def next(self):
        """
        Immediatly ends the current track, moves the queue to the next track and returns that track.
        """
   		self.end_current()
		next_track = self._get_next()
		print("Next {} Loop {}")
		if next_track is None and self.loop is True:
			next_track = self._get_next_if_loop()
		self._current = next_track
		return self._current

    def previous(self):
        """
        Immediatly ends the current track, moves the queue to the previous track and returns that track.
        """
        pass()
    
    def up_next(self):
        """
        Gets the next song in the queue. Note: This doesn't advance us to the
        next track it only allows us to see what the next song will be.
        """
		next_track = self._peek_next()
		if next_track is None:
			next_track = self._peek_next_if_loop()
		return next_track
    
	def _peek_next(self):
		qcopy = self._queued.copy()
		try:
			return qcopy.popleft()
		except IndexError:
			return None
    
    def shuffle(self, value):
        """
        queue.shuffle(True) turns on shuffling for this queue. All tracks that havn't been played will now
        be shuffled the current playing track is not affected.
        
        queue.shuffle(False) turns off shuffling - this will now play all songs in order from the current
        song in their original order (even if already played).
        """
        pass()
        
    def loop(self):
        """
        queue.loop(True) will turn on looping so that when this queue finishes it will loop around again. 
        If shuffle is also on the songs will be shuffled again when looping. Note this could mean you get
        the same song twice in a row.
        queue.loop(False) turns off looping and the queue will stop once the last track is played. If we have already
        looped at least once we will continue until the end of the queue.
        """
        pass()
    
    
    
	def _peek_next(self):
		qcopy = self._queued.copy()
		try:
			return qcopy.popleft()
		except IndexError:
			return None
	
	def _peek_next_from_loop_queue(self):
		qcopy = self._loop_queue.copy()
		try:
			return qcopy.popleft()
		except IndexError:
			return None
	
	def _peek_next_if_loop(self):
		next_track = None
		if self.loop is True:
			if self._loop_queue is None:
				self._create_loop_queue()
			next_track = self._peek_next_from_loop_queue()
		return next_track

	def _get_next_if_loop(self):
		next_track = None
		if self.loop is True:
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
		if self.loop is True:
			q = collections.deque(self._urls)
			if self.shuffle is True:
				print("shuffle")
				shuffle(q)
			self._loop_queue = q			
    
