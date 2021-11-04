import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel


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

    def add_bookaddress(self, book_address: dict):
        _al_center = QtCore.Qt.AlignCenter
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iied = QtCore.Qt.ItemIsEditable
        _if_iide = QtCore.Qt.ItemIsDragEnabled
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(_r)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/information.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        _bpic = QtGui.QPixmap(os.path.join(__path, '../assets/clipboard.png'))
        _bpic = _bpic.scaledToWidth(20, _transm_st)
        _bvpic = QLabel()
        _bvpic.setPixmap(_bpic)
        _bvpic.setAlignment(_al_center)
        _bvpic.setContentsMargins(0, 0, 0, 0)

        _coin = QTableWidgetItem(book_address['coin'])
        _coin.setFlags(_if_iied | _if_iis | _if_iide)
        _coin.setForeground(QtCore.Qt.black)

        _name = QTableWidgetItem(book_address['name'])
        _name.setFlags(_if_iied | _if_iis | _if_iide)
        _name.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(book_address['address'])
        _address.setFlags(_if_iied | _if_iis | _if_iide)
        _address.setForeground(QtCore.Qt.black)

        _sent = self.test_param(book_address, 'sent', '0.0')
        _sent.setFlags(_if_iied | _if_iis | _if_iide)
        _sent.setForeground(QtCore.Qt.black)

        _received = self.test_param(book_address, 'received', '0.0')
        _received.setFlags(_if_iied | _if_iis | _if_iide)
        _received.setForeground(QtCore.Qt.black)

        _label = QTableWidgetItem(book_address['label'])
        _label.setFlags(_if_iied | _if_iis | _if_iide)
        _label.setForeground(QtCore.Qt.black)

        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/trashcan.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _dellabel = QLabel()
        _dellabel.setPixmap(_pic)
        _dellabel.setAlignment(_al_center)
        _dellabel.setContentsMargins(0, 0, 0, 0)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _coin)
        self.setItem(_r, 2, _name)
        self.setItem(_r, 3, _address)
        self.setItem(_r, 4, _sent)
        self.setItem(_r, 5, _received)
        self.setItem(_r, 6, _label)
        self.setCellWidget(_r, 7, _dellabel)
        self.setCellWidget(_r, 8, _bvpic)
