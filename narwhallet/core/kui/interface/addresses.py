from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class AddressesScreen(Screen):
    address_list = GridLayout()
    wallet_name = Nwlabel()

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.wallet_name.text = wallet_name.text
        self.address_list.clear_widgets()
        
        _w = self.manager.wallets.get_wallet_by_name(wallet_name.text)

        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    _a = AddressListInfo()
                    _a.address.text = address.address
                    _a.address_label.text = address.label
                    _a.balance.text = str(round(address.balance, 8))
                    _a.transactions.text = str(len(address.history))
                    _a.wallet_name = wallet_name
                    _a.sm = self.manager

                    self.address_list.add_widget(_a)
            for address in _w.change_addresses.addresses:
                if address is not None:
                    _a = AddressListInfo()
                    _a.address.text = address.address
                    _a.address_label.text = address.label
                    _a.balance.text = str(round(address.balance, 8))
                    _a.transactions.text = str(len(address.history))
                    _a.wallet_name = wallet_name
                    _a.sm = self.manager

                    self.address_list.add_widget(_a)
        self.address_list.parent.scroll_y = 1
        self.manager.current = 'addresses_screen'

    def increase_address_pool(self):
        _w = self.manager.wallets.get_wallet_by_name(self.wallet_name.text)
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
