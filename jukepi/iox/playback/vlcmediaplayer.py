import logging

import vlc

import jukepi.iox.playback.mediaplayer as mp
import jukepi.iox.playlist as pl

logger = logging.getLogger(__name__)


def song_finished(event):
    logger.info(event)
    VlcMediaPlayer.instance.current_index += 1
    logger.debug('Song finished')


class VlcMediaPlayer(mp.MediaPlayer):
    """
    Singleton
    https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaListPlayer-class.html
    """
    instance = None
    
    class __VlcMediaPlayer:
        def __init__(self):
            vlc_instance = vlc.Instance()
            
            # Create a MediaPlayer with the default instance
            self.player = vlc_instance.media_player_new()
            self.playlist = None
            self.mlplayer = vlc.MediaListPlayer()
            self.mlplayer.set_media_player(self.player)
            
            self.current_index = 0
    
    def __init__(self):
        super(VlcMediaPlayer, self).__init__()
        if not self.instance:
            VlcMediaPlayer.instance = VlcMediaPlayer.__VlcMediaPlayer()
    
    def __getattr__(self, name):
        return getattr(self.instance, name)
    
    def enqueue_track(self, track):
        media_list = vlc.MediaList(track.uri)
        VlcMediaPlayer.player.set_media_list(media_list)
    
    def enqueue(self, tracks):
        pass
    
    def play(self, playlist: pl.Playlist = None):
        if not playlist:
            return

        VlcMediaPlayer.instance.mlplayer.stop()
        VlcMediaPlayer.instance.current_index = 0
        
        VlcMediaPlayer.instance.playlist = playlist

        uris = VlcMediaPlayer.instance.playlist.get_song_uris()
        
        media_list = vlc.MediaList(uris)
        VlcMediaPlayer.instance.mlplayer.set_media_list(media_list)
        VlcMediaPlayer.instance.mlplayer.current_song = media_list[0]
        
        # https://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.EventType-class.html
        event_manager = VlcMediaPlayer.instance.mlplayer.event_manager()
        event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, song_finished)
        
        VlcMediaPlayer.instance.mlplayer.play()
    
    def pause(self):
        """ Toggle pause (or resume) media list. """
        VlcMediaPlayer.instance.mlplayer.pause()
    
    def stop(self):
        VlcMediaPlayer.instance.mlplayer.stop()
    
    def next(self):
        VlcMediaPlayer.instance.mlplayer.next()
    
    def prev(self):
        VlcMediaPlayer.instance.mlplayer.previous()
    
    def get_now_playing_id(self):
        if not VlcMediaPlayer.instance.playlist:
            return None
        return VlcMediaPlayer.instance.playlist.get_song(VlcMediaPlayer.instance.current_index - 1).id
    
    def get_queue(self) -> pl.Playlist:
        return VlcMediaPlayer.instance.playlist
