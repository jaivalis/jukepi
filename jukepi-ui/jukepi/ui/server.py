import os
import urllib.parse
from os.path import join

import requests
from flask import render_template, request
from flask_bootstrap import Bootstrap
from markupsafe import Markup
from werkzeug.exceptions import abort

import jukepi.configuration as config
import jukepi.db as db
import jukepi.db.dao as dao
import jukepi.iox.volumecontrol as vol
from jukepi import app
from jukepi.exceptions import EntityNotFoundException


def render_include_context(template_name_or_list, **context):
    """ Render including the standard context: now_playing panel, volume
    :param template_name_or_list: template file
    :param context: vararg
    :return: rendered template
    """
    now_playing = dao.get_track_by_id(db.db_session, get_now_playing_id())
    # play_queue =
    # template_resolved_path=os.path.join(CWD, 'jukepi', 'ui', 'static', 'templates', template_name_or_list)
    return render_template(template_name_or_list,
                           now_playing=now_playing,
                           volume=vol.get_volume(),
                           **context)
    
    
@app.route('/')
@app.route('/index')
def index():
    added = dao.get_recently_added_albums(db.db_session, 5)
    played = dao.get_recently_played_albums(db.db_session, 5)
    
    return render_include_context('index.html', recently_added_albums=added, recently_played_albums=played)


@app.route('/search')
def search():
    query = request.args.get('q', type=str)
    query = urllib.parse.unquote_plus(query)
    
    artists = dao.search_artists(db.db_session, query)
    albums = dao.search_albums(db.db_session, query)
    tracks = dao.search_tracks(db.db_session, query)
    
    title = 'Search Results' + query
    return render_include_context('search_results.html', title=title, artists=artists, albums=albums, tracks=tracks)


@app.route('/artist/<name>')
def artist(name: str):
    name = urllib.parse.unquote_plus(name)

    albums = dao.get_artist_discography(db.db_session, name)
    if not albums:
        abort(404, {'message': 'Oops, artist not found!'})
        
    return render_include_context('artist.html', artist=albums[0].artist, albums=albums)


@app.route('/album/<name>/<title>')
def album(name: str, title: str):
    name = urllib.parse.unquote_plus(name)
    title = urllib.parse.unquote_plus(title)
    
    try:
        album_ = dao.get_album_by_str(db.db_session, name, title)
        
        title = title
        return render_include_context('album.html', title=title, album=album_)
    except EntityNotFoundException:
        abort(404, {'message': 'Oops, album not found!'})


@app.route('/play/<track_id>')
def play_track(track_id: str):
    track_id = urllib.parse.unquote_plus(track_id)


@app.route('/playAlbum/<album_id>')
def play_album(album_id: str):
    album_id = urllib.parse.unquote_plus(album_id)
    
    try:
        album_ = dao.get_album_by_id(db.db_session, album_id)
        # get_player().play(Playlist(album_.get_album_tracks()))
        r = requests.post(config.rest_player_host + '/play', album_.get_album_tracks())
        return r.text, r.status_code
        
        # return 'Now playing ' + str(album_), 200, {'Content-Type': 'text/plain'}
    except EntityNotFoundException:
        abort(404, {'message': 'Oops, album not found!'})
    

@app.route('/playAlbumFromTrack/<album_id>/<track_id>')
def play_album_from_track(album_id, track_id):
    album_id = urllib.parse.unquote_plus(album_id)
    album_ = dao.get_album_by_id(db.db_session, album_id)
    if not album_:
        abort(404, {'message': 'Oops, album not found!'})
        
    track_id = urllib.parse.unquote_plus(track_id)
    track_ = dao.get_track_by_id(db.db_session, track_id)
    if not track_ or track_ not in  album_.tracks:
        abort(404, {'message': 'Oops, track not found!'})

    tracks = album_.get_album_tracks()
    # get_player().play(Playlist(tracks[tracks.index(track_):]))
    r = requests.post(config.rest_player_host + '/play', tracks[tracks.index(track_):])
    return r.text, r.status_code


@app.route('/pause')
def pause():
    # get_player().pause()
    r = requests.get(config.rest_player_host + '/pause')
    return r.text, r.status_code
    # return '', 200, {'Content-Type': 'text/plain'}


