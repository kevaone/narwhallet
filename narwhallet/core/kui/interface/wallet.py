from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.control.shared import MShared

class WalletScreen(Screen):
    wallet_name = ObjectProperty(None)
    wallet_balance = ObjectProperty(None)
    wallet_unconfiremd_balance = ObjectProperty(None)
    wallet_locked_balance = ObjectProperty(None)
    wallet_sent = ObjectProperty(None)
    wallet_received = ObjectProperty(None)
    wallet_transaction_count = ObjectProperty(None)
    wallet_unspenttransaction_count = ObjectProperty(None)
    wallet_recent_transactions = ObjectProperty(None)
    btn_addresses = ObjectProperty(None)
    btn_namespaces = ObjectProperty(None)
    last_updated = ObjectProperty(None)

    def populate(self, wallet_name):
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
            self.wallet_name.text = _w.name
            self.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
            self.wallet_balance.text = str(_w.balance)
            _w.last_updated

            _asa = self.manager.cache.ns.get_view()

            for address in _w.addresses.addresses:
                if address is not None:
                    for p in _asa:
                        _oa = self.manager.cache.ns.last_address(p[0])
                        if _oa[0][0] == address.address:
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
            for address in _w.change_addresses.addresses:
                if address is not None:
                    for p in _asa:
                        _oa = self.manager.cache.ns.last_address(p[0])
                        if _oa[0][0] == address.address:
                            _count_namespaces += 1
                    _unconfirmed += address.unconfirmed_balance
                    _sent += address.sent
                    _received += address.received
                    _count_addresses += 1
                    for _h in address.history:
                        _tx[_h['tx_hash']] = _h['height']
                    for _u in address.unspent_tx:
                        _ustx += 1
        for _k, _v in _tx.items():
            _transactions += 1

        self.wallet_unconfirmed_balance.text = str(_unconfirmed)
        self.wallet_sent.text = str(_sent)
        self.wallet_received.text = str(_received)
        self.btn_transactions.text = 'Transactions (' + str(_ustx) + ' / ' + str(_transactions) + ')'
        self.btn_addresses.text = 'Addresses (' + str(_count_addresses) + ')'
        self.btn_namespaces.text = 'Namespaces (' + str(_count_namespaces) + ')'
        self.manager.current = 'wallet_screen'

    def update_wallet(self):
        _update_time = MShared.get_timestamp()