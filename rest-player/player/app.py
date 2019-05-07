import logging
import os
import sys
import urllib.parse

from flask import Flask, request
from flask import jsonify
from markupsafe import Markup

from exceptions import ConfigurationException
from playback.mockmediaplayer import MockMediaPlayer
from werkzeug.exceptions import abort

app = Flask(__name__)

if os.environ['PLAYER'].lower() == 'mock':
    player = MockMediaPlayer()
elif os.environ['PLAYER'].lower() == 'vlc':
    pass
    # player = VlcMediaPlayer()
else:
    raise ConfigurationException('Player type not set.')


@app.route('/')
@app.route('/index')
def index():
    return 'Not playing', 200, {'Content-Type': 'text/plain'}


@app.route('/play', methods=['POST'])
def play_list():
    req_data = request.get_json(force=True)
    playlist = req_data['tracks']
    print(playlist)
    success = player.play(playlist)
    if success:
        return jsonify(success)
    else:
        abort(404, {'message': 'Oops, album not found!'})


@app.route('/pause')
def pause():
    if player.pause():
        return 'Paused', 200, {'Content-Type': 'text/plain'}
    else:
        abort(404, {'message': 'Oops, an error occurred.'})


@app.route('/fwd')
def forward():
    player.next()
    return '', 200, {'Content-Type': 'text/plain'}


@app.route('/bwd')
def backward():
    player.prev()
    return '', 200, {'Content-Type': 'text/plain'}


@app.route('/setVolume')
def set_volume():
    pass
#     volume = request.args.get('v', type=int)
#     vol.set_volume(volume)
#     return '', 200, {'Content-Type': 'text/plain'}


@app.route('/getVolume')
def get_volume():
    pass
#     return vol.get_volume(), 200, {'Content-Type': 'text/plain'}


def get_now_playing_id():
    return player.get_now_playing_id()


@app.route('/queue')
def get_play_queue():
    return jsonify({'tracks': player.get_queue()})


@app.teardown_appcontext
def shutdown_session(exception):
    pass


@app.template_filter('urlencode')
def url_encode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = urllib.parse.quote(s)
    return Markup(s)


if __name__ == '__main__':
    log_format = '%(asctime)s %(levelname)s %(name)s | %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

    # db.init_app(player)
    # p = LocalProxy(get_player)

    app.run(host='0.0.0.0', port=8888, debug=True)
