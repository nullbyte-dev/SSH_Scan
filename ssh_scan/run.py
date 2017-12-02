"""
    Linux SSH Scanner Runner
"""

import sys

from . import SSHScanner


CONF = {
    'out_file': 'out.txt',
    'command': 'hostname',
    'pairs': (
        ('user1', 'pass1'),
        ('user2', 'pass2')
    ),
}


def enter():
    """ Main Entry Point """

    failed = SSHScanner(**CONF).start()
    # True -> 1, False -> 0
    return int(failed)


if __name__ == '__main__':
    sys.exit(enter())
