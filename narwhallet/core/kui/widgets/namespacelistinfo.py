from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class NamespaceListInfo(BoxLayout):
    address = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    owner = ObjectProperty(None)
    keys = ObjectProperty(None)
    wallet_name = ObjectProperty(None)
    sm = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.namespace_screen.populate(self.address.text)
            return
        return super(NamespaceListInfo, self).on_touch_down(touch)
