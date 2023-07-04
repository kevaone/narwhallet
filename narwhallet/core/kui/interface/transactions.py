from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class TransactionsScreen(Screen):
    transaction_list = GridLayout()
    header = Header()

    def tx_value(self, txid):
        _asa = self.manager.cache.tx.get_tx_by_txid(txid)
        _value = 0.0
        if _asa is not None:
            for o in _asa.vout:
                _value += o.value
                # _o.value.text = str(round(o.value, 8)) #str(o.value)
        return _value

    def populate(self, wallet_name):
        self.transaction_list.clear_widgets()
        self.transaction_list.parent.scroll_y = 1
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        _transactions = 0
        _ustx = 0
        self.transaction_list.rows = 0

        _tx = {}
        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        # TODO Check if tx_hash already present then fix the items below
                        _t = TransactionListInfo()
                        _t.transaction.text = _h['tx_hash']
                        _t.block.text = str(_h['height'])
                        # TODO Fix
                        _t.txvalue.text = str(round(self.tx_value(_h['tx_hash']), 8))
                        _t.sm = self.manager
                        _t.status.text = 'Spent'
                        _tx[_h['tx_hash']] = _t
                    for _u in address.unspent_tx:
                        if _u['tx_hash'] in list(_tx.keys()):
                            _tx[_u['tx_hash']].status.text = 'Partial Spend'
                            # TODO Include in above correction
                            _tx[_u['tx_hash']].txvalue.text = str(round(_u['value']/10000000, 8))
                        else:
                            _t = TransactionListInfo()
                            _t.transaction.text = _u['tx_hash']
                            _t.block.text = str(_u['height'])
                            # TODO Include in above correction
                            _t.txvalue.text = str(round(_u['value']/10000000, 8))
                            _t.sm = self.manager
                            _t.status.text = 'Unspent'
                            _tx[_u['tx_hash']] = _t
                        _ustx += 1
            # Change
            for address in _w.change_addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        # TODO Check if tx_hash already present then fix the items below
                        _t = TransactionListInfo()
                        _t.transaction.text = _h['tx_hash']
                        _t.block.text = str(_h['height'])
                        # TODO Fix
                        _t.txvalue.text = str(round(self.tx_value(_h['tx_hash']), 8))
                        _t.sm = self.manager
                        _t.status.text = 'Spent'
                        _tx[_h['tx_hash']] = _t
                    for _u in address.unspent_tx:
                        if _u['tx_hash'] in list(_tx.keys()):
                            _tx[_u['tx_hash']].status.text = 'Partial Spend'
                            # TODO Include in above correction
                            _tx[_u['tx_hash']].txvalue.text = str(round(_u['value']/10000000, 8))
                        else:
                            _t = TransactionListInfo()
                            _t.transaction.text = _u['tx_hash']
                            _t.block.text = str(_u['height'])
                            # TODO Include in above correction
                            _t.txvalue.text = str(round(_u['value']/10000000, 8))
                            _t.sm = self.manager
                            _t.status.text = 'Unspent'
                            _tx[_u['tx_hash']] = _t
                        _ustx += 1
            for _k, _v in _tx.items():
                self.transaction_list.rows += 1
                # self.transaction_list.rows_minimum[self.transaction_list.rows] = 65
                self.transaction_list.add_widget(_v)
                _transactions += 1

        self.manager.current = 'transactions_screen'
