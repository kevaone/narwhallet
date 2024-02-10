from kivy.app import App
from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.core.kui.widgets.header import Header


class AllScreen(Screen):
    all_list = Nwgrid()
    header = Header()

    def __init__(self, **kwargs):
        super(AllScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self):
        self.header.value = 'All'
        self.all_list.data = []

        for _w in self.app.ctrl.wallets.wallets:
            for address in _w.addresses.addresses:
                for _us in address.namespaces:
                    _fav = 'narwhallet/core/kui/assets/star.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star_dark.png'
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
                    _fav = 'narwhallet/core/kui/assets/star.png'
                    for favorite in self.manager.favorites.favorites:
                        if favorite == _us['namespaceid']:
                            _fav = 'narwhallet/core/kui/assets/star_dark.png'
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
