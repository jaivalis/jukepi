import vlc
import abc
from PyJukePi.io.playlist import Playlist


class MediaPlayer(metaclass=abc.ABCMeta):

    def __init__(self, playlist):
        self.playlist = playlist
        
    @abc.abstractmethod
    def enqueue(self, track):
        pass
    
    @abc.abstractmethod
    def play(self, playlist=None):
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
    
    def get_currently_playing_track(self):
        pass
    
    
class VlcMediaPlayer(MediaPlayer):
    """
    Singleton
    https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaListPlayer-class.html
    """
    instance = None
    
    class __VlcMediaPlayer:
        def __init__(self, playlist):
            
            instance = vlc.Instance()
    
            # Create a MediaPlayer with the default instance
            self.player = instance.media_player_new()
    
            self.mlplayer = vlc.MediaListPlayer()
            self.mlplayer.set_media_player(self.player)
    
    def __init__(self, playlist):
        super(VlcMediaPlayer, self).__init__(playlist)
        if not VlcMediaPlayer.instance:
            VlcMediaPlayer.instance = VlcMediaPlayer.__VlcMediaPlayer(playlist)
        else:
            VlcMediaPlayer.instance.playlist = playlist
            
    def __getattr__(self, name):
        return getattr(self.instance, name)
    
    def enqueue_track(self, track):
        media_list = vlc.MediaList(track.uri)
        self.player.set_media_list(media_list)
        pass
    
    def enqueue(self, tracks):
        pass
    
    def play(self, playlist=None):
        self.mlplayer.stop()
        
        if playlist:
            self.playlist = playlist
        
        assert isinstance(self.playlist, Playlist)
        
        uris = self.playlist.get_song_uris()

        media_list = vlc.MediaList(uris)
        self.mlplayer.set_media_list(media_list)
        self.mlplayer.current_song = media_list[0]

        self.mlplayer.play()
            
    def pause(self):
        self.mlplayer.pause()

    def stop(self):
        self.mlplayer.stop()

    def next(self):
        self.mlplayer.next()

    def prev(self):
        self.mlplayer.previous()




