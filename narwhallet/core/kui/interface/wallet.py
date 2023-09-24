from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.wallet import MWallet
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.loadingspinner import LoadingSpinner
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from kivy.clock import Clock
import threading
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class WalletScreen(Screen):
    # wallet_name = ObjectProperty(None)
    header = Header()
    wallet_balance = Nwlabel()
    wallet_unconfirmed_balance = Nwlabel()
    wallet_locked_balance = Nwlabel()
    wallet_sent = Nwlabel()
    wallet_received = Nwlabel()
    wallet_transaction_count = Nwlabel()
    wallet_unspenttransaction_count = Nwlabel()
    wallet_recent_transactions = Nwlabel()
    btn_addresses = Nwbutton()
    btn_namespaces = Nwbutton()
    btn_transactions = Nwbutton()
    btn_send = Nwbutton()
    btn_receive = Nwbutton()
    last_updated = Nwlabel()
    btn_update_wallet = LoadingSpinner()

    def __init__(self, **kwargs):
        super(WalletScreen, self).__init__(**kwargs)

        self.anim = Animation(angle = 360, duration=2) 
        self.anim += Animation(angle = 0, duration=0.01)
        self.anim.repeat = True

    def populate(self, wallet_name):
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)

        if _w is not None:
            if _w.kind == EWalletKind.NORMAL:
                self.btn_send.disabled = False
                self.btn_receive.disabled = False
            else:
                self.btn_send.disabled = True
                self.btn_receive.disabled = True

            self.header.value = _w.name
            self.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
            self.wallet_balance.text = str(round(_w.balance, 8))

            # self.wallet_unconfirmed_balance.text = str(round(_w.unconfirmed, 8))
            # self.wallet_sent.text = str(round(_w.sent, 8))
            # self.wallet_received.text = str(round(_w.received, 8))
            self.wallet_unconfirmed_balance.text = str(_w.unconfirmed_balance)
            self.wallet_sent.text = str(_w.sent)
            self.wallet_received.text = str(_w.received)
            self.btn_transactions.text = _tr.translate('History') + ' (' + str(len(_w.unspent_tx)) + ' / ' + str(len(_w.history)) + ')'
            self.btn_addresses.text = _tr.translate('Addresses') + ' (' + str(len(_w.addresses.addresses) + len(_w.change_addresses.addresses)) + ')'
            self.btn_namespaces.text = _tr.translate('Namespaces') + ' (' + str(len(_w.namespaces)) + ')'
            self.manager.current = 'wallet_screen'


    def _animate_loading_start(self, dt=None):
        self.anim.start(self.btn_update_wallet)
        self.btn_update_wallet.rotating = True

    def _animate_loading_stop(self, dt=None):
        self.anim.stop(self.btn_update_wallet)
        self.btn_update_wallet.rotating = False

    def update_wallet(self):
        Clock.schedule_once(self._animate_loading_start, -1)
        threading.Thread(target=self._update_wallet).start()

    def _update_wallet(self, dt=None):
        wallet: MWallet = self.manager.wallets.get_wallet_by_name(self.header.value)

        if wallet is None:
            return False

        wallet.set_bid_balance(0.0)
        wallet.set_bid_tx([])
        MShared.get_addresses(wallet, self.manager.kex)
        # MShared.get_histories(wallet, self.manager.kex)
        # MShared.get_balances(wallet, self.manager.kex)
        # MShared.list_unspents(wallet, self.manager.kex)
        # _provider = self.manager.settings_screen.settings.content_providers[0]
        # MShared.get_transactions(wallet, self.manager.kex, cache, _provider)
        _update_time = MShared.get_timestamp()
        wallet.set_last_updated(_update_time[0])
        self.manager.wallets.save_wallet(wallet.name)
        
        self.populate(wallet.name)
        Clock.schedule_once(self._animate_loading_stop, 0)

        return True
