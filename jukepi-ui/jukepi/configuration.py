import configparser
import logging
import os.path

from jukepi.exceptions import ConfigurationException

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = './resources/debug_config.yml'
DEFAULT_PLAYER_ENDPOINT = 'http://0.0.0.0:8888'

ENV = os.environ

if not os.path.exists(DEFAULT_CONFIG):
    raise ConfigurationException('Config file not found')

CONFIG = configparser.RawConfigParser()

CONFIG.read(DEFAULT_CONFIG)

if not CONFIG['Paths'] or not CONFIG['Paths']['library_dir']:
    raise ConfigurationException('Config file is missing entries')

endpoint_env = ENV.get('PLAYER_ENDPOINT')
rest_player_host = endpoint_env if endpoint_env else DEFAULT_PLAYER_ENDPOINT
