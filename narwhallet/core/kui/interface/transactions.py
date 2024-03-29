from kivy.app import App
from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.ksc.utils import Ut


class TransactionsScreen(Screen):
    transaction_list = Nwgrid()
    header = Header()

    def __init__(self, **kwargs):
        super(TransactionsScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    @staticmethod
    def sort_dict(item):
        if item['block'] == 'unconfirmed':
            return 100000000

        return int(item['block'])

    def populate(self, wallet_name):
        self.transaction_list.children[0].rows = 0
        self.transaction_list.data = []
        self.transaction_list.scroll_y = 1
        _w = self.app.ctrl.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        # _transactions = 0
        _txd = []
        _new_tdx = {}
        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    for _h in address.history:
                        _d = {
                                'time': _h['time'],
                                'transaction': _h['txid'],
                                'block': str(_h['block']),
                                'txvalue': str(Ut.from_sats(_h['value'])),
                                'sm': self.manager,
                                'status': ''} #_s}

                        if _d['transaction'] + _d['block'] not in _new_tdx:
                            _new_tdx[_d['transaction'] + _d['block']] = _d
                        else:
                            _v = float(_new_tdx[_d['transaction'] + _d['block']]['txvalue']) + float(_d['txvalue'])
                            _new_tdx[_d['transaction'] + _d['block']]['txvalue'] = str(round(_v, 8))

            # Change
            if self.manager.settings_screen.settings.show_change:
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        for _h in address.history:
                            _d = {
                                    'time': _h['time'],
                                    'transaction': _h['txid'],
                                    'block': str(_h['block']),
                                    'txvalue': str(Ut.from_sats(_h['value'])),
                                    'sm': self.manager,
                                    'status': ''} #_s}

                            if _d['transaction'] + _d['block'] not in _new_tdx:
                                _new_tdx[_d['transaction'] + _d['block']] = _d
                            else:
                                _v = float(_new_tdx[_d['transaction'] + _d['block']]['txvalue']) + float(_d['txvalue'])
                                _new_tdx[_d['transaction'] + _d['block']]['txvalue'] = str(round(_v, 8))

            for _, v in _new_tdx.items():
                _txd.append(v)

            _txd.sort(reverse=True, key=self.sort_dict)
            self.transaction_list.data = _txd

        self.manager.current = 'transactions_screen'
