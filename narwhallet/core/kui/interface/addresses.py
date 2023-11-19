from copy import copy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwspinner import Nwspinner


class AddressesScreen(Screen):
    address_list = GridLayout()
    wallet_name = Nwlabel()
    header = Header()
    btn_add = Nwbutton()
    spn_sort = Nwspinner()

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.header.value = wallet_name
        self.address_list.data = []
        self.app = App.get_running_app()
        _w = self.app.ctrl.wallets.get_wallet_by_name(wallet_name)
        self._addr = []
        self._original = None

        if _w is not None:
            if _w.kind == EWalletKind.NORMAL:
                self.btn_add._text = 'Increase Pool'
            else:
                self.btn_add._text = 'Add Address'

            _idx = 0
            for address in _w.addresses.addresses:
                if address is not None:
                    _a = {
                    'index': str(_idx),
                    'address': address.address,
                    'address_label': address.label,
                    'balance': str(round(address.balance, 8)),
                    'transactions': str(len(address.history)),
                    'wallet_name': wallet_name,
                    'background_color': [25/255, 27/255, 27/255, 1],
                    'sm': self.manager}

                    self._addr.append(_a)
                    _idx = _idx + 1

            if self.manager.settings_screen.settings.show_change:
                _idx = 0
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        _a = {
                        'index': str(_idx),
                        'address': address.address,
                        'address_label': address.label,
                        'balance': str(round(address.balance, 8)),
                        'transactions': str(len(address.history)),
                        'wallet_name': wallet_name,
                        'background_color': [86/255, 86/255, 86/255, 1],
                        'sm': self.manager}

                        self._addr.append(_a)
                        _idx = _idx + 1
        self.spn_sort._sort = 'bal_dsc'
        self.spn_sort.icon = 'narwhallet/core/kui/assets/balance-sort-down.png'
        self.spn_sort._text = ''
        self.spn_sort.values = [['bal_asc', 'narwhallet/core/kui/assets/balance-sort-up.png'],['bal_dsc', 'narwhallet/core/kui/assets/balance-sort-down.png']]
        self.address_list.scroll_y = 1
        self.address_list.data = self._addr
        self.manager.current = 'addresses_screen'

    def increase_address_pool(self):
        _w = self.app.ctrl.wallets.get_wallet_by_name(self.header.value)
        _ = _w.get_unused_address()
        self.app.ctrl.wallets.save_wallet(_w.name)
        # app = App.get_running_app()
        self.manager.wallet_screen.btn_addresses.text = self.app.translate_text('Addresses') + ' (' + str(_w.account_index + _w.change_index) + ')'
        self.populate(self.header.value)

    def add_watch_address(self):
        # TODO: Impliment
        pass

    def btn_add_click(self):
        if self.btn_add._text == 'Increase Pool':
            self.increase_address_pool()
        else:
            self.add_watch_address()

    def sort(self, *args):
        if args[0] == 'bal_asc':
            self._addr.sort(reverse=False, key=self._sort)
        elif args[0] == 'bal_dsc':
            self._addr.sort(reverse=True, key=self._sort)
        self.address_list.data = self._addr

    @staticmethod
    def _sort(item):
        return item['balance']

    def filter_zero_balance(self, *args):
        if self._original is None:
            self._original = copy(self._addr)
            _tmp = []
            for _i in self._addr:
                if _i['balance'] != '0.0':
                    _tmp.append(_i)
            self._addr = _tmp
            self.spn_sort.background_color = [86/255, 86/255, 86/255, 1]
            self.spn_sort._t = [86/255, 86/255, 86/255, 1]
        else:
            self._addr = copy(self._original)
            self._original = None
            self.spn_sort.background_color = [54/255, 58/255, 59/255, 1]
            self.spn_sort._t = [54/255, 58/255, 59/255, 1]
        self.address_list.data = self._addr
        