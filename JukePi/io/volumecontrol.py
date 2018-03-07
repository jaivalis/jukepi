import re
import subprocess


def get_volume():
    proc = subprocess.Popen(["amixer", "-D", "pulse", "get", "Master"], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    
    m = re.search(r"\[([0-9]+)(%)\]", str(output))
    return int(m.group(1))
    

def set_volume(val):
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(val) + '%'])


def modify_volume(delta):
    assert isinstance(delta, int)
    if delta > 0:
        pass
    delta_str = str(delta) + '%+' if delta > 0 else str(delta) + '%-'
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", delta_str])


def mute():
    subprocess.call(["amixer", "-D", "pulse", "sset", "Master", '0%'])


if __name__ == '__main__':
    print (get_volume())