from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class TransactionListInfo(BoxLayout):
    transaction = ObjectProperty(None)
    block = ObjectProperty(None)
    sm = ObjectProperty(None)
    tl_canvas = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.transaction_screen.populate(self.transaction.text)
            return
        return super(TransactionListInfo, self).on_touch_down(touch)
