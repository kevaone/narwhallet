from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, ListProperty, BooleanProperty


class AddressListInfo(BoxLayout):
    index = StringProperty()
    address = StringProperty()
    address_label = StringProperty()
    transactions = StringProperty()
    balance = StringProperty()
    last_updated = StringProperty()
    wallet_name = StringProperty()
    sm = ScreenManager()
    mouse_hover = BooleanProperty(False)
    background_color = ListProperty([25/255, 27/255, 27/255, 1])
    hover_color = ListProperty([136/255, 136/255, 136/255, 1])

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.address_screen.populate(self.wallet_name, self.address)
            return
        return super(AddressListInfo, self).on_touch_down(touch)