@app.route('/next')
def next():
    # get_player().next()
    r = requests.get(config.rest_player_host + '/fwd')
    return r.text, r.status_code
    # return '', 200, {'Content-Type': 'text/plain'}


@app.route('/prev')
def prev():
    # get_player().prev()
    r = requests.get(config.rest_player_host + '/bwd')
    return r.text, r.status_code
    # return '', 200, {'Content-Type': 'text/plain'}


@app.route('/setVolume')
def set_volume():
    volume = request.args.get('v', type=int)
    # vol.set_volume(volume)
    # return '', 200, {'Content-Type': 'text/plain'}
    r = requests.post(config.rest_player_host + '/setVolume')
    return r.text, r.status_code


@app.route('/getVolume')
def get_volume():
    return vol.get_volume(), 200, {'Content-Type': 'text/plain'}


def get_now_playing_id():
    r = requests.get(config.rest_player_host + '/queue')
    queue_list = r.json()['tracks']

    if not queue_list:
        return None

    enriched_track = queue_list[0]  # todo
    return enriched_track


@app.route('/queue')
def get_play_queue():
    # queue_list = get_player().get_queue()
    r = requests.get(config.rest_player_host + '/queue')
    queue_list = r.json()['tracks']

    if not queue_list:
        return 'Nothing playing right now.', 200, {'Content-Type': 'text/plain'}
    enriched_tracks = queue_list  # todo
    return render_template('playlist.html', playlist=enriched_tracks)
    
# </editor-fold>


# <editor-fold desc="Artist Overviews">
@app.route('/ArtistsAlpha')
def artists_alpha():
    """ Artists overview sorted alphabetically.
    :return:
    """
    artists = dao.get_artists_alpha(db.db_session)
    if not artists:
        abort(404, {'message': 'Oops, no artists found!'})

    return render_include_context('artists.html', artists=artists)


@app.route('/ArtistsRecentlyAdded')
def artists_by_added():
    """ Artists overview sorted by plays.
    :return:
    """
    artists = dao.get_artists_recent_added(db.db_session)
    if not artists:
        abort(404, {'message': 'Oops, no artists found!'})
    
    return render_include_context('artists.html', artists=artists)


@app.route('/ArtistsRecentlyPlayed')
def artists_by_plays():
    """ Artists overview sorted by plays.
    :return:
    """
    artists = dao.get_artists_recent_played(db.db_session)
    if not artists:
        abort(404, {'message': 'Oops, no artists found!'})
    
    return render_include_context('artists.html', artists=artists)
# </editor-fold>


# <editor-fold desc="Albums Overviews">
@app.route('/AlbumsAlpha')
def albums_by_alpha():
    """ Albums overview sorted alphabetically.
    :return:
    """
    albums = dao.get_albums_alpha(db.db_session)
    if not albums:
        abort(404, {'message': 'Oops, no artists found!'})
    
    return render_include_context('albums.html', albums=albums)


@app.route('/AlbumsRecentlyAdded')
def albums_by_plays():
    """ Albums overview sorted by plays.
    :return:
    """
    albums = dao.get_albums_recent_played(db.db_session)
    if not albums:
        abort(404, {'message': 'Oops, no artists found!'})
    
    return render_include_context('albums.html', albums=albums)


@app.route('/AlbumsRecentlyPlayed')
def albums_plays():
    """ Albums overview sorted by plays.
    :return:
    """
    albums = dao.get_albums_recent_played(db.db_session)
    if not albums:
        abort(404, {'message': 'Oops, no artists found!'})
    
    return render_include_context('albums.html', albums=albums)
# </editor-fold>


@app.teardown_appcontext
def shutdown_session(exception):
    db.db_session.remove()


@app.template_filter('urlencode')
def url_encode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = urllib.parse.quote(s)
    return Markup(s)

    
if __name__ == '__main__':

    # db.init_app(app)
    i = os.path.realpath(__file__).rfind(os.sep)
    file_dir = os.path.realpath(__file__)[:i]
    app.template_folder = join(file_dir, 'templates')
    app._static_folder = join(file_dir, 'static')
    Bootstrap(app)
    
    # p = LocalProxy(get_player)

    print('Hello World!')

    app.run(host=config.CONFIG['Other']['host_endpoint'], port=8080, debug=True)

