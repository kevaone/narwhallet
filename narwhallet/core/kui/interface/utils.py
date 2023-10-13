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
    # file = Nwlabel()
    message = TextInput()
    signature = TextInput()
    valid_sig = Nwlabel()
    # s_msg = Nwtogglebutton()
    # s_file = Nwtogglebutton()
    _w = MWallet()
    header = Header()

    def __init__(self, **kwargs):
        super(UtilsScreen, self).__init__(**kwargs)

        pass

    def populate(self):
        self.reset_screen()
        self.wallet_name.values = []
        for _w in self.manager.wallets.wallets:
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
        # self.file.text = ''
        self.address.text = ''
        self.wallet_name.text = ''
        # self.s_msg.state = 'down'
        # self.s_file.state = 'normal'

    def sign_wallet_changed(self):
        self.signature.text = ''
        self.pubk.text = ''
        self.address.text = ''
        self.address.values = []
        _v = []
        
        if self.wallet_name.text != '-':
            self._w = self.manager.wallets.get_wallet_by_name(self.wallet_name.text)
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

        # if _w.kind == 2:
        #     _ul = self.dialogs.lockbox_dialog(0)
        #     # TODO Test selected address can be derived using pass
        #     return False

        # if self.s_msg.state == 'down':

        _signature = self._w.sign_message(_idx,
                                     self.message.text,
                                     _ch)
        # elif self.s_file.state == 'down':
        #     _data = self.file.text
        #     _dat = Ut.sha256(MShared.load_message_file(_data)).decode()
        #     _signature = self._w.sign_message(_idx, _dat, _ch)

        self.signature.text = _signature

        return True

    def verify_message(self):
        self.valid_sig.text = ''
        _v = ''
        # if self.s_msg.state == 'down':
        _v = WalletUtils.verify_message(self.signature.text,
                                        self.pubk.text,
                                            self.message.text)
        # elif self.s_file.state == 'down':
        #     _data = self.file.text
        #     _dat = Ut.sha256(MShared.load_message_file(_data))
        #     _v = WalletUtils.verify_message(self.signature.text,
        #                                     self.pubk.text,
        #                                     _dat)

        self.valid_sig.text = _v
