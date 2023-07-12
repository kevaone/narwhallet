from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo
from narwhallet.core.kui.widgets.qrcode import QR_Code
import qrcode
from narwhallet.core.kui.widgets.header import Header


class AddressScreen(Screen):
    address = Nwlabel()
    balance = Nwlabel()
    label = Nwlabel()
    transactions = Nwlabel()
    transaction_list = GridLayout()
    qr_code = QR_Code()
    header = Header()

    def populate(self, wallet_name, address):
        self.transaction_list.clear_widgets()
        _w = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = wallet_name
        
        
        if _w is not None:
            try:
                _addr = _w.addresses.get_address_by_name(address)
            except:
                _addr = _w.change_addresses.get_address_by_name(address)

            self.address.text = address
            self.balance.text = str(round(_addr.balance, 8)) #str(_addr.balance)
            self.label.text = _addr.label
            self.transactions.text = str(len(_addr.history))

            for _h in _addr.history:
                _t = TransactionListInfo()
                _t.transaction.text = _h['tx_hash']
                _t.block.text = str(_h['height'])
                _t.sm = self.manager
                self.transaction_list.add_widget(_t)

        self.qr_code.data = self.address.text
        self.manager.current = 'address_screen'
