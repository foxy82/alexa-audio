class AlexaAudioQueue(object):

    def __init__(self, urls):
        self._urls = urls
        
    def status(self):
        pass()
    
    def start(self):
        """
        Starts the queue and returns the first track.
        """
        pass()
    
    def next(self):
        """
        Immediatly ends the current track, moves the queue to the next track and returns that track.
        """
        pass()

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
        pass()

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
