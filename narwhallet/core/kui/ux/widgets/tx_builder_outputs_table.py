from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.core.kui.ux.widgets.generator import UShared


class _tx_builder_outputs_table(QTableWidget):
    def __init__(self, _parent: QWidget):
        super().__init__()

        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(3, ['Value', 'Address', 'Script'], self)

    # def clear_rows(self):
    #     _m = self.rowCount()

    #     while _m > -1:
    #         self.removeRow(_m)
    #         _m = _m - 1

    def add_output(self, value: float, address: str, script: str):
        _r = self.rowCount()
        self.insertRow(_r)

        _value = UShared.create_table_item(value)
        _address = UShared.create_table_item(address)
        _script = UShared.create_table_item(script)

        self.setItem(_r, 0, _value)
        self.setItem(_r, 1, _address)
        self.setItem(_r, 2, _script)
        self.resizeColumnsToContents()
