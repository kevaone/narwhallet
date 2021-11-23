import threading
import ssl
import socket

from narwhallet.control.web_controller import NarwhalletWebController
from narwhallet.core.kws.processor import Processor


class Server():
    def __init__(self):
        self._thread = None
        self.ssl_thread = None
        self.server_run_state = True
        self.connections = []
        self.control = NarwhalletWebController()
        self.load_socket()

    def load_socket(self):
        self.__load_tcp_socket(False)
        # self.__load_tcp_socket(True)

    def __load_tcp_socket(self, _ssl: bool):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if _ssl is True:
            _socket.bind((self.control.strap.ip, 4443))
        else:
            _socket.bind((self.control.strap.ip, self.control.strap.port))

        _socket.listen(5)

        if _ssl is True:
            _ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            _ssl_ctx.load_cert_chain(self.control.strap.ssl_cert,
                                     self.control.strap.ssl_key)
            _ssl_socket = _ssl_ctx.wrap_socket(_socket, server_side=True)
            self.ssl_thread = threading.Thread(target=self.__receive,
                                               args=(_ssl_socket, ))
            self.ssl_thread.start()
        else:
            self._thread = threading.Thread(target=self.__receive,
                                            args=(_socket, ))

            self._thread.start()

    def __receive(self, _socket: socket.socket):
        while self.server_run_state is True:
            try:
                c, addr = _socket.accept()
                _conn_thread = threading.Thread(target=self.process,
                                                args=(c, addr[0], ))

                self.connections.append(_conn_thread)
                _conn_thread.start()

            except Exception as er:
                print('error:', er)
        _socket.shutdown(socket.SHUT_RDWR)
        _socket.close()

    def process(self, _connection, c):
        _proc = Processor(c, self.control)
        _return_status = _proc.process(_connection)
        if _return_status == 3:
            self.server_run_state = False
