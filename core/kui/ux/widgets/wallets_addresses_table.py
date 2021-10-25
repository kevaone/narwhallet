import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class _wallets_addr_tbl(QTableWidget):
    def __init__(self, name: str, QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['', 'Address', 'Received',
                                        'Sent', 'Balance', 'Label', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    def test_param(self, address_data: dict, val: str, default: str):
        if val in address_data:
            if address_data[val] is None:
                _ret = ''
            else:
                _ret = str(address_data[val])
            _return = QTableWidgetItem(_ret)
        else:
            _return = QTableWidgetItem(str(default))
        return _return

    def add_addresses(self, addresses_data: list):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

        for i in addresses_data:
            self.add_address(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def add_address(self, address_data: dict):
        _al_center = QtCore.Qt.AlignCenter
        _if_iied = QtCore.Qt.ItemIsEditable
        _if_iis = QtCore.Qt.ItemIsSelectable
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

        _address = QTableWidgetItem(address_data['address'])
        _address.setFlags(_if_iied | _if_iis | _if_iide)
        _address.setForeground(QtCore.Qt.black)
        address_data['received'] = round(address_data['received'], 9)
        _received = self.test_param(address_data, 'received', '0.0')
        _received.setFlags(_if_iied | _if_iis | _if_iide)
        _received.setForeground(QtCore.Qt.black)
        _af_ar = QtCore.Qt.AlignRight
        _af_avc = QtCore.Qt.AlignVCenter
        _received.setTextAlignment(_af_ar | _af_avc)
        address_data['sent'] = round(address_data['sent'], 9)
        _sent = self.test_param(address_data, 'sent', '0.0')
        _sent.setFlags(_if_iied | _if_iis | _if_iide)
        _sent.setForeground(QtCore.Qt.black)
        _sent.setTextAlignment(_af_ar | _af_avc)
        address_data['balance'] = round(address_data['balance'], 9)
        _balance = self.test_param(address_data, 'balance', '0.0')
        _balance.setFlags(_if_iied | _if_iis | _if_iide)
        _balance.setForeground(QtCore.Qt.black)
        _balance.setTextAlignment(_af_ar | _af_avc)

        _label = self.test_param(address_data, 'label', '')
        _label.setFlags(_if_iied | _if_iis | _if_iide)
        _label.setForeground(QtCore.Qt.black)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _address)
        self.setItem(_r, 2, _received)
        self.setItem(_r, 3, _sent)
        self.setItem(_r, 4, _balance)
        self.setItem(_r, 5, _label)
        self.setCellWidget(_r, 6, _bvpic)
