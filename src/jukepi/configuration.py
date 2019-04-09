import configparser

DEFAULT_CONFIG = '/home/jaivalis/workspace/PycharmProjects/PyJukePi/resources/debug_config.yml'

CONFIG = configparser.RawConfigParser()

CONFIG.read(DEFAULT_CONFIG)
