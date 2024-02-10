from kivy.app import App
from kivy.uix.screenmanager import Screen
from narwhallet.core.kcl.bip_utils.bip39.bip39_mnemonic import Bip39Languages
from narwhallet.core.kcl.wallet import MWallet
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class CreateScreen(Screen):
    wallet_name = TextInput()
    coin = Spinner()
    mnemonic_lang = Spinner()
    mnemonic = TextInput()
    _w = MWallet()
    header = Header()
    btn_create = Nwbutton()

    def __init__(self, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def get_mnemonic_lang(self):
        _lang = self.mnemonic_lang.text
        if _lang == self.app.translate_text('ENGLISH'):
            return Bip39Languages.ENGLISH
        elif _lang == self.app.translate_text('ITALIAN'):
            return Bip39Languages.ITALIAN
        elif _lang == self.app.translate_text('FRENCH'):
            return Bip39Languages.FRENCH
        elif _lang == self.app.translate_text('SPANISH'):
            return Bip39Languages.SPANISH
        elif _lang == self.app.translate_text('PORTUGUESE'):
            return Bip39Languages.PORTUGUESE
        elif _lang == self.app.translate_text('CZECH'):
            return Bip39Languages.CZECH
        elif _lang == self.app.translate_text('CHINESE_SIMPLIFIED'):
            return Bip39Languages.CHINESE_SIMPLIFIED
        elif _lang == self.app.translate_text('CHINESE_TRADITIONAL'):
            return Bip39Languages.CHINESE_TRADITIONAL
        elif _lang == self.app.translate_text('KOREAN'):
            return Bip39Languages.KOREAN

        return Bip39Languages.ENGLISH

    def generate_mnemonic(self):
        self._w.generate_mnemonic(self.get_mnemonic_lang())
        self.mnemonic.text = self._w.mnemonic

    def create_wallet(self):
        if self.wallet_name.text == '' or self.mnemonic.text == '':
            return

        self._w.set_coin(self.coin.text)
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

        self.app.ctrl.wallets.from_mwallet(self._w)
        self.app.ctrl.wallets.save_wallet(self._w.name)

        self.manager.home_screen.populate()
        self.manager.wallet_screen.populate(self._w.name)
        self.reset_screen()
        self.manager.current = 'wallet_screen'

    def populate(self):
        self.reset_screen()

        self.mnemonic_lang.values = [self.app.translate_text('ENGLISH'),
            self.app.translate_text('ITALIAN'),
            self.app.translate_text('FRENCH'),
            self.app.translate_text('SPANISH'),
            self.app.translate_text('PORTUGUESE'),
            self.app.translate_text('CZECH'),
            self.app.translate_text('CHINESE_SIMPLIFIED'),
            self.app.translate_text('CHINESE_TRADITIONAL'),
            self.app.translate_text('KOREAN')]
        self.manager.current = 'create_screen'

    def on_enter(self, *args):
        self.wallet_name.focus = True

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
