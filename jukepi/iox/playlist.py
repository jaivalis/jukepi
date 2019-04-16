from jukepi.db.models import Track


class Playlist(object):
    
    def __init__(self, tracks):
        self.tracks = tracks
        self.index = 0
    
    def enqueue(self, track) -> None:
        self.tracks.append(track)
    
    def remove(self, track) -> None:
        # TODO remove removes the first matching value, not a specific index
        # del removes the item at a specific index:
        self.tracks.remove(track)
    
    def move_up(self, track) -> None:
        pass
    
    def move_down(self, track) -> None:
        pass

    def get_song_uris(self) -> list:
        return [track.uri for track in self.tracks]
    
    def get_song(self, index) -> Track:
        return self.tracks[index]
