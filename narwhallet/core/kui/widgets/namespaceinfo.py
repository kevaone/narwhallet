from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class NamespaceInfo(BoxLayout):
    key = ObjectProperty(None)
    data = ObjectProperty(None)
    sm = ObjectProperty(None)

    # def on_touch_down(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         # self.sm.populate(self.wallet_name, self.address.text)
    #         # self.sm.address_screen.address.text = self.address.text
    #         # self.sm.address_screen.balance.text = self.balance.text
    #         self.sm.populate(self.address.text)
    #         self.sm.current = 'namespace_key_screen'
    #         # return
    #     return super(NamespaceInfo, self).on_touch_down(touch)
