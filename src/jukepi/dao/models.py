from datetime import datetime, timedelta

from jukepi.dao import db


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), index=True)
    
    added_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    played_at = db.Column(db.DateTime)
    
    plays = db.Column(db.Integer)  # TODO turn to float ?
    
    albums = db.relationship('Album', lazy='subquery', back_populates='artist')
    
    lastfm_url = db.Column(db.String(255))
    # TODO pic_uri = db.Column(db.String(255), index=True, unique=True)


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    title = db.Column(db.String(255))
    year = db.Column(db.Integer)

    artist_id = db.Column(db.String(255), db.ForeignKey(Artist.id))
    artist = db.relationship('Artist', lazy='subquery', back_populates='albums', uselist=False)

    tracks = db.relationship('Track', lazy='subquery', back_populates='album')
    
    added_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    played_at = db.Column(db.DateTime)
    
    cover_art_id = db.Column(db.Integer)
    cover_art = db.relationship('CoverArt', uselist=False)

    lastfm_url = db.Column(db.String(255))
    
    def get_album_tracks(self) -> list:
        """ Returns the album tracks sorted by track_num """
        return sorted(self.tracks, key=lambda x: x.track_num, reverse=False)
    
    def duration_str(self) -> str:
        duration = 0
        for track in self.tracks:
            duration += track.duration
        return str(timedelta(seconds=duration))
    
    def genre_str(self) -> str:
        genres = set()
        for track in self.tracks:
            genres.add(track.genre)
        return ','.join(genres)
    
    def __str__(self) -> str:
        return self.title + ' by ' + self.artist.name


class Track(db.Model):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    title = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    uri = db.Column(db.String(255), index=True, unique=True)
    duration = db.Column(db.Integer)
    track_num = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    format = db.Column(db.String(5))
    bit_rate = db.Column(db.Integer)
    year = db.Column(db.Integer)
    plays = db.Column(db.Integer, default=0)

    last_modified = db.Column(db.DateTime)

    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artist = db.relationship('Artist', lazy='subquery', uselist=False)

    album_id = db.Column(db.Integer, db.ForeignKey(Album.id))
    album = db.relationship('Album', lazy='subquery', uselist=False)

    def duration_str(self) -> str:
        time = datetime(1, 1, 1) + timedelta(seconds=self.duration)
        return format(time.minute, "02d") + ":" + format(time.second, "02d")
    
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def __cmp__(self, other):
        return self.track_num < other.track_num
    

class CoverArt(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, index=True)
    uri = db.Column(db.String(255), index=True, unique=True)
    
    album_id = db.Column(db.Integer, db.ForeignKey(Album.id))
    album = db.relationship(Album, uselist=False)
