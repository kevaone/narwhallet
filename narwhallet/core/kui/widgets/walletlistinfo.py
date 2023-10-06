from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from kivy.graphics import Color


class WalletListInfo(BoxLayout):
    wallet_name = ObjectProperty(None)
    ticker = ObjectProperty(None)
    transactions = ObjectProperty(None)
    addresses = ObjectProperty(None)
    namespaces = ObjectProperty(None)
    balance = ObjectProperty(None)
    last_updated = ObjectProperty(None)
    sm = ObjectProperty(None)
    background_color = ListProperty()
    hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(WalletListInfo, self).__init__(**kwargs)

        # Window.bind(mouse_pos=self.on_mouse_pos)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.wallet_screen._animate_loading_stop()
            self.sm.wallet_screen.populate(self.wallet_name.text)
            return
        return super(WalletListInfo, self).on_touch_down(touch)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(pos[0], pos[1]):
            if self.hover is False:
                self.background_color = [146/255, 149/255, 149/255, 1]
                self.hover = True
        else:
            if self.hover is True:
                self.background_color = [54/255, 58/255, 59/255, 1]
                self.hover = False
