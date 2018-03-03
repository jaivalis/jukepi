import os
from datetime import datetime
from pprint import pprint

from hsaudiotag import auto
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from ..dao import Album, Artist, Track, CoverArt
from ..io.libraryhandler import filtered_crawler, get_artwork


# # <editor-fold desc="init">
# DB_URI = 'sqlite:///library.db'
# engine = create_engine(DB_URI)
#
# Base = declarative_base()
# Base.metadata.bind = engine
#
# Base.metadata.drop_all()
# Base.metadata.create_all(checkfirst=True)
# # if not engine.dialect.has_table(engine, HoursTalents.__tablename__):
# #     print('Couldn\'t find tables, creating new where necessary.')
# #     Base.metadata.create_all(checkfirst=True)
# # else:
# #     print('Existing database found.')
#
# # debug
# engine.echo = True
#
# engine.encoding = 'UTF-8'
#
# # Connect to the database
# connection = engine.connect()
#
# # Begin a non-ORM transaction
# trans = connection.begin()
#
# # Bind an individual Session to the connection
# # autocommit=False, autoflush=False
# db_session = scoped_session(sessionmaker(bind=engine, autoflush=False))
# session = db_session()
# # </editor-fold>

# app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jaivalis/workspace/PycharmProjects/PyJukePi/library.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/jaivalis/workspace/PycharmProjects/PyJukePi/library.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
# session = session
# session.create_all()

# db.create_all()
# db.metadata.create_all(db.engine)


def init_db():
    pass
    

def persist_library(session_, rebuild):
    if rebuild:
        session_.commit()
        session_.flush()
            
    for uri, last_modified in filtered_crawler():
        existing = get_track(session_, uri)
        if existing and existing.last_modified.timestamp() <= last_modified:
            continue

        metadata = auto.File(uri)

        existing_artist = get_artist(session_, metadata.artist)
        if not existing_artist:
            existing_artist = Artist(name=metadata.artist)
            session_.add(existing_artist)
            session_.flush()

        existing_album = get_album(session_, metadata.album, existing_artist.id)
        if not existing_album:
            
            existing_album = Album(title=metadata.album,
                                   year=metadata.year,
                                   artist_id=existing_artist.id,
                                   artist=existing_artist)
            session_.add(existing_album)
            session_.flush()
            
            art_uri = uri[0:uri.rfind(os.sep)]
            cover_art = handle_cover_art_add(session_, art_uri, existing_album, flush=True)
            existing_album.cover_art = cover_art
            existing_album.cover_art_id = cover_art.id

        if existing:
            session_.query(Track).filter(Track.id == existing.id).delete()

        track = Track(title=metadata.title,
                      genre=metadata.genre,
                      uri=uri,
                      duration=metadata.duration,
                      track_num=metadata.track,
                      format=os.path.splitext(uri)[1],
                      bit_rate=metadata.bitrate,
                      year=metadata.year,
                      
                      last_modified=datetime.fromtimestamp(last_modified),

                      artist_id=existing_artist.id,
                      artist=existing_artist,
                      album_id=existing_album.id,
                      album=existing_album)
        pprint(track)
        session_.add(track)
    session_.commit()


def handle_cover_art_add(session_, uri, album, flush=False):
    """
    Adds an CoverArt entity or fetches an existing one from the db.
    :param session_:
    :param uri:
    :param album:
    :param flush:
    :return:
    """
    existing = get_artwork(session_, uri)
    if not existing:
        existing = CoverArt(uri=uri, album_id=album.id, album=album)
        session_.add(existing)
        if flush:
            session_.flush()
    return existing
    

def get_track(session_, uri):
    """ Fetches track by uri.
    :param session_:
    :param uri:
    :return: :type: Track
    """
    return session_.query(Track).filter_by(uri=uri).first()


def get_artist(session_, name, case_sensitive=False):
    if not case_sensitive:
        return session_.query(Artist).filter(Artist.name.ilike(name)).first()
    return session_.query(Artist).filter_by(name=name).first()


def get_album(session_, title, artist_id):
    return session_.query(Album).filter_by(title=title, artist_id=artist_id).first()


def get_artwork(session_, uri):
    """ Fetches cover art by uri.
    :param session_:
    :param uri:
    :return: :type: Track
    """
    return session_.query(CoverArt).filter_by(uri=uri).first()


def get_recently_played_albums(session_, limit):
    return session_.query(Album).order_by(desc(Album.played_at)).limit(limit).all()


def get_recently_added_albums(session_, limit):
    return session_.query(Album).order_by(desc(Album.added_at)).limit(limit).all()


# <editor-fold desc="Searches">
def search_artists(session_, name):
    return session_.query(Artist).filter(Artist.name.ilike('%{}%'.format(name))).all()


def search_albums(session_, title):
    return session_.query(Album).filter(Album.title.ilike('%{}%'.format(title))).all()


def search_tracks(session_, title):
    return session_.query(Track).filter(Track.title.ilike('%{}%'.format(title))).all()
# </editor-fold>


# <editor-fold desc="Artist Page">
def get_artist_discography(session_, name):
    artist = get_artist(session_, name, case_sensitive=False)
    if not artist:
        return None
    return session_.query(Album).filter(Album.artist_id == artist.id).all()
# </editor-fold>


# <editor-fold desc="Album Page">
def get_album_by_str(session_, artist_name, title, case_sensitive=False):
    artist = get_artist(session_, artist_name, case_sensitive)
    if not artist:
        return None
    
    # album = get_album(session_, title, artist.id)
    # if not album:
    #     return None
    
    for album in artist.albums:
        if album.title.lower() == title.lower():
            return album
    return None
# </editor-fold>


# <editor-fold desc="Session management">
def handle_transaction_commit(session_, entries_processed, entries_total, entry_type_str=''):
    try:
        session_.commit()
        session_.flush()
        print('[Done] Imported {} of {} {} entries.'.format(entries_processed, entries_total, entry_type_str))
        return True
    except SQLAlchemyError as e:
        print('[Failed, rolling back]. Cause:\n\t{}'.format(str(e)))
        session_.rollback()
        return False
    
    
def __enter__(self):
    return self


# def __exit__(exc_type, exc_val, exc_tb):
#     session_.commit()
#     connection.close()
# </editor-fold>


