from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class AllScreen(Screen):
    all_list = RecycleView()
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('All')
        self.all_list.data = []

        for _w in self.manager.wallets.wallets:
            for address in _w.addresses.addresses:
                for _us in address.namespaces:
                    _fav = 'narwhallet/core/kui/assets/star_dark.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star.png'
                            break
                    _ns = {
                        'address': _us['namespaceid'],
                        'shortcode': str(_us['shortcode']),
                        'ns_name': str(_us['name']),
                        'keys': str(_us['keys']),
                        'sm': self.manager,
                        'favorite_source': _fav}
                    self.all_list.data.append(_ns)

            for address in _w.change_addresses.addresses:
                for _us in address.namespaces:
                    _fav = 'narwhallet/core/kui/assets/star_dark.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star.png'
                            break
                    _ns = {
                        'address': _us['namespaceid'],
                        'shortcode': str(_us['shortcode']),
                        'ns_name': str(_us['name']),
                        'keys': str(_us['keys']),
                        'sm': self.manager,
                        'favorite_source': _fav}
                    self.all_list.data.append(_ns)

        self.manager.current = 'all_screen'
