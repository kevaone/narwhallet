from kivy.uix.screenmanager import Screen
from narwhallet.core.kcl.wallet import MWallet
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class CreateScreen(Screen):
    wallet_name = TextInput()
    coin = Spinner()
    # type = ObjectProperty(None)
    mnemonic = TextInput()
    _w = MWallet()
    header = Header()
    btn_create = Nwbutton()

    def __init__(self, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)

    def generate_mnemonic(self):
        self._w.generate_mnemonic()
        self.mnemonic.text = self._w.mnemonic

    def create_wallet(self):
        if self.wallet_name.text == '' or self.mnemonic.text == '':
            return

        self._w.set_coin(self.coin.text)
        # self._w.set_bip(self.wallet_type.text)
        self._w.set_bip('bip49')

        _filters = ['\\', '/', '\'', '"', ',', '*',
                    '?', '<', '>', ':', ';', '|']
        for _filter in _filters:
            if _filter in self.wallet_name.text:
                return

            self._w.set_name(self.wallet_name.text)
        
        if self._w.bip == 'bip49' and self._w.mnemonic != '':
            # TODO Pass password if advanced enabled
            self._w.generate_seed('')

        self.manager.wallets.from_mwallet(self._w)
        self.manager.wallets.save_wallet(self._w.name)

        self.manager.home_screen.populate()
        self.manager.wallet_screen.populate(self._w.name)
        self.reset_screen()
        self.manager.current = 'wallet_screen'

    def populate(self):
        self.reset_screen()
        self.manager.current = 'create_screen'

    def return_home(self):
        self.reset_screen()
        self.manager.current = 'home_screen'

    def reset_screen(self):
        self._w = MWallet()
        self.wallet_name.text = ''
        self.mnemonic.text = ''
        self.btn_create.disabled = True

    def validate_name(self, cb=True):
        if self.wallet_name.text != '':
            _a = True
            if cb is True:
                _a = self.validate_mnemonic(False)

            if _a is True:
                self.btn_create.disabled = False
                return True
        self.btn_create.disabled = True

    def validate_mnemonic(self, cb=True):
        if self.mnemonic.text != '':
            if len(self.mnemonic.text.split(' ')) == 24:
                _a = True
                if cb is True:
                    _a = self.validate_name(False)

                if _a is True:
                    self.btn_create.disabled = False
                    return True
        self.btn_create.disabled = True