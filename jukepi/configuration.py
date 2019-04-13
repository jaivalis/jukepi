import configparser
import logging
import os.path

from jukepi.exceptions import ConfigurationException

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = './resources/debug_config.yml'

if not os.path.exists(DEFAULT_CONFIG):
    raise ConfigurationException('Config file not found')

CONFIG = configparser.RawConfigParser()

CONFIG.read(DEFAULT_CONFIG)

if not CONFIG['Paths'] or not CONFIG['Paths']['library_dir']:
    raise ConfigurationException('Config file is missing entries')
