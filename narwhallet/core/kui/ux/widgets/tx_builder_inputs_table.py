from PyQt5.QtWidgets import QWidget
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.ntablewidget import NTableWidget


class _tx_builder_inputs_table(NTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.set_properties(name)
        self.set_columns(6, ['value', 'address', 'tx_hash',
                                      'n', 'script_sig', 'sequence'])

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
