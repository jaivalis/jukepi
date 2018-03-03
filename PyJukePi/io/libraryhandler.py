import os
import pathlib
from os.path import isfile, join

SUPPORTED_FORMATS = ['.flac', '.mp3', '.m4a', '.ogg']
IMG_FORMATS = ['.jpg', '.jpeg', '.png']
# SUPPORTED_FORMATS = ['.mp3']
FILE_COUNT = 0

path_short = '/home/jaivalis/Downloads/Soulseek Downloads/complete/'
path_long = '/home/jaivalis/Music/Sorted/'


def type_filter(path, types):
    return pathlib.Path(path).suffix.lower() in types


def filtered_crawler(path=path_short, suffix_filter=SUPPORTED_FORMATS):
    global FILE_COUNT

    for (path, dirs, files) in os.walk(path):

        for file in files:
            if not type_filter(file, suffix_filter):
                continue

            FILE_COUNT += 1
            full_path = os.path.join(path, file)

            yield full_path, os.path.getmtime(full_path)


def get_artwork(path):
    img_files = [f for f in os.listdir(path) if isfile(join(path, f)) and type_filter(f, IMG_FORMATS)]
    
    print(img_files)
    for img in img_files:
        if 'front' in img.lower():
            return os.path.join(path, img)
        elif 'folder' in img.lower():
            return os.path.join(path, img)
        elif 'cover' in img.lower():
            return os.path.join(path, img)
    return None


if __name__ == '__main__':
    filtered_crawler()
    print('Found {} files.'.format(FILE_COUNT))
