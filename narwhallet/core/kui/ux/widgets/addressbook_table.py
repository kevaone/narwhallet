from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


class _address_book_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(['', 'Coin', 'Name', 'Address', 'Sent',
                                        'Received', 'Label', '', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.setColumnHidden(1, True)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.setColumnHidden(4, True)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.setColumnHidden(5, True)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeaderItem(8).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(5)

    def test_param(self, book_address: dict, val: str, default: str):
        if val in book_address:
            _return = QTableWidgetItem(str(book_address[val]))
        else:
            _return = QTableWidgetItem(str(default))
        return _return

    def add_bookaddresses(self, book_addresses: list):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

        for i in book_addresses:
            self.add_bookaddress(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(7, 20)

    @staticmethod
    def _create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _vpic = QLabel()

        if pic == 0:
            _p = QPixmap(MShared.get_resource_path('information'))
            _vpic.setToolTip('View Address Details')
        elif pic == 1:
            _p = QPixmap(MShared.get_resource_path('clipboard.png'))
            _vpic.setToolTip('Copy Address to Clipboard')
        elif pic == 2:
            _p = QPixmap(MShared.get_resource_path('trashcan.png'))
            _vpic.setToolTip('Delete Adderess From Address Book')

        _p = _p.scaledToWidth(20, _transm_st)

        _vpic.setPixmap(_p)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        return _vpic

    @staticmethod
    def flags():
        return (QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsDragEnabled)

    def add_bookaddress(self, book_address: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _vpic = self._create_table_item_graphic(0)
        _bvpic = self._create_table_item_graphic(1)

        _coin = QTableWidgetItem(book_address['coin'])
        _coin.setFlags(self.flags())
        _coin.setForeground(QtCore.Qt.black)

        _name = QTableWidgetItem(book_address['name'])
        _name.setFlags(self.flags())
        _name.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(book_address['address'])
        _address.setFlags(self.flags())
        _address.setForeground(QtCore.Qt.black)

        _sent = self.test_param(book_address, 'sent', '0.0')
        _sent.setFlags(self.flags())
        _sent.setForeground(QtCore.Qt.black)

        _received = self.test_param(book_address, 'received', '0.0')
        _received.setFlags(self.flags())
        _received.setForeground(QtCore.Qt.black)

        _label = QTableWidgetItem(book_address['label'])
        _label.setFlags(self.flags())
        _label.setForeground(QtCore.Qt.black)

        _dellabel = self._create_table_item_graphic(2)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _coin)
        self.setItem(_r, 2, _name)
        self.setItem(_r, 3, _address)
        self.setItem(_r, 4, _sent)
        self.setItem(_r, 5, _received)
        self.setItem(_r, 6, _label)
        self.setCellWidget(_r, 7, _dellabel)
        self.setCellWidget(_r, 8, _bvpic)
