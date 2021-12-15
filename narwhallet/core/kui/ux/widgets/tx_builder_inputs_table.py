from PyQt5.QtWidgets import QWidget, QTableWidget
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

    def add_input(self, value: float, address: str, tx_hash: str, n: int,
                  script: str):

        _r = self.rowCount()
        self.insertRow(_r)

        _value = UShared.create_table_item(value)
        _address = UShared.create_table_item(address)
        _n = UShared.create_table_item(n)
        _tx_hash = UShared.create_table_item(tx_hash)
        _script = UShared.create_table_item(script)
        _sequence = UShared.create_table_item('ffffffff')

        self.setItem(_r, 0, _value)
        self.setItem(_r, 1, _address)
        self.setItem(_r, 2, _tx_hash)
        self.setItem(_r, 3, _n)
        self.setItem(_r, 4, _script)
        self.setItem(_r, 5, _sequence)

        self.resizeColumnsToContents()
