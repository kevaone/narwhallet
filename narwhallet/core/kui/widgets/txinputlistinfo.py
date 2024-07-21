from kivy.uix.boxlayout import BoxLayout
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class TXInputListInfo(BoxLayout):
    txid = Nwlabel()
    vout = Nwlabel()
    sequence = Nwlabel()
    scriptsig = Nwlabel()
    sm = Nwlabel()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            return
        return super(TXInputListInfo, self).on_touch_down(touch)
