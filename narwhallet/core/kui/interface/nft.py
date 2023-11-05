from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.core.kui.widgets.header import Header


class NftScreen(Screen):
    nft_list = Nwgrid()
    header = Header()

    def populate(self):
        self.header.value = 'Nft''s'
        self.nft_list.data = []

        for _w in self.manager.wallets.wallets:
            for address in _w.addresses.addresses:
                for _us in address.namespaces:
                    _fav = 'narwhallet/core/kui/assets/star.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star_dark.png'
                            break
                    _ns = {
                        'namespaceid': _us['namespaceid'],
                        'shortcode': str(_us['shortcode']),
                        'ns_name': str(_us['name']),
                        'keys': str(_us['keys']),
                        'sm': self.manager,
                        'favorite_source': _fav}
                    self.nft_list.data.append(_ns)

            for address in _w.change_addresses.addresses:
                for _us in address.namespaces:
                    _fav = 'narwhallet/core/kui/assets/star.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star_dark.png'
                            break
                    _ns = {
                        'namespaceid': _us['namespaceid'],
                        'shortcode': str(_us['shortcode']),
                        'ns_name': str(_us['name']),
                        'keys': str(_us['keys']),
                        'sm': self.manager,
                        'favorite_source': _fav}
                    self.nft_list.data.append(_ns)

        self.manager.current = 'nft_screen'
