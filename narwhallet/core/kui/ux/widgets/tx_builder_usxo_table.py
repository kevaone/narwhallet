from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from narwhallet.core.kui.ux.widgets.generator import UShared

class _tx_builder_usxo_table(QTableWidget):
    def __init__(self, _parent: QWidget):
        super().__init__()

        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['wallet', 'address', '', 'value',
                                        'pos', 'tx_hash', 'height'])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

        self.setColumnHidden(2, True)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_usxo(self, wallet: str, usxo: list):
        for i in usxo:
            i['wallet'] = wallet
            self._add_usxo(i)

        self.resizeColumnsToContents()

    def _add_usxo(self, usxo_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _wallet = QTableWidgetItem(usxo_data['wallet'])
        _wallet.setFlags(UShared.flags())
        _wallet.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(str(usxo_data['a']))
        _address.setFlags(UShared.flags())
        _address.setForeground(QtCore.Qt.black)

        _address_index = QTableWidgetItem(str(usxo_data['a_idx'])
                                          + ':' + str(usxo_data['ch']))
        _address_index.setFlags(UShared.flags())
        _address_index.setForeground(QtCore.Qt.black)

        _ts_pos = QTableWidgetItem(str(usxo_data['tx_pos']))
        _ts_pos.setFlags(UShared.flags())
        _ts_pos.setForeground(QtCore.Qt.black)

        _value_dat = int(usxo_data['value']) / 100000000
        _value = QTableWidgetItem(str(_value_dat))
        _value.setFlags(UShared.flags())
        _value.setForeground(QtCore.Qt.black)

        _height = QTableWidgetItem(str(usxo_data['height']))
        _height.setFlags(UShared.flags())
        _height.setForeground(QtCore.Qt.black)

        _tx_hash = QTableWidgetItem(usxo_data['tx_hash'])
        _tx_hash.setFlags(UShared.flags())
        _tx_hash.setForeground(QtCore.Qt.black)

        # _check = QCheckBox()
        # _check.clicked.connect(self.usxo_checked)

        self.setItem(_r, 0, QTableWidgetItem(_wallet))
        self.setItem(_r, 1, QTableWidgetItem(_address))
        self.setItem(_r, 2, QTableWidgetItem(_address_index))
        # self.setCellWidget(_r, 1, _check)
        self.setItem(_r, 3, QTableWidgetItem(_value))
        self.setItem(_r, 4, QTableWidgetItem(_ts_pos))

        self.setItem(_r, 5, QTableWidgetItem(_tx_hash))
        self.setItem(_r, 6, QTableWidgetItem(_height))
