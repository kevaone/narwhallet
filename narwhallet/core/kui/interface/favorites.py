import json
from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class FavoritesScreen(Screen):
    favorites_list = Nwgrid()
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('Favorites')
        self.favorites_list.data = []

        for favorite in self.manager.favorites.favorites:
            _ns = MShared.get_namespace(favorite, self.manager.kex)
            _ns = _ns['result']

            try:
                _name = json.loads(_ns['name'])['displayName']
            except:
                _name = _ns['name']

            _fav = 'narwhallet/core/kui/assets/star.png'
            _ns = {
                'address': favorite,
                'shortcode': _ns['root_shortcode'],
                'ns_name': str(_name),
                'keys': str(len(_ns['data'])),
                'sm': self.manager,
                'favorite_source': _fav}
            self.favorites_list.data.append(_ns)

        self.manager.current = 'favorites_screen'
