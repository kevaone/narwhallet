from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.qrcode import QR_Code
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header


class AddressBookEntryScreen(Screen):
    address = Nwlabel()
    balance = Nwlabel()
    sent = Nwlabel()
    received = Nwlabel()
    label = Nwlabel()
    coin = Nwlabel()
    qr_code = QR_Code()
    header = Header()

    def populate(self, address):
        _a = self.manager.address_book.get_address_by_name(address)

        if _a is not None:
            self.address.text = address
            self.address_name.text = _a.name
            self.label.text = _a.label
            self.coin.text = _a.coin
            self.balance.text = str(round(_a.received - _a.sent, 8))
            self.sent.text = str(_a.sent)
            self.received.text = str(_a.received)

            self.qr_code.data = self.address.text
            self.manager.current = 'addressbookentry_screen'
