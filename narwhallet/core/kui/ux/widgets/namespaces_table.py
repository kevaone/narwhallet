from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared


class _namespaces_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        UShared.set_table_properties(self, name)
        UShared.set_table_columns(8, ['', 'Date', 'Wallet',
                                      'Shortcode', 'Keys',
                                      'NamespaceId', 'Address', ''], self)
        self.setColumnHidden(1, True)
        # TODO Add settings control to show/hide address column
        self.setColumnHidden(6, True)

    def add_namespaces(self, wallet: str, namespaces: list):
        self.setSortingEnabled(False)
        for i in namespaces:
            if i['wallet'] != 'live':
                self._add_namespace(i)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_namespace(self, namespace_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)
        _vpic = UShared.create_table_item_graphic(1)
        _vpic.setToolTip('View Namespace Details')
        _date = MShared.get_timestamp(namespace_data['date'])[1]
        _date = UShared.create_table_item(_date)
        _wallet = UShared.create_table_item(namespace_data['wallet'])
        _namespaceid = UShared.create_table_item(namespace_data['namespaceid'])
        _shortcode = UShared.create_table_item(namespace_data['shortcode'])
        _keys = UShared.create_table_item(namespace_data['key_count'])
        _address = UShared.create_table_item(namespace_data['address'])
        _dellabel = UShared.create_table_item_graphic(8)
        _dellabel.setToolTip('Transfer Namespace')

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _keys)
        self.setItem(_r, 5, _namespaceid)
        self.setItem(_r, 6, _address)
        self.setCellWidget(_r, 7, _dellabel)
        self.setItem(_r, 7, UShared.create_table_item(''))
