from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.uix.screenmanager import ScreenManager

from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kui.widgets.nwimage import Nwimage


class MarketListInfo(BoxLayout):
    time = StringProperty()
    root_shortcode = StringProperty()
    desc = StringProperty()
    displayName = StringProperty()
    price = StringProperty()
    namespaceid = StringProperty()
    bids = StringProperty()
    high_bid = StringProperty()
    favorite = Nwimage()
    favorite_source = StringProperty()
    
    sm = ScreenManager()

    def on_touch_down(self, touch):
        if self.favorite.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            self.set_favorite()
            return

        if self.collide_point(touch.x, touch.y):
            self.sm.namespacealt_screen.populate(self.namespaceid, self.root_shortcode)
            return
        return super(MarketListInfo, self).on_touch_down(touch)

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
            _a.set_value(self.namespaceid)
            _a.set_filter([])

            self.sm.favorites.favorites[_a.value] = _a
        else:
            self.sm.favorites.remove_favorite(self.namespaceid)

        self.sm.favorites.save_favorites()
