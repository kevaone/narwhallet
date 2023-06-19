from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class AddressListInfo(BoxLayout):
    address = ObjectProperty(None)
    address_label = ObjectProperty(None)
    transactions = ObjectProperty(None)
    balance = ObjectProperty(None)
    last_updated = ObjectProperty(None)
    wallet_name = ObjectProperty(None)
    sm = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.address_screen.populate(self.wallet_name.text, self.address.text)
            return
        return super(AddressListInfo, self).on_touch_down(touch)
