from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets


class RestoreScreen(Screen):
    wallet_name = ObjectProperty(None)
    coin = ObjectProperty(None)
    type = ObjectProperty(None)
    data = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(RestoreScreen, self).__init__(**kwargs)

        self._w = MWallet()

    def set_kind(self):
        if self.data.text.startswith('xprv'):
            self._w.set_bip('bip32')
            self._w.set_extended_prv(self.data.text)
        elif self.data.text.startswith('xpub'):
            self._w.set_bip('bip32')
            self._w.set_extended_pub(self.data.text)
        elif self.data.text.startswith('ypub'):
            self._w.set_bip('bip49')
            self._w.set_kind(1)
            self._w.set_extended_pub(self.data.text)
        elif len(self.data.text
                 .strip().replace('\n', ' ').split(' ')) == 24:
            self._w.set_mnemonic(self.data.text)

    def restore(self):
        _filters = ['\\', '/', '\'', '"', ',', '*',
                    '?', '<', '>', ':', ';', '|']
        for _filter in _filters:
            if _filter in self.wallet_name.text:
                return

        self._w.set_name(self.wallet_name.text)
        self._w.set_coin(self.coin.text)
        self.set_kind()
        if self._w.bip == 'bip49' and self._w.mnemonic != '':
            # TODO Pass password if advanced enabled
            self._w.generate_seed('')
        
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
        self.data.text = ''
