from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kui.widgets.nwlabel import Nwlabel

class AddressBookListInfo(BoxLayout):
    address = Nwlabel()
    address_label = Nwlabel()
    address_name = Nwlabel()
    coin = Nwlabel()
    balance = Nwlabel()
    sent = Nwlabel()
    received = Nwlabel()
    sm = ScreenManager()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.sm.addressbookentry_screen.populate(self.address.text)
            return
        return super(AddressBookListInfo, self).on_touch_down(touch)
