class Playlist(object):
    
    def __init__(self, tracks):
        self.tracks = tracks
        self.index = 0
    
    def enqueue(self, track):
        self.tracks.append(track)
    
    def remove(self, track):
        # TODO remove removes the first matching value, not a specific index
        # del removes the item at a specific index:
        self.tracks.remove(track)
    
    def move_up(self, track):
        pass
    
    def move_down(self, track):
        pass

    def get_song_uris(self):
        return [track.uri for track in self.tracks]
    
    def get_song(self, index):
        return self.tracks[index]
