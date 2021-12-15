from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from narwhallet.core.kui.ux.widgets.generator import UShared

class _tx_builder_inputs_table(QTableWidget):
    def __init__(self, _parent: QWidget):
        super().__init__()

        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(6, ['value', 'address', 'tx_hash',
                                        'n', 'script_sig', 'sequence'], self)
        # self.setColumnCount(6)
        # self.setHorizontalHeaderLabels(['value', 'address', 'tx_hash',
        #                                 'n', 'script_sig', 'sequence'])
        # self.horizontalHeaderItem(0).setTextAlignment(4)
        # self.horizontalHeaderItem(1).setTextAlignment(4)
        # self.horizontalHeaderItem(2).setTextAlignment(4)
        # self.horizontalHeaderItem(3).setTextAlignment(4)
        # self.horizontalHeaderItem(4).setTextAlignment(4)
        # self.horizontalHeaderItem(5).setTextAlignment(4)
        # self.horizontalHeader().setMinimumSectionSize(25)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_input(self, value: float, address: str, tx_hash: str, n: int,
                  script: str):

        _r = self.rowCount()
        self.insertRow(_r)

        _value = QTableWidgetItem(str(value))
        _value.setFlags(UShared.flags())
        _value.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(address)
        _address.setFlags(UShared.flags())
        _address.setForeground(QtCore.Qt.black)

        _n = QTableWidgetItem(str(n))
        _n.setFlags(UShared.flags())
        _n.setForeground(QtCore.Qt.black)

        _tx_hash = QTableWidgetItem(tx_hash)
        _tx_hash.setFlags(UShared.flags())
        _tx_hash.setForeground(QtCore.Qt.black)

        _script = QTableWidgetItem(script)
        _script.setFlags(UShared.flags())
        _script.setForeground(QtCore.Qt.black)

        _sequence = QTableWidgetItem('ffffffff')
        _sequence.setFlags(UShared.flags())
        _sequence.setForeground(QtCore.Qt.black)

        self.setItem(_r, 0, QTableWidgetItem(_value))
        self.setItem(_r, 1, QTableWidgetItem(_address))
        self.setItem(_r, 2, QTableWidgetItem(_tx_hash))
        self.setItem(_r, 3, QTableWidgetItem(_n))
        self.setItem(_r, 4, QTableWidgetItem(_script))
        self.setItem(_r, 5, QTableWidgetItem(_sequence))

        self.resizeColumnsToContents()
