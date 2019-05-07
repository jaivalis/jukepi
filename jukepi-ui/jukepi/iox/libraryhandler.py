import logging
import os
import pathlib
from os.path import isfile, join

from jukepi.configuration import CONFIG


logger = logging.getLogger(__name__)


SUPPORTED_FORMATS = ['.flac', '.mp3', '.m4a', '.ogg']
IMG_FORMATS = ['.jpg', '.jpeg', '.png']
FILE_COUNT = 0

path_long = '/home/jaivalis/Music/Sorted/'


def type_filter(path: str, types):
    return pathlib.Path(path).suffix.lower() in types


def filtered_crawler(path: str, suffix_filter: list=SUPPORTED_FORMATS):
    logger.info('Scanning folder \'%s\' for files of type(s) \'%s\'', path, suffix_filter)
    global FILE_COUNT

    for (path, dirs, files) in os.walk(path):

        for file in files:
            if not type_filter(file, suffix_filter):
                continue

            FILE_COUNT += 1
            full_path = os.path.join(path, file)

            yield full_path, os.path.getmtime(full_path)


def get_artwork(path: str) -> str:
    img_files = [f for f in os.listdir(path) if isfile(join(path, f)) and type_filter(f, IMG_FORMATS)]

    logger.info(img_files)
    for img in img_files:
        if 'front' in img.lower() or 'folder' in img.lower() or 'cover' in img.lower():
            return os.path.join(path, img)
    return ''


if __name__ == '__main__':
    for f in filtered_crawler(CONFIG['Paths']['library_dir']):
        logger.debug(f)
    logger.info('Found %s files.', FILE_COUNT)
