from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from kivy.properties import StringProperty


class AddressBookListInfo(BoxLayout):
    address = StringProperty()
    address_label = StringProperty()
    address_name = StringProperty()
    coin = StringProperty()
    sent = StringProperty()
    received = StringProperty()
    sm = ScreenManager()

    def __init__(self, **kwargs):
        super(AddressBookListInfo, self).__init__(**kwargs)

        self.mode = 0

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.mode == 0:
                self.sm.addressbookentry_screen.populate(self.address)
            elif self.mode == 1:
                self.sm.send_screen.send_to.text = self.address
                self.sm.current = 'send_screen'
            elif self.mode == 2:
                self.sm.transfernamespace_screen.new_namespace_address.text = self.address
                self.sm.current = 'transfernamespace_screen'
            elif self.mode == 3:
                self.sm.auctionnamespace_screen.payment_address.text = self.address
                self.sm.current = 'auctionnamespace_screen'
            return
        return super(AddressBookListInfo, self).on_touch_down(touch)
