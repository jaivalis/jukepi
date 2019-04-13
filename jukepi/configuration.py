import configparser
import os.path
import logging


logger = logging.getLogger(__name__)

DEFAULT_CONFIG = './resources/debug_config.yml'

if not os.path.exists(DEFAULT_CONFIG):
    logger.error('Config file not found')
    exit(0)

CONFIG = configparser.RawConfigParser()

CONFIG.read(DEFAULT_CONFIG)

if not CONFIG['Paths'] or not CONFIG['Paths']['library_dir']:
    logger.error('Config file is missing entries')
    exit(0)
