"""
    Linux SSH Scanner & SFTP Sender Core
"""

import paramiko

from paramiko.ssh_exception import AuthenticationException


class BaseSSHClientError(Exception):
    """ Basic client error """
    pass


class SSHScannerError(BaseSSHClientError):
    """ Basic SSHScanner Error """
    pass


class SFTPSenderError(BaseSSHClientError):
    """ Basic SFTPSender Error """
    pass


class BaseSSHClient:
    """ Abstract class for Client """

    def __init__(self, **kwargs):
        """ Initialize attributes """

        self.port = 22

        self.out_file = kwargs.get('out_file', 'out.txt')
        self.pairs = kwargs.get('pairs')

        if not self.pairs:
            raise BaseSSHClientError('No user/password pairs supplied')

        if len(self.pairs) != 2:
            raise BaseSSHClientError('Extactly two user/password pairs required')

        self.net = (192, 168, 1)

    def start(self):
        """ Start requesting hosts """

        fail = False

        with open(self.out_file, 'w') as handler:
            for addr in self.get_address():
                keys = self.get_credentials()

                try:
                    result = self.request_host(addr, **next(keys))

                except AuthenticationException:
                    result = '%s (EOS)' % self.request_host(addr, **next(keys))

                except Exception as error:
                    result = str(error)
                    fail = True

                handler.write('IP: %s %s' % (addr, result))

        return fail

    def get_address(self):
        """ Build IP address """

        for part in range(1, 255):
            yield '.'.join(str(x) for x in iter(self.net + (part,)))

    def get_credentials(self):
        """ Return user/password pair, support 2 pairs """

        for user, password in self.pairs:
            yield {
                'username': user,
                'password': password
            }

    def request_host(self, addr, **kwargs):
        """ Implement request logic in subclasses """

        raise NotImplementedError


class SSHScanner(BaseSSHClient):
    """
        Connect to Linux Host, execute bash command & save Results
    """

    def __init__(self, **kwargs):
        """ Initialize attributes """

        super().__init__(**kwargs)

        self.command = kwargs.get('command')

        if not self.command:
            raise SSHScannerError('No command supplied')

    def request_host(self, addr, **kwargs):
        """ Connect to host, execute command, return result """

        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=addr, port=self.port, **kwargs)
            _, std_out, std_err = client.exec_command(self.command)
            data = std_out.read() + std_err.read()

            return 'Hostname: %s' % data.decode()


class SFTPSender(BaseSSHClient):

    def __init__(self, **kwargs):
        """ Initialize attributes """

        super().__init__(**kwargs)

        self.from_path = kwargs.get('from_path')
        self.to_path = kwargs.get('to_path')

        if not self.from_path:
            raise SFTPSenderError('Nothing to send')

        if not self.to_path:
            raise SFTPSenderError('No remote path')

    def request_host(self, addr, **kwargs):
        """ Connect to host, send file, return result """

        with paramiko.Transport((addr, self.port)) as transport:
            transport.connect(**kwargs)

            with paramiko.SFTPClient.from_transport(transport) as sftp:
                state = 'OK'

                try:
                    sftp.put(self.from_path, self.to_path)
                except Exception:
                    state = 'FAILED'

                return state
