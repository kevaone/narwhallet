from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kui.widgets.nwimage import Nwimage


class AllListInfo(BoxLayout):
    address = StringProperty()
    shortcode = StringProperty()
    owner = StringProperty()
    keys = StringProperty()
    wallet_name = StringProperty()
    favorite = Nwimage()
    favorite_source = StringProperty()
    ns_name = StringProperty()
    sm = ScreenManager()

    def on_touch_down(self, touch):
        if self.favorite.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            self.set_favorite()
            return

        if self.collide_point(touch.x, touch.y):
            self.sm.alldetail_screen.populate(self.address)
            return
        return super(AllListInfo, self).on_touch_down(touch)

    def set_favorite(self):
        _add_fav = False
        if self.favorite_source == 'narwhallet/core/kui/assets/star_dark.png':
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'
            _add_fav = True
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'

        if _add_fav:
            # TODO Validate inputs
            _a = MFavorite()
            # TODO Make more dynamic once more favorite types come into play
            _a.set_coin('KEVACOIN')
            _a.set_kind('Namespace')
            _a.set_value(self.address)
            _a.set_filter([])

            self.sm.favorites.favorites[_a.value] = _a
        else:
            self.sm.favorites.remove_favorite(self.address)

        self.sm.favorites.save_favorites()
