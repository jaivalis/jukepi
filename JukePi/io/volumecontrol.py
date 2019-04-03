import logging
import re
import subprocess


logger = logging.getLogger(__name__)


def get_volume():
    proc = subprocess.Popen(["amixer", "-D", "pulse", "get", "Master"], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    
    m = re.search(r"\[([0-9]+)(%)\]", str(output))
    assert 0 <= int(m.group(1)) <= 100
    return int(m.group(1))
    

def set_volume(val: int):
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(val) + '%'])


def modify_volume(delta: int):
    assert isinstance(delta, int)
    delta_str = str(delta) + '%+' if delta > 0 else str(delta) + '%-'
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", delta_str])


def mute():
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", '0%'])


if __name__ == '__main__':
    logger.info('Current volume: %s', get_volume())
