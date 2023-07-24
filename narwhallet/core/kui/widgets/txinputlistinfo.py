from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class TXInputListInfo(BoxLayout):
    txid = ObjectProperty(None)
    vout = ObjectProperty(None)
    sm = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            return
        return super(TXInputListInfo, self).on_touch_down(touch)
