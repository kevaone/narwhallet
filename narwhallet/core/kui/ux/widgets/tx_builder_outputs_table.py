from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem

from narwhallet.core.kui.ux.widgets.generator import UShared

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

    # @staticmethod
    # def flags():
    #     return (QtCore.Qt.ItemIsSelectable |
    #             QtCore.Qt.ItemIsEditable |
    #             QtCore.Qt.ItemIsDragEnabled)

    def add_output(self, value: float, address: str, script: str):
        _r = self.rowCount()
        self.insertRow(_r)

        _value = QTableWidgetItem(str(value))
        # _value.setFlags(self.flags())
        _value.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(address)
        _address.setFlags(UShared.flags())
        _address.setForeground(QtCore.Qt.black)

        _script = QTableWidgetItem(script)
        _script.setFlags(UShared.flags())
        _script.setForeground(QtCore.Qt.black)

        self.setItem(_r, 0, QTableWidgetItem(_value))
        self.setItem(_r, 1, QTableWidgetItem(_address))
        self.setItem(_r, 2, QTableWidgetItem(_script))
        self.resizeColumnsToContents()
