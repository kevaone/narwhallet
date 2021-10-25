import os
import socket
from core.kws.http.enumerations.mediatypes import content_type
from core.kws.http.enumerations.http_status_codes import status_codes


class ResponseBuilder():
    def __init__(self, connection):
        self.connection: socket.socket = connection

        # self.content_type = _response[2] #_content_type
        self.body = b'no data'

        self.header_list = [
            'Connection: close'
        ]

        self.protocol = 'HTTP/1.1'
        self.status_code = 403
        self.status_text = 'Forbidden'

    @property
    def headline(self):
        _p = self.protocol
        _sc = self.status_code
        _st = self.status_text
        _hl = ''.join('%s %s %s\r\n' % (_p, _sc, _st))
        return _hl.encode()

    @property
    def headers(self):
        _h = ''.join('%s\r\n' % (v) for v in self.header_list) + '\r\n'
        return _h.encode()

    @property
    def content_length(self):
        return len(self.body)

    def add_header(self, header, value):
        self.header_list.append(header + ': ' + value)

    def set_content_type(self, c_type):
        self.add_header('Content-Type', content_type[c_type].value)

    def set_content_length(self):
        for i in range(0, len(self.header_list)):
            if 'Content-Length' in self.header_list[i]:
                self.header_list.pop(i)
                break

        self.add_header('Content-Length', str(self.content_length))

    def set_status(self, code):
        _code = status_codes[code].value
        self.status_code = _code[0]
        self.status_text = _code[1]

    def send(self, close_connection=True):
        self.connection.send(self.headline)
        self.connection.send(self.headers)
        self.connection.send(self.body)

        # and closing connection, as we stated before
        if close_connection:
            self.connection.close()

    def body_from_file(self, **args):
        _content = b'no data'
        _content_path = args['file']
        # _content_path = os.path.join(_path, _file)

        try:
            with open(_content_path, mode='rb') as _content_file:
                _content = _content_file.read()

            # Set body
            self.body = _content
            # Set headers
            self.add_header('Content-Type',
                            content_type[args['file'].split('.')[-1]].value)
            self.add_header('Content-Length', str(self.content_length))

            self.set_status('OK')
        except FileNotFoundError:
            self.set_status('NotFound')
        except Exception:
            self.set_status('UnicodeDecodeError')

    def body_from_parts(self, **args):
        _content = args['content']
        _path = args['path']

        try:
            with open(os.path.join(_path, 'meta.html'), mode='rb') as _file:
                _page_meta = _file.read()
            with open(os.path.join(_path, 'header.html'), mode='rb') as _file:
                _page_header = _file.read()
            with open(os.path.join(_path, 'footer.html'), mode='rb') as _file:
                _page_footer = _file.read()

            with open(os.path.join(_path, _content), mode='rb') as _file:
                _page_content = _file.read()

                if 'content_inject' in args:
                    for key in args['content_inject']:
                        if key[0] == '$':
                            _ag = args['content_inject'][key].encode()
                            _page_content = (_page_content
                                             .replace(key.encode(), _ag))

            _page_content = _page_content.replace(b'$error', b'')

            _page_meta = (_page_meta
                          .replace(b'$header', _page_header)
                          .replace(b'$footer', _page_footer)
                          .replace(b'$content', _page_content))

            self.body = _page_meta
            # Set headers
            self.add_header('Content-Type',
                            content_type[args['content'].split('.')[-1]].value)
            self.add_header('Content-Length', str(self.content_length))

            self.set_status('OK')
        except FileNotFoundError:
            self.set_status('NotFound')
        except Exception:
            self.set_status('UnicodeDecodeError')
