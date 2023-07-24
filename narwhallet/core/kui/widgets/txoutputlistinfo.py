from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class TXOutputListInfo(BoxLayout):
    n = ObjectProperty(None)
    value = ObjectProperty(None)
    scriptpubkey_asm = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            return
        return super(TXOutputListInfo, self).on_touch_down(touch)
