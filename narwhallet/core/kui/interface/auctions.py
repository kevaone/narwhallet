import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class AuctionsScreen(Screen):
    auction_list = ObjectProperty(None)
    header = Header()

    def __init__(self, **kwargs):
        super(AuctionsScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self):
        self.auction_list.data = []
        self.header.value = 'My Auctions'
        self.manager.current = 'auctions_screen'

        for _w in self.app.ctrl.wallets.wallets:
            for address in _w.addresses.addresses:
                for _ns in address.namespaces:
                    if 'active_auction' in _ns:
                        if _ns['active_auction'][0] is True:
                            _auction = self.get_namespace(_ns['namespaceid'])
                            if _auction != {}:
                                self.auction_list.data.append(_auction)

            for address in _w.change_addresses.addresses:
                for _ns in address.namespaces:
                    if 'active_auction' in _ns:
                        if _ns['active_auction'][0] is True:
                            _auction = self.get_namespace(_ns['namespaceid'])
                            if _auction != {}:
                                self.auction_list.data.append(_auction)

    def get_namespace(self, namespaceid):
        _ns = MShared.get_namespace(namespaceid, self.app.ctrl.kex)
        if _ns is None:
            return

        if namespaceid in self.manager.favorites.favorites:
            _fav = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            _fav = 'narwhallet/core/kui/assets/star.png'

        _keys = len(_ns.keys.keys)
        _ns.keys.keys.reverse()
        _auction = {}
        for _k in _ns.keys.keys:
            if _k.dtype == 'name_update':
                break

            if _k.dtype == 'nft_auction':
                _na = json.loads(_k.dvalue)
                _auction = {
                    'time': _k.date[0],
                    'root_shortcode': str(_ns.shortcode),
                    'keys': str(_keys),
                    'desc': str(_na['desc']),
                    'displayName': str(_na['displayName']),
                    'price': str(_na['price']),
                    'bids': str(len(_k.replies)),
                    'favorite_source': _fav,
                    'namespaceid': _ns.namespaceid,
                    'sm': self.manager
                }

                _hb = 0
                for _r in _k.replies:
                    if _r.dvalue > _hb:
                        _hb = _r.dvalue

                _auction['high_bid'] = str(_hb)
                break
        return _auction
