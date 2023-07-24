from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty


class TransactionListInfo(BoxLayout):
    transaction = StringProperty()
    block = StringProperty()
    sm = ScreenManager()
    status = StringProperty()
    txvalue = StringProperty()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.transaction_screen.populate(self.transaction)
            return
        return super(TransactionListInfo, self).on_touch_down(touch)
