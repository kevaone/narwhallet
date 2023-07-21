from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class AddressesScreen(Screen):
    address_list = GridLayout()
    wallet_name = Nwlabel()
    header = Header()
    btn_add = Nwbutton()

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.header.value = wallet_name
        self.address_list.data = []
        
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        _addr = []
        if _w is not None:
            if _w.kind == EWalletKind.NORMAL:
                self.btn_add.text = 'Increase Pool'
            else:
                self.btn_add.text = 'Add Address'

            for address in _w.addresses.addresses:
                if address is not None:
                    _a = {
                    'address': address.address,
                    'address_label': address.label,
                    'balance': str(round(address.balance, 8)),
                    'transactions': str(len(address.history)),
                    'wallet_name': wallet_name,
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
                        'sm': self.manager}

                        _addr.append(_a)
        self.address_list.scroll_y = 1
        self.address_list.data = _addr
        self.manager.current = 'addresses_screen'

    def increase_address_pool(self):
        _w = self.manager.wallets.get_wallet_by_name(self.header.value)
        _ = _w.get_unused_address()
        self.manager.wallets.save_wallet(_w.name)
        self.manager.wallet_screen.btn_addresses.text = 'Addresses (' + str(_w.account_index + _w.change_index) + ')'
        self.populate(self.header.value)

    def add_watch_address(self):
        # TODO: Impliment
        pass

    def btn_add_click(self):
        if self.btn_add.text == 'Increase Pool':
            self.increase_address_pool()
        else:
            self.add_watch_address()