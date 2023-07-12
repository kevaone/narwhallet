from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.qrcode import QR_Code
import qrcode
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets
from narwhallet.core.kcl.wallet.address import MAddress
from narwhallet.core.kui.widgets.header import Header


class ReceiveScreen(Screen):
    address = Nwlabel()
    # amount = ObjectProperty(None)
    label = TextInput()
    qr_code = QR_Code()
    header = Header()

    def populate(self, wallet_name):
        self.address.text = ''
        # self.amount.text = ''
        # self.address.text = ''
        # self.qr_code = QR_Code()
        _w: MWallet = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        
        if _w is not None:
            _addr = _w.get_unused_address()
            self.qr_code.data = _addr
            self.address.text = _addr

            self.manager.wallet_screen.btn_addresses.text = 'Addresses (' + str(_w.account_index + _w.change_index) + ')'
        self.manager.current = 'receive_screen'

    def save(self):
        _w: MWallet = self.manager.wallets.get_wallet_by_name(self.header.value)
        _addr = _w.addresses.get_address_by_name(self.address.text)
        _addr.set_label(self.label.text)
        self.manager.wallets.save_wallet(_w.name)

        self.manager.current = 'wallet_screen'