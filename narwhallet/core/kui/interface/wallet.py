import os
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.loadingspinner import LoadingSpinner
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from kivy.clock import Clock
import threading
from narwhallet.core.kui.widgets.header import Header


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

    def populate(self, wallet_name, cache=None):
        if cache is None:
            cache_path = os.path.join(self.manager.user_path, 'narwhallet_cache.db')
            cache = MCache(cache_path)
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        _unconfirmed = 0.0
        _sent = 0.0
        _received = 0.0
        _transactions = 0
        _ustx = 0
        _count_addresses = 0
        _count_namespaces = 0
        _tx = {}

        if _w is not None:
            if _w.kind == EWalletKind.NORMAL:
                self.btn_send.disabled = False
                self.btn_receive.disabled = False
            else:
                self.btn_send.disabled = True
                self.btn_receive.disabled = True

            # TODO create owner view
            _asa = cache.ns.get_view()
            owner_list = []

            for p in _asa:
                _oa = cache.ns.last_address(p[0])
                owner_list.append(_oa[0][0])

            for address in _w.addresses.addresses:
                if address is not None:
                    if address.address in owner_list:
                        _count_namespaces += 1
                    _unconfirmed += address.unconfirmed_balance
                    _sent += address.sent
                    _received += address.received
                    _count_addresses += 1

                    for _h in address.history:
                        _tx[_h['tx_hash']] = _h['height']

                    for _u in address.unspent_tx:
                        _ustx += 1
            # Change
            if self.manager.settings_screen.settings.show_change:
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        if address.address in owner_list:
                            _count_namespaces += 1
                        _unconfirmed += address.unconfirmed_balance
                        _sent += address.sent
                        _received += address.received
                        _count_addresses += 1

                        for _h in address.history:
                            _tx[_h['tx_hash']] = _h['height']

                        for _u in address.unspent_tx:
                            _ustx += 1

            # self.wallet_name.text = _w.name
            self.header.value = _w.name
            self.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
            self.wallet_balance.text = str(round(_w.balance, 8))

        for _k, _v in _tx.items():
            _transactions += 1

        self.wallet_unconfirmed_balance.text = str(round(_unconfirmed, 8))
        self.wallet_sent.text = str(round(_sent, 8))
        self.wallet_received.text = str(round(_received, 8))
        self.btn_transactions.text = 'Transactions (' + str(_ustx) + ' / ' + str(_transactions) + ')'
        self.btn_addresses.text = 'Addresses (' + str(_count_addresses) + ')'
        self.btn_namespaces.text = 'Namespaces (' + str(_count_namespaces) + ')'
        self.manager.current = 'wallet_screen'

        return True

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
        cache_path = os.path.join(self.manager.user_path, 'narwhallet_cache.db')
        cache = MCache(cache_path)
        wallet: MWallet = self.manager.wallets.get_wallet_by_name(self.header.value)

        if wallet is None:
            return False

        wallet.set_bid_balance(0.0)
        wallet.set_bid_tx([])
        MShared.get_histories(wallet, self.manager.kex)
        MShared.get_balances(wallet, self.manager.kex)
        MShared.list_unspents(wallet, self.manager.kex)
        MShared.get_transactions(wallet, self.manager.kex, cache)
        _update_time = MShared.get_timestamp()
        wallet.set_last_updated(_update_time[0])
        self.manager.wallets.save_wallet(wallet.name)
        
        self.populate(wallet.name, cache)
        Clock.schedule_once(self._animate_loading_stop, 0)

        return True
