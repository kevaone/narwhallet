from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.qrcode import QR_Code
import qrcode
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets
from narwhallet.core.kcl.wallet.address import MAddress


class ReceiveScreen(Screen):
    address = ObjectProperty(None)
    amount = ObjectProperty(None)
    label = ObjectProperty(None)
    qr_code = ObjectProperty(None)

    def populate(self, wallet_name):
        self.address.text = ''
        self.amount.text = ''
        # self.address.text = ''
        # self.qr_code = QR_Code()
        _w: MWallet = self.manager.wallets.get_wallet_by_name(wallet_name)
        
        if _w is not None:
            _addr = _w.get_unused_address()
            self.qr_code.data = _addr
            self.address.text = _addr

        self.manager.current = 'receive_screen'