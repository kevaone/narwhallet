
import socket
import ssl


class _peer():
    def __init__(self, host: str, port: int, tls: bool, validate_cert: bool):
        self.host = host
        self.port = port
        self.tls = tls
        self.last = 0
        self.socket = None
        self.validate_cert = validate_cert
        self.busy = False

    def connect(self):
        try:
            _sock = socket.create_connection((self.host, self.port), 15)
            if self.tls:
                _t_ctx = ssl.create_default_context()

                if self.validate_cert is False:
                    _t_ctx.check_hostname = False
                    _t_ctx.verify_mode = ssl.CERT_NONE

                _t_sock = _t_ctx.wrap_socket(_sock, server_hostname=self.host)

                self.socket = _t_sock
            else:
                self.socket = _sock
            return 'connected'
        except socket.timeout as ex:
            return str(ex)
        except socket.gaierror as ex:
            return str(ex)
        except socket.error as ex:
            return str(ex)
        except socket.herror as ex:
            return str(ex)

    def disconnect(self):
        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()

    def reconnect(self):
        self.disconnect()
        self.socket = self.connect()

    def comm(self, command) -> bytes:
        self.busy = True
        try:
            self.socket.sendall(command)
            data = b''

            while True:
                _r = self.socket.recv(4096)
                data = data + _r

                if data == b'':
                    break

                if (_r.endswith(b'"}\n')
                        or _r.endswith(b'}]\n')
                        or _r.endswith(b']\n}\n')):
                    break

            if data == b'':
                self.connect()
                data = self.comm(command)
        except Exception as ex:
            if ex == 'The read operation timed out':
                print('time out, reattempting', ex)
                self.connect()
                data = self.comm(command)
            else:
                data = b''
        self.busy = False
        return data
