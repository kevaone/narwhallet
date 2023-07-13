from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.namespacelistinfo import NamespaceListInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header


class NamespacesScreen(Screen):
    namespaces_list = ObjectProperty(None)
    # wallet_name = Nwlabel()
    header = Header()

    def populate(self):
        self.header.value = self.manager.wallet_screen.header.value
        self.namespaces_list.data = []
        
        _w = self.manager.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return
        
        _asa = self.manager.cache.ns.get_view()

        for p in _asa:
            _oa = self.manager.cache.ns.last_address(p[0])
            for address in _w.addresses.addresses:
                if _oa[0][0] == address.address:
                    _block = self.manager.cache.ns.ns_block(p[0])[0]
                    _ns = {
                    'address': p[0],
                    'shortcode': str(len(str(_block[0])))+str(_block[0])+str(_block[1]),
                    'keys': str(self.manager.cache.ns.key_count(p[0])[0][0]),
                    'sm': self.manager}
                    self.namespaces_list.data.append(_ns)

            for address in _w.change_addresses.addresses:
                if _oa[0][0] == address.address:
                    _block = self.manager.cache.ns.ns_block(p[0])[0]
                    _ns = {
                    'address': p[0],
                    'shortcode': str(len(str(_block[0])))+str(_block[0])+str(_block[1]),
                    'keys': str(self.manager.cache.ns.key_count(p[0])[0][0]),
                    'sm': self.manager}
                    self.namespaces_list.data.append(_ns)
            self.manager.current = 'namespaces_screen'
