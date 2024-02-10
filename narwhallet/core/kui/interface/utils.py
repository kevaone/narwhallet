from kivy.app import App
from kivy.uix.screenmanager import Screen
from narwhallet.core.kcl.wallet import MWallet
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kcl.wallet_utils import _wallet_utils as WalletUtils


class UtilsScreen(Screen):
    wallet_name = Spinner()
    address = Spinner()
    pubk = TextInput()
    message = TextInput()
    signature = TextInput()
    valid_sig = Nwlabel()
    _w = MWallet()
    header = Header()

    def __init__(self, **kwargs):
        super(UtilsScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self):
        self.reset_screen()
        self.wallet_name.values = []
        for _w in self.app.ctrl.wallets.wallets:
            if _w.kind == EWalletKind.NORMAL:
                self.wallet_name.values.append(_w.name)
        self.manager.current = 'utils_screen'

    def return_home(self):
        self.reset_screen()
        self.manager.current = 'home_screen'

    def reset_screen(self):
        self.signature.text = ''
        self.pubk.text = ''
        self.address.values = []
        self.message.text = ''
        self.address.text = ''
        self.wallet_name.text = ''

    def sign_wallet_changed(self):
        self.signature.text = ''
        self.pubk.text = ''
        self.address.text = ''
        self.address.values = []
        _v = []
        
        if self.wallet_name.text != '-':
            self._w = self.app.ctrl.wallets.get_wallet_by_name(self.wallet_name.text)
            if self._w is not None:
                for index in range(0, self._w.addresses.count):
                    _addr = self._w.addresses.get_address_by_index(index)
                    _v.append(_addr.address)

                for index in range(0, self._w.change_addresses.count):
                    _addr = self._w.change_addresses.get_address_by_index(index)
                    _v.append(_addr.address)

        self.address.values = _v

    def sign_address_changed(self):
        self.signature.text = ''
        if self.address.text not in ('', '-'):
            _idx = self._w.addresses.get_address_index_by_name(self.address.text)
            _ch = 0
            if _idx == -1:
                _idx = self._w.change_addresses.get_address_index_by_name(self.address.text)
                _ch = 1

            _pub = self._w.get_publickey_raw(_idx, _ch)
            self.pubk.text = _pub
        else:
            self.pubk.text = ''

    def sign_message(self):
        self.signature.text = ''
        _signature = ''
        _idx = self._w.addresses.get_address_index_by_name(self.address.text)
        _ch = 0
        if _idx == -1:
            _idx = self._w.change_addresses.get_address_index_by_name(self.address.text)
            _ch = 1

        if _idx == -1:
            return False

        _signature = self._w.sign_message(_idx,
                                     self.message.text,
                                     _ch)

        self.signature.text = _signature

        return True

    def verify_message(self):
        self.valid_sig.text = ''
        _v = ''
        _v = WalletUtils.verify_message(self.signature.text,
                                        self.pubk.text,
                                            self.message.text)

        self.valid_sig.text = _v
