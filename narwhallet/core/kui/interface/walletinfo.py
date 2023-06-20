from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.control.shared import MShared

class WalletInfoScreen(Screen):
    wallet_name = ObjectProperty(None)
    mnemonic_phrase = ObjectProperty(None)
    seed = ObjectProperty(None)
    ypub = ObjectProperty(None)
    coin = ObjectProperty(None)
    kind = ObjectProperty(None)
    account_index = ObjectProperty(None)
    change_index = ObjectProperty(None)
    balance = ObjectProperty(None)
    locked_balance = ObjectProperty(None)
    last_updated = ObjectProperty(None)

    def populate(self, name):
        _w = self.manager.wallets.get_wallet_by_name(name.text)

        if _w is not None:
            # _w.bip
            
            self.wallet_name.text = _w.name
            self.mnemonic_phrase.text = _w.mnemonic
            self.seed.text = _w.seed
            self.ypub.text = '_w.extended_pub'
            self.coin.text = _w.coin
            self.kind.text = _w.kind.name
            self.account_index.text = str(_w.account_index)
            self.change_index.text = str(_w.change_index)
            self.balance.text = str(round(_w.balance, 8)) #str(_w.balance)
            self.locked_balance.text = str(round(_w.locked, 8)) #str(_w.locked)
            self.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
        self.manager.current = 'walletinfo_screen'
