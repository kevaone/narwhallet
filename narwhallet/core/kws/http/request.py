from typing import List
# from narwhallet.core.kws.http.enumerations.mediatypes import content_type


class RequestProcessor():
    def __init__(self, connection):
        self.connection = connection
        self.headline: List[bytes] = ['', '', '']
        self.headers = []
        self.forwarded_for = b''  # X-Forwarded-For
        self.body = b''
        self.request_type = 'unknown'
        self.process()
        # self._method = None

    @property
    def method(self):
        return self.headline[0]

    def set_method(self, _method):
        self.headline[0] = _method

    @property
    def path(self):
        return self.headline[1]

    @property
    def path_root(self):
        return self.path.split(b'?')[0]

    @property
    def query_string(self):
        _tsq = self.path.split(b'?')
        if len(_tsq) > 1:
            return _tsq[1].split(b'&')

        return []

    def process(self):
        self._decoder()

    def _decoder(self):
        # TODO: Extend for receiving more than 8096 bytes
        _count = 0

        _command_extracted = False
        while _command_extracted is False:
            _tmp = self.connection.recv(8096)

            _bytes_to_read = len(_tmp)

            _split_tmp = _tmp.split(b'\n')

            self.headline = _split_tmp[_count].replace(b'\r', b'').split(b' ')
            _bytes_to_read -= len(_split_tmp[_count]) + 1

            while True:
                _count += 1
                _end = False
                if _split_tmp[_count] == b'\r':
                    _bytes_to_read -= len(_split_tmp[_count]) + 1
                    _end = True
                elif _count == 25:
                    _end = True

                if _end is True:
                    break

                _head = _split_tmp[_count].split(b': ')

                self.headers.append((_head[0], _head[1]))
                if _head[0] == b'X-Forwarded-For':
                    self.forwarded_for = _head[1]

                _bytes_to_read -= len(_split_tmp[_count]) + 1

            while True:
                _count += 1
                _end = False
                if _bytes_to_read == 0:
                    _end = True
                elif _split_tmp[_count] == b'':
                    _end = True
                elif _count == 250:
                    _end = True

                if _end is True:
                    break

                self.body += _split_tmp[_count]
                _bytes_to_read -= len(_split_tmp[_count])

            _command_extracted = True
