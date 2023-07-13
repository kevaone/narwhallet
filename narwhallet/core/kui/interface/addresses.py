from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class AddressesScreen(Screen):
    address_list = GridLayout()
    wallet_name = Nwlabel()
    header = Header()

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.header.value = wallet_name
        self.address_list.data = []
        
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        _addr = []
        if _w is not None:
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
        _addr = _w.get_unused_address()
        self.manager.wallets.save_wallet(_w.name)
        _a = AddressListInfo()
        _a.address.text = _addr
        _a.address_label.text = ''
        _a.balance.text = '0.0'
        _a.transactions.text = '0'
        _a.wallet_name = _w.name
        _a.sm = self.manager

        self.address_list.add_widget(_a)
        self.manager.wallet_screen.btn_addresses.text = 'Addresses (' + str(_w.account_index + _w.change_index) + ')'
