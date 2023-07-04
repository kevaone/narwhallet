from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class TransactionListInfo(BoxLayout):
    transaction = Nwlabel()
    block = Nwlabel()
    sm = ScreenManager()
    status = Nwlabel()
    txvalue = Nwlabel()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.transaction_screen.populate(self.transaction.text)
            return
        return super(TransactionListInfo, self).on_touch_down(touch)
