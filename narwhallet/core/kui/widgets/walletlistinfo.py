from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, StringProperty
from kivy.graphics import Color


class WalletListInfo(BoxLayout):
    wallet_name = StringProperty('')
    ticker = ObjectProperty(None)
    lock_state = ObjectProperty(None)
    lock_icon = StringProperty('')
    transactions = ObjectProperty(None)
    addresses = ObjectProperty(None)
    namespaces = ObjectProperty(None)
    balance = StringProperty('')
    last_updated = StringProperty('')
    sm = ObjectProperty(None)
    mouse_hover = BooleanProperty(False)
    background_color = ListProperty([25/255, 27/255, 27/255, 1])
    hover_color = ListProperty([136/255, 136/255, 136/255, 1])

    def __init__(self, **kwargs):
        super(WalletListInfo, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.lock_state.collide_point(touch.x, touch.y):
            app = App.get_running_app()
            app.wallet_lock(self.wallet_name, self)
            return

        if self.collide_point(touch.x, touch.y):
            self.sm.wallet_screen._animate_loading_stop()
            self.sm.wallet_screen.populate(self.wallet_name)
            return
        return super(WalletListInfo, self).on_touch_down(touch)
