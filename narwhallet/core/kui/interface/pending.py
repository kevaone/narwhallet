import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class PendingScreen(Screen):
    bid_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.bid_list.data = []
        self.header.value = 'My Bids'
        self.manager.current = 'pending_screen'

        _asa = self.manager.cache.ns.get_view()

        for _a in _asa:
            _auctions = self.manager.cache.ns.get_namespace_bids(_a[0])
            for _ac in _auctions:
                _oa = self.manager.cache.ns.last_address(_a[0])
                for _w in self.manager.wallets.wallets:
                    for address in _w.addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0], _w)
                            if _auction != {}:
                                self.bid_list.data.append(_auction)

                    for address in _w.change_addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0], _w)
                            if _auction != {}:
                                self.bid_list.data.append(_auction)

    def get_namespace(self, namespaceid, wallet):
        _provider = self.manager.settings_screen.settings.content_providers[0]
        _ns = MShared.get_namespace(namespaceid, _provider)
        _ns = _ns['result']

        if namespaceid in self.manager.favorites.favorites:
            _fav = 'narwhallet/core/kui/assets/star.png'
        else:
            _fav = 'narwhallet/core/kui/assets/star_dark.png'

        _dat = _ns['data']
        _dat.reverse()
        _auction = {}
        for _k in _dat:
            if _k['dtype'] == 'nft_bid':
                if _k['addr'] in wallet.addresses.addresses:
                    _auction = {
                        'time': _k['time'],
                        'root_shortcode': str(_k['target'][0]),
                        'desc': '', #str(_na['desc']),
                        'displayName': str(_k['target'][1]),
                        'price': str(_k['dvalue']),
                        'bids': str("result['bids'][0]"),
                        'high_bid': str("result['bids'][1]"),
                        'favorite_source': _fav,
                        'namespaceid': _ns['dnsid'],
                        'sm': self.manager
                    }
                    return _auction

                if _k['addr'] in wallet.change_addresses.addresses:
                    _auction = {
                        'time': _k['time'],
                        'root_shortcode': str(_k['target'][0]),
                        'desc': '', #str(_na['desc']),
                        'displayName': str(_k['target'][1]),
                        'price': str(_k['dvalue']),
                        'bids': str("result['bids'][0]"),
                        'high_bid': str("result['bids'][1]"),
                        'favorite_source': _fav,
                        'namespaceid': _ns['dnsid'],
                        'sm': self.manager
                    }
                    return _auction
        return {}
