from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class NftScreen(Screen):
    nft_list = RecycleView()
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('Nft''s')
        self.nft_list.data = []
        _asa = self.manager.cache.ns.get_view()

        for _a in _asa:
            _auctions = self.manager.cache.ns.get_namespace_auctions(_a[0])
            for _ac in _auctions:
                _oa = self.manager.cache.ns.last_address(_a[0])
                for _w in self.manager.wallets.wallets:
                    for address in _w.addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0])
                            if _auction != {}:
                                self.nft_list.data.append(_auction)

                    for address in _w.change_addresses.addresses:
                        if _oa[0][0] == address.address:
                            _auction = self.get_namespace(_a[0])
                            if _auction != {}:
                                self.nft_list.data.append(_auction)

        self.manager.current = 'nft_screen'

    def get_namespace(self, namespaceid):
        _provider = self.manager.settings_screen.settings.content_providers[0]
        _ns = MShared.get_namespace(namespaceid, _provider)
        _ns = _ns['result']

        if namespaceid in self.manager.favorites.favorites:
            _fav = 'narwhallet/core/kui/assets/star.png'
        else:
            _fav = 'narwhallet/core/kui/assets/star_dark.png'

        _nft = {
            'shortcode': str(_ns['root_shortcode']),
            'ns_name': str(_ns['name']),
            'keys': str(len(_ns['data'])),
            'favorite_source': _fav,
            'namespaceid': _ns['dnsid'],
            'sm': self.manager
        }

        return _nft
