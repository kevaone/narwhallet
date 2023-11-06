from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header
# from narwhallet.core.kui.widgets.nwspinner import Nwspinner


class AddressesScreen(Screen):
    address_list = GridLayout()
    wallet_name = Nwlabel()
    header = Header()
    btn_add = Nwbutton()
    # spn_sort = Nwspinner()

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.header.value = wallet_name
        self.address_list.data = []
        self.app = App.get_running_app()
        _w = self.app.ctrl.wallets.get_wallet_by_name(wallet_name)
        _addr = []
        # self.spn_sort.values = [['', 'narwhallet/core/kui/assets/balance-sort-up.png'],['', 'narwhallet/core/kui/assets/balance-sort-down.png']]
        if _w is not None:
            if _w.kind == EWalletKind.NORMAL:
                self.btn_add._text = 'Increase Pool'
            else:
                self.btn_add._text = 'Add Address'

            for address in _w.addresses.addresses:
                if address is not None:
                    _a = {
                    'address': address.address,
                    'address_label': address.label,
                    'balance': str(round(address.balance, 8)),
                    'transactions': str(len(address.history)),
                    'wallet_name': wallet_name,
                    'background_color': [25/255, 27/255, 27/255, 1],
                    'sm': self.manager}

                    _addr.append(_a)

            if self.manager.settings_screen.settings.show_change:
                for address in _w.change_addresses.addresses:
                    if address is not None:
                        _a = {
                        'address': address.address,
                        'address_label': address.label,
                        'balance': str(round(address.balance, 8)),
                        'transactions': str(len(address.history)),
                        'wallet_name': wallet_name,
                        'background_color': [86/255, 86/255, 86/255, 1],
                        'sm': self.manager}

                        _addr.append(_a)
        self.address_list.scroll_y = 1
        self.address_list.data = _addr
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
