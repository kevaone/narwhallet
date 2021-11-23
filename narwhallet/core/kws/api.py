import json
import urllib

from narwhallet.control import NarwhalletWebController
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.models.namespace import MNamespace
from narwhallet.core.kws.kits.microblog import Feed
from narwhallet.core.kcl.models.cache import MCache


class _Api():
    def __init__(self, control: NarwhalletWebController, cache):
        self.cmds = [
            'keva_filter',
            'getrawtransaction'
        ]
        self.bh: int = 0
        self.control: NarwhalletWebController = control
        self.content_path: str = self.control.theme_path
        self.cache: MCache = cache

    def querystring_to_dict(self, _data):
        _dict = {}
        _entries = _data.split('&')
        for _entry in _entries:
            _e = _entry.split('=')
            _dict[_e[0]] = urllib.parse.unquote(_e[1])

        return _dict

    def keva_get_namespace_by_id(self, nsid):
        try:
            return nsid, 'namespace'
        except Exception:
            return nsid, None

    def get_profile_theme(self, _id):
        return self.content_path+'/../theme/default/'

    def is_restricted_block(self, block) -> bool:
        pass

    def test_for_namespace(self, name):
        if len(name) != 2:
            return []

        _short_code = name[1]
        try:
            _short_code = int(_short_code)
        except Exception:
            _short_code = _short_code.decode()

        if isinstance(_short_code, int):
            _namespace = self.cache.ns.get_ns_by_shortcode(_short_code)
        else:
            _namespace = self.cache.ns.get_namespace_by_id(_short_code)

        if len(_namespace) == 0:
            if isinstance(_short_code, int):
                MShared.get_K(_short_code, self.cache, self.control.KEX)
                _namespace = self.cache.ns.get_ns_by_shortcode(_short_code)

        return _namespace

    def get_profile(self, _data):
        # _name = _data[0]
        _request_status = {}
        isRestricted = self.is_restricted_block(_data[0])

        if isRestricted is False:
            _request_status['payload'] = '_page'

        return _request_status

    def get_display_name(self, _ns):
        if 'displayName' in _ns:
            _reply_ns = json.loads(_ns)['displayName']

        return _reply_ns

    def get_block_id(self, _ns):
        _n_vout = str(len(str(_ns[0]))) + str(_ns[0]) + str(_ns[1])
        return _n_vout

    def get_block_links(self, _item):
        return _item

    def get_replies(self, _key):
        _replies = []
        return _replies

    def get_posts(self, _key):
        _posts = []
        return _posts

    def get_rewards(self, _key):
        _rewards = []
        return _rewards

    def get_bids(self, _key):
        _rewards = []
        return _rewards

    def get_nft_auctions(self, auction_type: int):
        if auction_type == 0:
            _result = ''
        else:
            _ = self.control.DF_KEX.peers[0].connect()
            # TODO Add HTTP commands to kex, remove hard code
            _nft_data = self.control.settings.data_feeds['nft_data']
            _cmd = ('GET ' + _nft_data[0] +
                    ' HTTP/1.1\r\nHost: ' + _nft_data[1] + '\r\n\r\n')
            _auctions = self.control.DF_KEX.call_batch(_cmd.encode(), False)
            _auctions = json.loads(_auctions.decode().split('\r\n\r\n')[1])

            _pigw = self.control.settings.primary_ipfs_gateway
            _microblog = Feed(self.content_path,
                              self.control.settings.ipfs_gateways[_pigw][2])

            _result = _microblog.get_auction_feed(_auctions,
                                                  auction_type)

        return _result

    def get_microblog(self, _namespace: list):
        # Default blog type view for rendering namespace's
        _pigw = self.control.settings.primary_ipfs_gateway
        _microblog = Feed(self.content_path,
                          self.control.settings.ipfs_gateways[_pigw][2])

        _result = _microblog.get_feed(_namespace, self.cache)
        return _result

    def search_get_namespace(self, _data):
        # _theme = _data[1]
        _data = self.querystring_to_dict(_data[0])
        if 'sq' in _data:
            _data['search'] = _data['sq']

        _request_status = {}
        return _request_status
