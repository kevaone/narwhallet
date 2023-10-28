from kivy.uix.screenmanager import Screen
from narwhallet.core.kcl.wallet import MWallet
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header


class WalletInfoScreen(Screen):
    wallet_name = Nwlabel()
    mnemonic_phrase = Nwlabel()
    seed = Nwlabel()
    ypub = Nwlabel()
    xpriv = Nwlabel()
    coin = Nwlabel()
    bip = Nwlabel()
    kind = Nwlabel()
    account_index = Nwlabel()
    change_index = Nwlabel()
    balance = Nwlabel()
    locked_balance = Nwlabel()
    last_updated = Nwlabel()
    header = Header()

    def populate(self, name):
        _w: MWallet = self.manager.wallets.get_wallet_by_name(name)

        if _w is not None:
            self.header.value = _w.name
            self.mnemonic_phrase.text = _w.mnemonic
            self.seed.text = _w.seed
            self.ypub.text = _w.extended_pub
            self.xpriv.text = _w.extended_prv
            self.coin.text = _w.coin
            self.bip.text = _w.bip
            self.kind.text = _w.kind.name
            self.account_index.text = str(_w.account_index)
            self.change_index.text = str(_w.change_index)
            self.balance.text = str(round(_w.balance, 8))
            self.locked_balance.text = str(round(_w.locked, 8))
            self.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
        self.manager.current = 'walletinfo_screen'

    def clear_screen(self):
        self.wallet_name.text = ''
        self.mnemonic_phrase.text = ''
        self.seed.text = ''
        self.ypub.text = ''
        self.xpriv.text = ''
        self.coin.text = ''
        self.bip.text = ''
        self.kind.text = ''
        self.account_index.text = ''
        self.change_index.text = ''
        self.balance.text = ''
        self.locked_balance.text = ''
        self.last_updated.text = ''
        self.manager.current = 'wallet_screen'
