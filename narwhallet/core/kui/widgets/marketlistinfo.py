from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kui.widgets.nwimage import Nwimage
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwmarketimage import Nwmarketimage


class MarketListInfo(BoxLayout):
    time = StringProperty()
    root_shortcode = StringProperty()
    keys = StringProperty(None)
    desc = StringProperty()
    desc_box = BoxLayout()
    displayName = StringProperty()
    price = StringProperty()
    namespaceid = StringProperty()
    bids = StringProperty()
    high_bid = StringProperty()
    favorite = Nwimage()
    favorite_source = StringProperty()
    mouse_hover = BooleanProperty(False)
    background_color = ListProperty([25/255, 27/255, 27/255, 1])
    hover_color = ListProperty([136/255, 136/255, 136/255, 1])
    image_path = StringProperty()
    media_size = NumericProperty()
    y_size = NumericProperty()
    sm = ScreenManager()

    def on_image_path(self, *args):
        if self.image_path != '':
            self.height = self.y_size + dp(150)
            self.media_size = dp(150)
        else:
            self.height = self.y_size
            self.media_size = dp(0)

    def get_text_height(self, text, text_width):
        _label = Nwlabel()
        _label.font_size = dp(15)
        _label.width = text_width
        _label.text_size = (text_width, None)
        _label.size_hint = (1, None)
        _label.padding = [5, 0, 0, 0]
        _label.text = text
        _label.texture_update()

        text_height = _label.texture_size[1]
        self.desc_box.height = text_height
        self.height = dp(90) + text_height
        self.y_size = self.height

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
        if self.favorite_source == 'narwhallet/core/kui/assets/star.png':
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
            _add_fav = True
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        if _add_fav:
            # TODO Validate inputs
            _a = MFavorite()
            # TODO Make more dynamic once more favorite types come into play
            _a.set_id(self.namespaceid)
            _a.set_coin('KEVACOIN')
            _a.set_kind('Namespace')
            _a.set_value([self.namespaceid, self.root_shortcode, self.displayName, self.keys])
            _a.set_filter([])

            self.sm.favorites.favorites[_a.id] = _a
        else:
            self.sm.favorites.remove_favorite(self.namespaceid)

        self.sm.favorites.save_favorites()
