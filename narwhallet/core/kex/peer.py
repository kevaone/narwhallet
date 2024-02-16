import socket
import ssl
import logging


class PeerError(Exception):
    pass

class Peer:
    def __init__(self, host: str, port: int, tls: bool,
                 validate_cert: bool, timeout: float = 45.0,
                 buffer_size: int = 1024):
        self.host: str = host
        self.port: int = port
        self.tls: bool = tls
        self.validate_cert: bool = validate_cert
        self.timeout: float = timeout
        self.buffer_size: int = buffer_size
        self.socket: socket.socket | None = None
        self.busy = False

    def _create_socket(self) -> socket.socket:
        try:
            _sock = socket.create_connection((self.host, self.port), self.timeout)
            if self.tls:
                _t_ctx = ssl.create_default_context()
                if not self.validate_cert:
                    _t_ctx.check_hostname = False
                    _t_ctx.verify_mode = ssl.CERT_NONE
                _sock = _t_ctx.wrap_socket(_sock, server_hostname=self.host)
            _sock.settimeout(self.timeout)
            return _sock
        except Exception as ex:
            raise PeerError(f'Failed to create socket: {ex}')

    def connect(self) -> str:
        try:
            self.disconnect()  # Ensure any existing connection is closed
            self.socket = self._create_socket()
            logging.info('Connection established')
            return 'Connection established'
        except PeerError as ex:
            logging.error(f'Socket creation failed: {ex}')
            return f'Socket creation failed: {ex}'

    def disconnect(self) -> None:
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except socket.error as ex:
                logging.warning(f'Error during socket shutdown: {ex}')
            finally:
                self.socket.close()
                self.socket = None
                logging.info('Disconnected')

    def comm(self, command: bytes) -> bytes:
        if not self.socket:
            raise PeerError('Not connected')
        self.busy = True
        data = b''
        try:
            self.socket.sendall(command)
            while True:
                _r = self.socket.recv(self.buffer_size)
                data += _r
                if len(_r) < self.buffer_size:
                    break
        except socket.error as ex:
            logging.error(f'Communication error: {ex}')
            raise PeerError(f'Communication error: {ex}')
        finally:
            self.busy = False
        return data
