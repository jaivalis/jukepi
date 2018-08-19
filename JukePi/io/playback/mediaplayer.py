import abc

import logging

from JukePi.io.playlist import Playlist

logger = logging.getLogger(__name__)


class MediaPlayer(metaclass=abc.ABCMeta):
    
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def enqueue(self, track):
        pass
    
    @abc.abstractmethod
    def play(self, playlist: Playlist = None):
        pass
    
    @abc.abstractmethod
    def pause(self):
        pass
    
    @abc.abstractmethod
    def stop(self):
        pass
    
    @abc.abstractmethod
    def next(self):
        pass
    
    @abc.abstractmethod
    def prev(self):
        pass
    
    def get_now_playing_id(self):
        pass
    
    def get_queue(self):
        pass
    
    def song_finished(self, event):
        pass
