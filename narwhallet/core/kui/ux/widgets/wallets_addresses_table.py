from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget

from narwhallet.core.kui.ux.widgets.generator import UShared

class _wallets_addr_tbl(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(7, ['', 'Address', 'Received',
                                        'Sent', 'Balance', 'Label', ''], self)
        # self.setColumnCount(7)
        # self.setHorizontalHeaderLabels(['', 'Address', 'Received',
        #                                 'Sent', 'Balance', 'Label', ''])
        # self.horizontalHeaderItem(0).setTextAlignment(4)
        # self.horizontalHeaderItem(1).setTextAlignment(4)
        # self.horizontalHeaderItem(2).setTextAlignment(4)
        # self.horizontalHeaderItem(3).setTextAlignment(4)
        # self.horizontalHeaderItem(4).setTextAlignment(4)
        # self.horizontalHeaderItem(5).setTextAlignment(4)
        # self.horizontalHeaderItem(6).setTextAlignment(4)
        # self.horizontalHeader().setMinimumSectionSize(25)

    def test_param(self, address_data: dict, val: str, default: str,
                   ret_str: bool = False):
        if val in address_data:
            if address_data[val] is None:
                _ret = ''
            else:
                _ret = str(address_data[val])
            if ret_str is False:
                _return = UShared._create_table_item(_ret)
            else:
                _return = _ret
        else:
            if ret_str is False:
                _return = UShared._create_table_item(str(default))
            else:
                _return = str(default)
        return _return

    def clear_row(self, row):
        self.setRowHidden(row, True)
        self.item(row, 1).setText('')
        self.item(row, 2).setText('')
        self.item(row, 3).setText('')
        self.item(row, 4).setText('')
        self.item(row, 5).setText('')

    def clear_rows(self):
        for i in range(0, self.rowCount()):
            self.clear_row(i)

    def add_addresses(self, addresses_data: list):
        for i in range(0, self.rowCount()):
            self.clear_row(i)

        for c, dat in enumerate(addresses_data):
            self.add_address(c, dat)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def add_address(self, idx: int, address_data: dict):
        if idx == self.rowCount():
            self.insertRow(idx)
            _pic = UShared._create_table_item_graphic(1)
            _bpic = UShared._create_table_item_graphic(2)
            _address = UShared._create_table_item(address_data['address'])
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
            self.setItem(idx, 1, _address)
            self.setItem(idx, 2, _received)
            self.setItem(idx, 3, _sent)
            self.setItem(idx, 4, _balance)
            self.setItem(idx, 5, _label)
            self.setCellWidget(idx, 6, _bpic)
        elif idx <= self.rowCount():
            address_data['received'] = round(address_data['received'], 9)
            address_data['sent'] = round(address_data['sent'], 9)
            address_data['balance'] = round(address_data['balance'], 9)
            address_data['label'] = ''
            self.item(idx, 1).setText(address_data['address'])
            (self.item(idx, 2)
             .setText(self.test_param(address_data, 'received', '0.0', True)))
            (self.item(idx, 3)
             .setText(self.test_param(address_data, 'sent', '0.0', True)))
            (self.item(idx, 4)
             .setText(self.test_param(address_data, 'balance', '0.0', True)))
            self.item(idx, 5).setText(address_data['label'])
            self.setRowHidden(idx, False)
