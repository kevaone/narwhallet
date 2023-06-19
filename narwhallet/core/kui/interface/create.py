from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets


class CreateScreen(Screen):
    wallet_name = ObjectProperty(None)
    coin = ObjectProperty(None)
    # type = ObjectProperty(None)
    mnemonic = ObjectProperty(None)
    _w = MWallet()

    def __init__(self, **kwargs):
        super(CreateScreen, self).__init__(**kwargs)

    def generate_mnemonic(self):
        self._w.generate_mnemonic()
        self.mnemonic.text = self._w.mnemonic

    def create_wallet(self):
        # self._w = MWallet()
        self._w.set_coin(self.coin.text)
        # self._w.set_bip(self.wallet_type.text)
        self._w.set_bip('bip49')
        self._w.generate_seed(self._w.mnemonic)

        _filters = ['\\', '/', '\'', '"', ',', '*',
                    '?', '<', '>', ':', ';', '|']
        for _filter in _filters:
            if _filter in self.wallet_name.text:
                
                return

            self._w.set_name(self.wallet_name.text)
        
        self.manager.wallets.from_mwallet(self._w)
        self.manager.wallets.save_wallet(self._w.name)

        self.manager.populate()
        self.manager.populate(self._w.name)
        self.reset_screen()
        self.manager.current = 'wallet_screen'

    def return_home(self):
        self.reset_screen()
        self.manager.current = 'home_screen'

    def reset_screen(self):
        self._w = MWallet()
        self.wallet_name.text = ''
        self.mnemonic.text = ''
