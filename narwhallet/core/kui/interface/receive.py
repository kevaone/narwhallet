from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.qrcode import QR_Code
from narwhallet.core.kcl.wallet import MWallet
from narwhallet.core.kui.widgets.header import Header


class ReceiveScreen(Screen):
    address = Nwlabel()
    label = TextInput()
    qr_code = QR_Code()
    header = Header()

    def populate(self, wallet_name):
        self.app = App.get_running_app()
        self.address.text = ''
        _w: MWallet = self.app.ctrl.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        
        if _w is not None:
            _addr = _w.get_unused_address()
            self.qr_code.data = _addr
            self.address.text = _addr

            self.manager.wallet_screen.btn_addresses.text = 'Addresses (' + str(_w.account_index + _w.change_index) + ')'
        self.manager.current = 'receive_screen'

    def on_enter(self, *args):
        self.label.focus = True

    def save(self):
        _w: MWallet = self.app.ctrl.wallets.get_wallet_by_name(self.header.value)
        _addr = _w.addresses.get_address_by_name(self.address.text)
        _addr.set_label(self.label.text)
        self.app.ctrl.wallets.save_wallet(_w.name)

        self.manager.current = 'wallet_screen'
