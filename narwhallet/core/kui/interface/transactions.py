from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class TransactionsScreen(Screen):
    transaction_list = RecycleView()
    header = Header()

    @staticmethod
    def sort_dict(item):
        return int(item['block'])

    def populate(self, wallet_name):
        self.transaction_list.children[0].rows = 0
        self.transaction_list.data = []
        self.transaction_list.scroll_y = 1
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        _transactions = 0
        _txd = []
        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        _s = ''
                        if 'received' in _h:
                            _s = 'Spend'
                        else:
                            _s = 'Receive'
                        _d = {
                                'transaction': _h['txid'],
                                'block': str(_h['block']),
                                # 'txvalue': str(round(_h['value'], 8)),
                                'txvalue': str(_h['value']),
                                'sm': self.manager,
                                'status': _tr.translate(_s)}
                        self.transaction_list.children[0].rows += 1
                        _txd.append(_d)
                        _transactions += 1

            # Change
            if self.manager.settings_screen.settings.show_change:
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        for _h in address.history:
                            _s = ''
                            if 'received' in _h:
                                _s = 'Spend'
                            else:
                                _s = 'Receive'
                            _d = {
                                'transaction': _h['txid'],
                                'block': str(_h['block']),
                                # 'txvalue': str(round(_h['value'], 8)),
                                'txvalue': str(_h['value']),
                                'sm': self.manager,
                                'status': _tr.translate(_s)}
                            self.transaction_list.children[0].rows += 1
                            _txd.append(_d)
                            _transactions += 1

            _txd.sort(reverse=True, key=self.sort_dict)
            self.transaction_list.data = _txd

        self.manager.current = 'transactions_screen'
