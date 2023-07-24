from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class FavoritesScreen(Screen):
    favorites_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = 'Favorites'
        self.favorites_list.data = []
        _asa = self.manager.cache.ns.get_view()

        for p in _asa:
            for favorite in self.manager.favorites.favorites:
                if p[0] == favorite:
                    _block = self.manager.cache.ns.ns_block(p[0])[0]
                    _ns_name = self.manager.cache.ns.ns_root_value(p[0])[0][0]
                    _fav = 'narwhallet/core/kui/assets/star.png'
                    _ns = {
                        'address': p[0],
                        'shortcode': str(len(str(_block[0])))+str(_block[0])+str(_block[1]),
                        'ns_name': str(_ns_name),
                        'keys': str(self.manager.cache.ns.key_count(p[0])[0][0]),
                        'sm': self.manager,
                        'favorite_source': _fav}
                    self.favorites_list.data.append(_ns)

            self.manager.current = 'favorites_screen'
