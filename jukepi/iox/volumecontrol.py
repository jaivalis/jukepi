import logging
import platform
import re
import subprocess

from subprocess import call


logger = logging.getLogger(__name__)
# fixme
# use: https://github.com/AndreMiras/pycaw


def get_volume() -> int:
    if platform.system() == 'Linux':
        # proc = subprocess.Popen(["amixer", "-D", "pulse", "get", "Master"], stdout=subprocess.PIPE)
        # output = proc.stdout.read()
        #
        # m = re.search(r"\[([0-9]+)(%)\]", str(output))
        # assert 0 <= int(m.group(1)) <= 100
        # return int(m.group(1))
        return 0
    elif platform.system() == 'Darwin':
        output = str(subprocess.check_output(['osascript', '-e', '"get volume settings"']))
        return int(output[16:output.index(',')])


def set_volume(val: int):
    if platform.system() == 'Linux':
        # subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(val) + '%'])
        pass
    elif platform.system() == 'Darwin':
        # osascript.osascript("set volume output volume " + str(val))
        call(["osascript -e 'set volume " + str(val / 10) + "'"], shell=True)


def modify_volume(delta: int):
    assert isinstance(delta, int)
    if platform.system() == 'Linux':
        # delta_str = str(delta) + '%+' if delta > 0 else str(delta) + '%-'
        # subprocess.call(["amixer", "-D", "pulse", "sset", "Master", delta_str])
        pass
    elif platform.system() == 'Darwin':
        set_volume(get_volume() + delta)


def mute():
    if platform.system() == 'Linux':
        # subprocess.call(["amixer", "-D", "pulse", "sset", "Master", '0%'])
        pass
    elif platform.system() == 'Darwin':
        # osascript.osascript("set volume output volume 0")
        call(["osascript -e 'set volume 0'"], shell=True)


if __name__ == '__main__':
    logger.info('Current volume: %s', get_volume())
