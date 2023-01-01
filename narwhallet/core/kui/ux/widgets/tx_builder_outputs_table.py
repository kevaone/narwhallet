from PyQt5.QtWidgets import QWidget
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.ntablewidget import NTableWidget


class _tx_builder_outputs_table(NTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.set_properties(name)
        self.set_columns(3, ['Value', 'Address', 'Script'])

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
