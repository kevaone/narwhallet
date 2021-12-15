from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from narwhallet.core.kui.ux.widgets.generator import UShared

class _address_book_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(9, ['', 'Coin', 'Name', 'Address', 'Sent',
                                      'Received', 'Label', '', ''], self)
        self.setColumnHidden(1, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)

    # def test_param(self, book_address: dict, val: str, default: str):
    #     if val in book_address:
    #         _return = QTableWidgetItem(str(book_address[val]))
    #     else:
    #         _return = QTableWidgetItem(str(default))
    #     return _return

    def add_bookaddresses(self, book_addresses: list):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

        for i in book_addresses:
            self.add_bookaddress(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(7, 20)

    def add_bookaddress(self, book_address: dict):
        self.setSortingEnabled(False)
        _r = self.rowCount()
        self.insertRow(_r)

        _vpic = UShared.create_table_item_graphic(1)
        _bvpic = UShared.create_table_item_graphic(2)

        _coin = UShared.create_table_item(book_address['coin'])
        # _coin = QTableWidgetItem(book_address['coin'])
        # _coin.setFlags(UShared.flags())
        # _coin.setForeground(QtCore.Qt.black)

        _name = UShared.create_table_item(book_address['name'])
        # _name = QTableWidgetItem(book_address['name'])
        # _name.setFlags(UShared.flags())
        # _name.setForeground(QtCore.Qt.black)

        _address = UShared.create_table_item(book_address['address'])
        # _address = QTableWidgetItem(book_address['address'])
        # _address.setFlags(UShared.flags())
        # _address.setForeground(QtCore.Qt.black)
        if 'sent' in book_address:
            _sent = UShared.create_table_item(book_address['sent'])
        else:
            _sent = UShared.create_table_item('0.0')
        # _sent = self.test_param(book_address, 'sent', '0.0')
        # _sent.setFlags(UShared.flags())
        # _sent.setForeground(QtCore.Qt.black)

        if 'received' in book_address:
            _received = UShared.create_table_item(book_address['received'])
        else:
            _received = UShared.create_table_item('0.0')
        # _received = self.test_param(book_address, 'received', '0.0')
        # _received.setFlags(UShared.flags())
        # _received.setForeground(QtCore.Qt.black)

        _label = UShared.create_table_item(book_address['label'])
        # _label = QTableWidgetItem(book_address['label'])
        # _label.setFlags(UShared.flags())
        # _label.setForeground(QtCore.Qt.black)

        _dellabel = UShared.create_table_item_graphic(3)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _coin)
        self.setItem(_r, 2, _name)
        self.setItem(_r, 3, _address)
        self.setItem(_r, 4, _sent)
        self.setItem(_r, 5, _received)
        self.setItem(_r, 6, _label)
        self.setCellWidget(_r, 7, _dellabel)
        self.setCellWidget(_r, 8, _bvpic)
        self.setSortingEnabled(True)
