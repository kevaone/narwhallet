from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.core.kui.ux.widgets.generator import UShared


class _tx_builder_usxo_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        UShared.set_table_properties(self, name)
        UShared.set_table_columns(7, ['wallet', 'address', '', 'value',
                                      'pos', 'tx_hash', 'height'], self)

        self.setColumnHidden(2, True)

    def add_usxo(self, wallet: str, usxo: list):
        for i in usxo:
            i['wallet'] = wallet
            self._add_usxo(i)

        self.resizeColumnsToContents()

    def _add_usxo(self, usxo_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _wallet = UShared.create_table_item(usxo_data['wallet'])
        _address = UShared.create_table_item(usxo_data['a'])
        _address_index = UShared.create_table_item((str(usxo_data['a_idx'])
                                                    + ':' +
                                                    str(usxo_data['ch'])))
        _ts_pos = UShared.create_table_item(usxo_data['tx_pos'])
        _value_dat = int(usxo_data['value']) / 100000000
        _value = UShared.create_table_item(_value_dat)
        _height = UShared.create_table_item(usxo_data['height'])
        _tx_hash = UShared.create_table_item(usxo_data['tx_hash'])

        self.setItem(_r, 0, _wallet)
        self.setItem(_r, 1, _address)
        self.setItem(_r, 2, _address_index)
        self.setItem(_r, 3, _value)
        self.setItem(_r, 4, _ts_pos)
        self.setItem(_r, 5, _tx_hash)
        self.setItem(_r, 6, _height)
