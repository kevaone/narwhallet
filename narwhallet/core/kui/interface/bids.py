import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class BidsScreen(Screen):
    bid_list = ObjectProperty(None)
    header = Header()

    def __init__(self, **kwargs):
        super(BidsScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self):
        self.bid_list.data = []
        self.header.value = 'My Bids'
        self.manager.current = 'bids_screen'
        _bids = {}
        _b = [] 

        for _w in self.app.ctrl.wallets.wallets:
            for address in _w.addresses.addresses:
                for _us in address.namespaces:
                    if 'namespace_bids' not in _us: continue
                    for _ns in _us['namespace_bids']:
                        _b.append([_ns['nsid'], _ns['shortcode'], _us['namespaceid'], _ns['txid']])

            for address in _w.change_addresses.addresses:
                for _us in address.namespaces:
                    if 'namespace_bids' not in _us: continue
                    for _ns in _us['namespace_bids']:
                        _b.append([_ns['nsid'], _ns['shortcode'], _us['namespaceid'], _ns['txid']])

        for k, n, v, c in _b: 
            _auction = self.get_namespace(k, n, v, c)
            if _auction != {}:
                self.bid_list.data.append(_auction)

    def get_namespace(self, bid_nsid, bid_shortcode, namespaceid, bid_tx):
        _ns = MShared.get_namespace(bid_nsid, self.app.ctrl.kex)
        if _ns is None:
            return

        if bid_nsid in self.manager.favorites.favorites:
            _fav = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            _fav = 'narwhallet/core/kui/assets/star.png'

        _keys = len(_ns.keys.keys)
        _ns.keys.keys.reverse()
        _auction = {}

        for _k in _ns.keys.keys:
            if _k.dtype == 'name_update':
                return {}

            if _k.dtype == 'nft_auction':
                _ad = json.loads(_k.dvalue)
                _auction = {
                    'time': _k.date[0],
                    'namespaceid': bid_nsid,
                    'root_shortcode': str(bid_shortcode),
                    'keys': str(_keys),
                    'displayName': str(_ad['displayName']),
                    'price': str(_ad['price']),
                    'desc': str(_ad['desc']),
                    'favorite_source': _fav,
                    'sm': self.manager
                }

                _bid_count = 0
                _high_bid = 0.0

                for _r in _k.replies:
                    if _r.dtype != 'nft_bid':
                        continue

                    try:
                        if _r.dvalue > _high_bid:
                            _high_bid = _r.dvalue
                            _auction['high_bid'] = str(_high_bid)
                    except:
                        continue

                    if _r.namespaceid == namespaceid and _r.dkey[4:] == bid_tx:
                        _auction['my_bid'] = str(_r.dvalue)
                    _bid_count = _bid_count + 1
                _auction['bids'] = str(_bid_count)

                if 'my_bid' in _auction:
                    return _auction
        return {}
