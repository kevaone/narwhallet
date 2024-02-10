from kivy.app import App
from functools import partial
import json
from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwaddfavorite import Nwaddfavorite
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class FavoritesScreen(Screen):
    favorites_list = Nwgrid()
    header = Header()

    def __init__(self, **kwargs):
        super(FavoritesScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self, *args):
        self.header.value = 'Favorites'
        self.favorites_list.data = []

        for favorite in self.manager.favorites.favorites:
            _f = self.manager.favorites.get_favorite_by_id(favorite)

            if isinstance(_f.value, str):
                _ns = MShared.get_namespace(favorite, self.app.ctrl.kex)
                _ns = _ns['result']

                try:
                    _name = json.loads(_ns['name'])['displayName']
                except:
                    _name = _ns['name']

                _favorite = favorite
                _shortcode = _ns['root_shortcode']
                _keys = len(_ns['data'])
            else:
                _favorite = _f.value[0]
                _shortcode = _f.value[1]
                _name = _f.value[2]
                _keys = _f.value[3]

            _fav = 'narwhallet/core/kui/assets/star_dark.png'
            _ns = {
                'address': _favorite,
                'shortcode': _shortcode,
                'ns_name': str(_name),
                'keys': str(_keys),
                'sm': self.manager,
                'favorite_source': _fav}
            self.favorites_list.data.append(_ns)

        self.manager.current = 'favorites_screen'

    def add_favorite(self):
        addfav_popup = Nwaddfavorite()
        addfav_popup.sm = self.manager
        addfav_popup.namespace.text = ''
        addfav_popup.bind(next=partial(self.populate))
        addfav_popup.open()
