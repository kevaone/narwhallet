from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import Nwlabel
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class PsbtListInfo(BoxLayout):
    key_name = Nwlabel()
    key_data = Nwlabel()
    value_data = Nwlabel()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            return
        return super(PsbtListInfo, self).on_touch_down(touch)
