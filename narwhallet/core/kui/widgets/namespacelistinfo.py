from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.uix.screenmanager import ScreenManager


class NamespaceListInfo(BoxLayout):
    address = StringProperty()
    shortcode = StringProperty()
    owner = StringProperty()
    keys = StringProperty()
    wallet_name = StringProperty()
    sm = ScreenManager()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.namespace_screen.populate(self.address)
            return
        return super(NamespaceListInfo, self).on_touch_down(touch)
