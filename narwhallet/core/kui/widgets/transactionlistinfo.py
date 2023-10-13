from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, ListProperty, BooleanProperty


class TransactionListInfo(BoxLayout):
    transaction = StringProperty()
    block = StringProperty()
    sm = ScreenManager()
    status = StringProperty()
    txvalue = StringProperty()
    mouse_hover = BooleanProperty(False)
    background_color = ListProperty([25/255, 27/255, 27/255, 1])
    hover_color = ListProperty([136/255, 136/255, 136/255, 1])

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.transaction_screen.populate(self.transaction)
            return
        return super(TransactionListInfo, self).on_touch_down(touch)
