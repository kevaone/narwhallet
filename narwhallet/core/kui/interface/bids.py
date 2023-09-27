import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class BidsScreen(Screen):
    bid_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.bid_list.data = []
        self.header.value = _tr.translate('My Bids')
        self.manager.current = 'bids_screen'

        # _asa = self.manager.cache.ns.get_view()
        _bids = {}

        # for _a in _asa:
        # _auctions = self.manager.cache.ns.get_namespace_bids(_a[0])
        # for _ac in _auctions:
        for _w in self.manager.wallets.wallets:
            for address in _w.addresses.addresses:
                for _us in address.namespaces:
                    if 'namespace_bids' not in _us: continue
                    for _ns in _us['namespace_bids']:
                        print('_ns', _ns)
                        # if _us['tx_hash'] == _ac[2] and _us['tx_pos'] == _ac[1]:
                        _bids[_ns['nsid']] = _w

            for address in _w.change_addresses.addresses:
                for _us in address.namespaces:
                    if 'namespace_bids' not in _us: continue
                    for _ns in _us['namespace_bids']:
                        print('_ns', _ns)
                        # if _us['tx_hash'] == _ac[2] and _us['tx_pos'] == _ac[1]:
                        _bids[_ns['nsid']] = _w

        for k, v in _bids.items():
            _auction = self.get_namespace(k, v)
            if _auction != {}:
                self.bid_list.data.append(_auction)

    def get_namespace(self, namespaceid, wallet):
        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
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
                _auction = {
                    'time': _k['time'],
                    'root_shortcode': str(_k['target'][0]),
                    'my_bid': str(_k['dvalue']),
                    'favorite_source': _fav,
                    # 'namespaceid': _ns['dnsid'],
                    'sm': self.manager
                }

                _auction_ns = MShared.get_shortcode(_k['target'][0], self.manager.kex)['result']
                _ans_dat = _auction_ns['data']
                _ans_dat.reverse()

                for _i in _ans_dat:
                    if _i['dtype'] == 'nft_auction':
                        _ad = json.loads(_i['dvalue'])
                        _auction['displayName'] = str(_ad['displayName'])
                        _auction['price'] = str(_ad['price'])
                        _auction['desc'] = str(_ad['desc'])
                        _auction['bids'] = str(len(_i['replies']))
                        _auction['namespaceid'] = _auction_ns['dnsid']
                        _hb = 0

                        for _b in _i['replies']:
                            if _b['dvalue'] > _hb:
                                _hb = _b['dvalue']

                        _auction['high_bid'] = str(_hb)

                return _auction
        return {}
