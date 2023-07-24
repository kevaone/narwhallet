from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class WalletListInfo(BoxLayout):
    wallet_name = ObjectProperty(None)
    ticker = ObjectProperty(None)
    transactions = ObjectProperty(None)
    addresses = ObjectProperty(None)
    namespaces = ObjectProperty(None)
    balance = ObjectProperty(None)
    last_updated = ObjectProperty(None)
    sm = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.wallet_screen._animate_loading_stop()
            self.sm.wallet_screen.populate(self.wallet_name.text)
            return
        return super(WalletListInfo, self).on_touch_down(touch)
