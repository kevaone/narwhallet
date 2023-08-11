import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class AuctionsScreen(Screen):
    auction_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.auction_list.data = []
        self.header.value = 'My Auctions'
        self.manager.current = 'auctions_screen'

        _asa = self.manager.cache.ns.get_view()

        for _a in _asa:
            _auctions = self.manager.cache.ns.get_namespace_auctions(_a[0])
            for _ac in _auctions:
                # _auc = json.loads(_ac[4])
                _oa = self.manager.cache.ns.last_address(_a[0])
                for _w in self.manager.wallets.wallets:
                    for address in _w.addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0])
                            if _auction != {}:
                                self.auction_list.data.append(_auction)

                    for address in _w.change_addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0])
                            if _auction != {}:
                                self.auction_list.data.append(_auction)

    def get_namespace(self, namespaceid):
        _provider = self.manager.settings_screen.settings.content_providers[0]
        _ns = MShared.get_namespace(namespaceid, _provider)
        _ns = _ns['result']

        if namespaceid in self.manager.favorites.favorites:
            _fav = 'narwhallet/core/kui/assets/star.png'
        else:
            _fav = 'narwhallet/core/kui/assets/star_dark.png'

        _dat = _ns['data']
        _dat.reverse()
        for _k in _dat:
            if _k['dtype'] == 'nft_auction':
                _na = json.loads(_k['dvalue'])
                _auction = {
                    'time': _k['time'],
                    'root_shortcode': str(_ns['root_shortcode']),
                    'desc': str(_na['desc']),
                    'displayName': str(_na['displayName']),
                    'price': str(_na['price']),
                    'bids': str(len(_k['replies'])),
                    'favorite_source': _fav,
                    'namespaceid': _ns['dnsid'],
                    'sm': self.manager
                }

                _hb = 0
                for _r in _k['replies']:
                    if _r['dvalue'] > _hb:
                        _hb = _r['dvalue']

                _auction['high_bid'] = str(_hb)
            return _auction
        return {}