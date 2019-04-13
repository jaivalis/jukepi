import mutagen

METADATA_TRACK_TITLE = 'TIT2'


TITLE_KEY = 'title'
ALBUM_KEY = 'album'
GENRE_KEY = 'genre'
YEAR_KEY = 'year'
TRACK_NUM_KEY = 'track.num'
ARTIST_KEY = 'artist'
FILE_PATH_KEY = 'file.path'
DURATION_KEY = 'duration'
BITRATE_KEY = 'bitrate'


def extract_metadata(uri: str) -> dict:
    f = mutagen.File(uri)

    return {TITLE_KEY: str(f.tags[METADATA_TRACK_TITLE]),
            ALBUM_KEY: str(f.tags['TALB']),
            GENRE_KEY: str(f.tags['TCON']),
            YEAR_KEY: int(str(f.tags['TDRC'])),
            TRACK_NUM_KEY: str(f.tags['TRCK']),
            ARTIST_KEY: str(f['TPE1']),
            FILE_PATH_KEY: f.filename,
            DURATION_KEY: f.info.length,
            BITRATE_KEY: f.info.bitrate / 1000
            }
