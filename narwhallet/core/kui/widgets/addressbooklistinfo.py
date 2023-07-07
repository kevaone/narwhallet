from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kui.widgets.nwlabel import Nwlabel

class AddressBookListInfo(BoxLayout):
    address = Nwlabel()
    address_label = Nwlabel()
    address_name = Nwlabel()
    coin = Nwlabel()
    sent = Nwlabel()
    received = Nwlabel()
    sm = ScreenManager()

    def __init__(self, **kwargs):
        super(AddressBookListInfo, self).__init__(**kwargs)

        self.mode = 0

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.mode == 0:
                self.sm.addressbookentry_screen.populate(self.address.text)
            elif self.mode == 1:
                self.sm.send_screen.send_to.text = self.address.text
                self.sm.current = 'send_screen'
            elif self.mode == 2:
                self.sm.transfernamespace_screen.new_namespace_address.text = self.address.text
                self.sm.current = 'transfernamespace_screen'
            return
        return super(AddressBookListInfo, self).on_touch_down(touch)
