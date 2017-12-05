"""
    Linux SSH Scanner Core
"""

import paramiko

from paramiko.ssh_exception import AuthenticationException


class SSHScannerError(Exception):
    """ Basic SSHScanner Error """
    pass


class SSHScanner:
    """
        Connect to Linux Host, retrieve Hostname & Save Results
    """

    def __init__(self, **kwargs):
        """ Initialize attributes """

        self.out_file = kwargs.get('out_file', 'out.txt')
        self.command = kwargs.get('command')
        self.pairs = kwargs.get('pairs')

        if not self.command:
            raise SSHScannerError('No command supplied')

        if not self.pairs:
            raise SSHScannerError('No user/password pairs supplied')

        if len(self.pairs) != 2:
            raise SSHScannerError('Extacly two user/password pairs required')

        self._net = (192, 168, 1)

    def start(self):
        """ Start requesting hosts """

        fail = False

        with open(self.out_file, 'w') as handler:
            for addr in self._get_address():
                keys = self._get_credentials()

                try:
                    result = self._request_host(addr, **next(keys))
                except AuthenticationException:
                    result = '%s (EOS)' % self._request_host(addr, **next(keys))
                except Exception as error:
                    result = str(error)
                    fail = True

                handler.write('IP: %s %s' % (addr, result))

        return fail

    def _get_address(self):
        """ Build IP address """

        for part in range(1, 255):
            yield '.'.join(str(x) for x in iter(self._net + (part,)))

    def _get_credentials(self):
        """ Return user/password pair, support 2 pairs """

        for user, password in self.pairs:
            yield {
                'username': user,
                'password': password
            }

    def _request_host(self, addr, **kwargs):
        """ Connect to host, execute command, return result """

        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=addr, port=22, **kwargs)
            _, std_out, std_err = client.exec_command(self.command)
            data = std_out.read() + std_err.read()
            return 'Hostname: %s' % data.decode()
