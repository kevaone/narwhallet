import socket

from core.kws.http import request as _Request
from core.kws.http import response as _Response
from core.kws.api import _Api
from core.kcl.models.cache import MCache
from control import NarwhalletWebController
from control.shared import MShared


class Processor():
    def __init__(self, client, control: NarwhalletWebController):
        self.client = client
        self.control = control
        self.who: str = self.control.who
        self.content_path: str = self.control.theme_path

        self.api_path = b'/'
        self.cache: MCache = MCache(self.control.db_file)

        self.sAPI = _Api(self.control, self.cache)

    def process(self, _connection: socket.socket):
        try:
            _request = _Request.RequestProcessor(_connection)

            if _request.forwarded_for != b'':
                self.client = _request.forwarded_for.replace(b'\r', b'')
                self.client.decode()

            _response = _Response.ResponseBuilder(_connection)
            _Api_req_dat = []
            _return_status = 0

            if _request.method == b'GET':
                content_inject = {}
                # TODO Swap to check against media types enum
                if b'.' in _request.path:
                    _tmp = _request.headline[1].decode().split('?')[0]
                    _tmp = _tmp.split('.')[-1]
                    if _tmp != 'html':
                        _file = self.content_path
                        _file = _file + _request.headline[1].decode()
                        _file = _file.split('?')[0]
                        _response.body_from_file(file=_file)
                        if _tmp != 'svg':
                            _response.add_header('Cache-Control',
                                                 'must-revalidate, max-age=0')

                content_inject['$keva_name'] = ''
                content_inject['$namespace'] = ''

                if _request.path == b'/':
                    _ci = {'$search_results': ''}
                    _response.body_from_parts(content='main.html',
                                              content_inject=_ci,
                                              path=self.content_path)
                elif _request.path.startswith(b'/about'):
                    _response.body_from_parts(content='about.html',
                                              path=self.content_path,
                                              content_inject=content_inject)
                elif _request.path.startswith(b'/howto'):
                    _response.body_from_parts(content='howto.html',
                                              path=self.content_path,
                                              content_inject=content_inject)
                elif _request.path.startswith(b'/marketplace'):
                    if b'numbers' in _request.path:
                        _result = self.sAPI.get_nft_auctions(2)
                    elif b'mine' in _request.path:
                        _result = self.sAPI.get_nft_auctions(0)
                    else:
                        _result = self.sAPI.get_nft_auctions(1)
                    _result = {'$search_results': _result}
                    _response.body_from_parts(content='marketplace.html',
                                              content_inject=_result,
                                              path=self.content_path)
                elif _request.path.startswith(b'/search'):
                    if len(_request.query_string) == 0:
                        _ci = {'$search_results': ''}
                        _response.body_from_parts(content='main.html',
                                                  content_inject=_ci,
                                                  path=self.content_path)
                    else:
                        # _Api_function = 'search_get_namespace'
                        _Api_req_dat.append(_request.query_string[0].decode())
                        _dt = self.content_path
                        _Api_req_dat.append(_dt)
                        _result = self.sAPI.search_get_namespace(_Api_req_dat)
                        _response.body_from_parts(content='main.html',
                                                  content_inject=_result,
                                                  path=self.content_path)
                elif _request.path.startswith(b'/shutdown'):
                    _return_status = 3
                    _response.body_from_parts(content='shutdown.html',
                                              path=self.content_path,
                                              content_inject=content_inject)
                elif b'.' not in _request.path:
                    # Test reqest path for possible shortcode
                    _short_code = _request.path.split(b'/')
                    if len(_short_code) != 2:
                        # TODO fix abort hack
                        return
                    _short_code = _short_code[1]
                    try:
                        _short_code = int(_short_code)
                    except Exception:
                        _short_code = _short_code.decode()

                    if isinstance(_short_code, int):
                        _namespace = (self.cache.ns
                                      .get_ns_by_shortcode(_short_code))
                    else:
                        _namespace = (self.cache.ns
                                      .get_namespace_by_id(_short_code))

                    if len(_namespace) == 0:
                        if isinstance(_short_code, int):
                            MShared.get_K(_short_code, 'live',
                                          self.cache, self.control.KEX)
                            _namespace = (self.cache.ns
                                          .get_ns_by_shortcode(_short_code))

                    if len(_namespace) > 0:
                        _result_data = self.sAPI.get_microblog(_namespace)
                        _c = 'profile_feed_meta.html'
                        _ci = {'$feed': _result_data}
                        _response.body_from_parts(content=_c,
                                                  content_inject=_ci,
                                                  path=self.content_path)
                    else:
                        _ci = {'$error': ''}
                        _response.body_from_parts(content='error.html',
                                                  content_inject=_ci,
                                                  path=self.content_path)

            elif _request.method == b'POST':
                if _request.path == (b'/search'):
                    # HACK Fix this up to be functional
                    _request.body = _request.body.replace(b'search=', b'')
                    _response.status_code = 301
                    _response.status_text = 'Moved'
                    _response.add_header('Location',
                                         '/'+_request.body.decode())

            _response.body = _response.body.replace(b'$who', self.who.encode())
            _response.set_content_length()
            _response.send()
        except Exception as er:
            # _response = _Response.ResponseBuilder(_connection, self.client)
            # _response.body_from_parts(content='/error.html',
            #         content_inject={'$error': er}, path=self.content_path)
            # _response.body = _response.body.replace(b'$who',
            #                                         self.who.encode())
            # _response.set_content_length()
            # _response.send()
            _return_status = 1
            print('web error:', er)
        self.cache.interface.close_cursor()
        _connection.close()

        return _return_status
