import logging

import playback.mediaplayer as mp

logger = logging.getLogger(__name__)


class MockMediaPlayer(mp.MediaPlayer):

    def __init__(self):
        pass
    
    def enqueue(self, track):
        pass
    
    def play(self, playlist):
        logger.info('Playing from %s', playlist)
        self.playlist = playlist
        return True
    
    def pause(self):
        pass
    
    def stop(self):
        pass
    
    def next(self):
        pass
    
    def prev(self):
        pass
    
    def get_now_playing_id(self):
        pass
    
    def get_queue(self):
        return self.playlist
    
    def song_finished(self, event):
        pass
