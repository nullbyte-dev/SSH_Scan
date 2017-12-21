"""
    Linux SSH Scanner Runner
"""

import sys

from ssh_scan.core import SSHScanner, SFTPSender


CREDENTIALS = {
    'pairs': (
        ('user1', 'pass1'),
        ('user2', 'pass2')
    ),
}

SCAN_CONFIG = {
    'out_file': 'scan_out.txt',
    'command': 'hostname',
}

SEND_CONFIG = {
    'out_file': 'send_out.txt',
    'from_path': '/path/to/local/file',
    'to_path':  '/path/where/put/file',
}

SCAN_CONFIG.update(CREDENTIALS)
SEND_CONFIG.update(CREDENTIALS)


def enter():
    """ Main Entry Point """

    scan_status = SSHScanner(**SCAN_CONFIG).start()
    send_status = SFTPSender(**SEND_CONFIG).start()

    # True -> 1, False -> 0
    return int(scan_status or send_status)


if __name__ == '__main__':
    sys.exit(enter())
