from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.ntablewidget import NTableWidget


class _wallets_addr_tbl(NTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.set_properties(name)
        self.set_columns(7, ['', 'Address', 'Received',
                                      'Sent', 'Balance', 'Label', ''])

    def test_param(self, address_data: dict, val: str, default: str,
                   ret_str: bool = False):
        if val in address_data:
            if address_data[val] is None:
                _ret = ''
            else:
                _ret = str(address_data[val])
            if ret_str is False:
                _return = UShared.create_table_item(_ret)
            else:
                _return = _ret
        else:
            if ret_str is False:
                _return = UShared.create_table_item(str(default))
            else:
                _return = str(default)
        return _return

    def add_addresses(self, addresses_data: list):
        self.clear_rows()
        self.setSortingEnabled(False)
        for c, dat in enumerate(addresses_data):
            self.add_address(c, dat)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def add_address(self, idx: int, address_data: dict):
        if idx == self.rowCount():
            self.insertRow(idx)
            _pic = UShared.create_table_item_graphic(1)
            _pic.setToolTip('View Address Details')
            _bpic = UShared.create_table_item_graphic(2)
            _bpic.setToolTip('Copy Address to Clipboard')
            _address = UShared.create_table_item(address_data['address'])
            address_data['received'] = round(address_data['received'], 9)
            _received = self.test_param(address_data, 'received', '0.0')
            _af_ar = QtCore.Qt.AlignRight
            _af_avc = QtCore.Qt.AlignVCenter
            _received.setTextAlignment(_af_ar | _af_avc)
            address_data['sent'] = round(address_data['sent'], 9)
            _sent = self.test_param(address_data, 'sent', '0.0')
            _sent.setTextAlignment(_af_ar | _af_avc)
            address_data['balance'] = round(address_data['balance'], 9)
            _balance = self.test_param(address_data, 'balance', '0.0')
            _balance.setTextAlignment(_af_ar | _af_avc)
            _label = self.test_param(address_data, 'label', '')

            self.setCellWidget(idx, 0, _pic)
            self.setItem(idx, 0, UShared.create_table_item(''))
            self.setItem(idx, 1, _address)
            self.setItem(idx, 2, _received)
            self.setItem(idx, 3, _sent)
            self.setItem(idx, 4, _balance)
            self.setItem(idx, 5, _label)
            self.setCellWidget(idx, 6, _bpic)
            self.setItem(idx, 6, UShared.create_table_item(''))
        elif idx <= self.rowCount():
            address_data['received'] = round(address_data['received'], 9)
            address_data['sent'] = round(address_data['sent'], 9)
            address_data['balance'] = round(address_data['balance'], 9)
            address_data['label'] = ''
            self.set_text(idx, 1, address_data['address'])
            (self.set_text(idx, 2,
             self.test_param(address_data, 'received', '0.0', True)))
            (self.set_text(idx, 3,
             self.test_param(address_data, 'sent', '0.0', True)))
            (self.set_text(idx, 4,
             self.test_param(address_data, 'balance', '0.0', True)))
            self.set_text(idx, 5, address_data['label'])
            self.setRowHidden(idx, False)
