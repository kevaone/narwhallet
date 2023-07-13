from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class TransactionsScreen(Screen):
    transaction_list = RecycleView()
    header = Header()

    def tx_value(self, txid):
        _asa = self.manager.cache.tx.get_tx_by_txid(txid)
        _value = 0.0
        if _asa is not None:
            for o in _asa.vout:
                _value += o.value
        return _value

    def populate(self, wallet_name):
        self.transaction_list.children[0].rows = 0
        self.transaction_list.data = []
        self.transaction_list.scroll_y = 1
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        _transactions = 0
        _ustx = 0

        _tx = {}
        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        _d = {
                                'transaction': _h['tx_hash'],
                                'block': str(_h['height']),
                                'txvalue': str(round(self.tx_value(_h['tx_hash']), 8)),
                                'sm': self.manager,
                                'status': 'Spent'}
                        _tx[_h['tx_hash']] = _d
                    for _u in address.unspent_tx:
                        if _u['tx_hash'] in list(_tx.keys()):
                            _tx[_u['tx_hash']]['status'] = 'Partial Spend'
                            # TODO Include in above correction
                            _tx[_u['tx_hash']]['txvalue'] = str(round(_u['value']/10000000, 8))
                        else:
                            _d = {
                                'transaction': _h['tx_hash'],
                                'block': str(_h['height']),
                                'txvalue': str(round(self.tx_value(_h['tx_hash']), 8)),
                                'sm': self.manager,
                                'status': 'Unspent'}
                            _tx[_u['tx_hash']] = _d
                        _ustx += 1

            # Change
            if self.manager.settings_screen.settings.show_change:
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        for _h in address.history:
                            _d = {
                                'transaction': _h['tx_hash'],
                                'block': str(_h['height']),
                                'txvalue': str(round(self.tx_value(_h['tx_hash']), 8)),
                                'sm': self.manager,
                                'status': 'Spent'}
                            _tx[_h['tx_hash']] = _d
                        for _u in address.unspent_tx:
                            if _u['tx_hash'] in list(_tx.keys()):
                                _tx[_u['tx_hash']]['status'] = 'Partial Spend'
                                # TODO Include in above correction
                                _tx[_u['tx_hash']]['txvalue'] = str(round(_u['value']/10000000, 8))
                            else:
                                _d = {
                                'transaction': _h['tx_hash'],
                                'block': str(_h['height']),
                                'txvalue': str(round(self.tx_value(_h['tx_hash']), 8)),
                                'sm': self.manager,
                                'status': 'Unspent'}
                                _tx[_u['tx_hash']] = _d
                            _ustx += 1

            _txd = []

            for _k, _v in _tx.items():
                self.transaction_list.children[0].rows += 1
                _txd.append(_v)
                _transactions += 1

            self.transaction_list.data = _txd

        self.manager.current = 'transactions_screen'
