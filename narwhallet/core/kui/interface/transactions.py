from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo


class TransactionsScreen(Screen):
    transaction_list = ObjectProperty(None)

    def populate(self, wallet_name):
        self.transaction_list.clear_widgets()
        self.transaction_list.parent.scroll_y = 1
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        _transactions = 0
        _ustx = 0
        self.transaction_list.rows = 0

        _tx = {}
        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        _t = TransactionListInfo()
                        _t.transaction.text = _h['tx_hash']
                        _t.block.text = str(_h['height'])
                        _t.sm = self.manager
                        _tx[_h['tx_hash']] = _t
                    for _u in address.unspent_tx:
                        _ustx += 1
            # Change
            for address in _w.change_addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        _t = TransactionListInfo()
                        _t.transaction.text = _h['tx_hash']
                        _t.block.text = str(_h['height'])
                        _t.sm = self.manager
                        _tx[_h['tx_hash']] = _t
                    for _u in address.unspent_tx:
                        _ustx += 1
            for _k, _v in _tx.items():
                self.transaction_list.rows += 1
                # self.transaction_list.rows_minimum[self.transaction_list.rows] = 65
                self.transaction_list.add_widget(_v)
                _transactions += 1

        self.manager.current = 'transactions_screen'
