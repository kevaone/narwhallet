import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header


class NamespacesScreen(Screen):
    namespaces_list = ObjectProperty(None)
    # wallet_name = Nwlabel()
    btn_create = Nwbutton()
    header = Header()

    def populate(self):
        self.header.value = self.manager.wallet_screen.header.value
        self.namespaces_list.scroll_y = 1
        self.namespaces_list.data = []
        
        _w = self.manager.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return

        if _w.kind == EWalletKind.NORMAL:
            self.btn_create.disabled = False
        else:
            self.btn_create.disabled = True
        
        _asa = self.manager.cache.ns.get_view()

        for p in _asa:
            _oa = self.manager.cache.ns.last_address(p[0])
            for address in _w.addresses.addresses:
                if _oa[0][0] == address.address:
                    _block = self.manager.cache.ns.ns_block(p[0])[0]
                    _ns_name = self.manager.cache.ns.ns_root_value(p[0])[0][0]
                    try:
                        _ns_name = json.loads(_ns_name)['displayName']
                    except:
                        pass

                    if p[0] in self.manager.favorites.favorites:
                        _fav = 'narwhallet/core/kui/assets/star.png'
                    else:
                        _fav = 'narwhallet/core/kui/assets/star_dark.png'
                    _ns = {
                    'address': p[0],
                    'shortcode': str(len(str(_block[0])))+str(_block[0])+str(_block[1]),
                    'keys': str(self.manager.cache.ns.key_count(p[0])[0][0]),
                    'sm': self.manager,
                    'ns_name': _ns_name,
                    'favorite_source': _fav}
                    self.namespaces_list.data.append(_ns)

            for address in _w.change_addresses.addresses:
                if _oa[0][0] == address.address:
                    _block = self.manager.cache.ns.ns_block(p[0])[0]
                    _ns_name = self.manager.cache.ns.ns_root_value(p[0])[0][0]
                    try:
                        _ns_name = json.loads(_ns_name)['displayName']
                    except:
                        pass

                    if p[0] in self.manager.favorites.favorites:
                        _fav = 'narwhallet/core/kui/assets/star.png'
                    else:
                        _fav = 'narwhallet/core/kui/assets/star_dark.png'
                    _ns = {
                    'address': p[0],
                    'shortcode': str(len(str(_block[0])))+str(_block[0])+str(_block[1]),
                    'keys': str(self.manager.cache.ns.key_count(p[0])[0][0]),
                    'sm': self.manager,
                    'ns_name': _ns_name,
                    'favorite_source': _fav}
                    self.namespaces_list.data.append(_ns)
        self.manager.current = 'namespaces_screen'
