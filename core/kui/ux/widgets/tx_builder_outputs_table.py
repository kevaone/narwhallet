from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem


class _tx_builder_outputs_table(QTableWidget):
    def __init__(self, _parent: QWidget):
        super().__init__()

        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Value', 'Address', 'Script'])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_output(self, value: float, address: str, script: str):
        _if_iied = QtCore.Qt.ItemIsEditable
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iide = QtCore.Qt.ItemIsDragEnabled

        _r = self.rowCount()
        self.insertRow(_r)

        _value = QTableWidgetItem(str(value))
        # _value.setFlags(_if_iied | _if_iis | _if_iide)
        _value.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(address)
        _address.setFlags(_if_iied | _if_iis | _if_iide)
        _address.setForeground(QtCore.Qt.black)

        _script = QTableWidgetItem(script)
        _script.setFlags(_if_iied | _if_iis | _if_iide)
        _script.setForeground(QtCore.Qt.black)

        self.setItem(_r, 0, QTableWidgetItem(_value))
        self.setItem(_r, 1, QTableWidgetItem(_address))
        self.setItem(_r, 2, QTableWidgetItem(_script))
        self.resizeColumnsToContents()
