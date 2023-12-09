import socket
import ssl
import logging


class PeerError(Exception):
    pass

class Peer:
    def __init__(self, host: str, port: int, tls: bool,
                 validate_cert: bool, timeout=45.0, buffer_size=1024):
        self.host = host
        self.port = port
        self.tls = tls
        self.validate_cert = validate_cert
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.socket = None
        self.busy = False

    def _create_socket(self):
        _sock = socket.create_connection((self.host, self.port), self.timeout)
        if self.tls:
            _t_ctx = ssl.create_default_context()
            if not self.validate_cert:
                _t_ctx.check_hostname = False
                _t_ctx.verify_mode = ssl.CERT_NONE
            return _t_ctx.wrap_socket(_sock, server_hostname=self.host)
        return _sock

    def connect(self):
        try:
            self.disconnect()
            self.socket = self._create_socket()
            logging.info('Connection established')
            return 'Connection established'
        except socket.error as ex:
            self.socket = None
            logging.error(f'Socket creation failed: {ex}')
            return f'Socket creation failed: {ex}'

    def disconnect(self):
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except socket.error as ex:
                logging.warning(f'Error during disconnection: {ex}')
            finally:
                self.socket = None
            logging.info('Disconnected')

    def comm(self, command: bytes) -> bytes:
        if not self.socket:
            raise PeerError('Not connected')
        self.busy = True
        data = b''
        try:
            self.socket.sendall(command)
            self.socket.settimeout(self.timeout)
            while True:
                _r = self.socket.recv(self.buffer_size)
                data += _r
                if len(_r) < self.buffer_size:
                    break
        except socket.error as ex:
            logging.error(f'Communication error: {ex}')
            raise
        finally:
            self.busy = False
        return data
