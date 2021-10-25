from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class _tx_builder_inputs_table(QTableWidget):
    def __init__(self, QWidget):
        super().__init__()

        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['value', 'address', 'tx_hash',
                                        'n', 'script_sig', 'sequence'])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_input(self, value: float, address: str, tx_hash: str, n: int,
                  script: str):
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iide = QtCore.Qt.ItemIsDragEnabled
        _if_iied = QtCore.Qt.ItemIsEditable

        _r = self.rowCount()
        self.insertRow(_r)

        _value = QTableWidgetItem(str(value))
        _value.setFlags(_if_iied | _if_iis | _if_iide)
        _value.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(address)
        _address.setFlags(_if_iied | _if_iis | _if_iide)
        _address.setForeground(QtCore.Qt.black)

        _n = QTableWidgetItem(str(n))
        _n.setFlags(_if_iied | _if_iis | _if_iide)
        _n.setForeground(QtCore.Qt.black)

        _tx_hash = QTableWidgetItem(tx_hash)
        _tx_hash.setFlags(_if_iied | _if_iis | _if_iide)
        _tx_hash.setForeground(QtCore.Qt.black)

        _script = QTableWidgetItem(script)
        _script.setFlags(_if_iied | _if_iis | _if_iide)
        _script.setForeground(QtCore.Qt.black)

        _sequence = QTableWidgetItem('ffffffff')
        _sequence.setFlags(_if_iied | _if_iis | _if_iide)
        _sequence.setForeground(QtCore.Qt.black)

        self.setItem(_r, 0, QTableWidgetItem(_value))
        self.setItem(_r, 1, QTableWidgetItem(_address))
        self.setItem(_r, 2, QTableWidgetItem(_tx_hash))
        self.setItem(_r, 3, QTableWidgetItem(_n))
        self.setItem(_r, 4, QTableWidgetItem(_script))
        self.setItem(_r, 5, QTableWidgetItem(_sequence))

        self.resizeColumnsToContents()
