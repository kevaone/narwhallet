from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from narwhallet.control.shared import MShared

from narwhallet.core.kui.ux.widgets.generator import UShared

class _namespaces_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(8, ['', 'Date', 'Wallet',
                                      'Shortcode', 'Keys',
                                      'NamespaceId', 'Address', ''], self)
        self.setColumnHidden(1, True)
        # TODO Add settings control to show/hide address column
        self.setColumnHidden(6, True)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

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

        _date = UShared.create_table_item(MShared.get_timestamp(namespace_data['date'])[1])
        # _date = (QTableWidgetItem(
        #     MShared.get_timestamp(namespace_data['date'])[1], 0))
        # _date.setFlags(UShared.flags())
        # _date.setForeground(QtCore.Qt.black)

        _wallet = UShared.create_table_item(namespace_data['wallet'])
        # _wallet = QTableWidgetItem(namespace_data['wallet'])
        # _wallet.setFlags(UShared.flags())
        # _wallet.setForeground(QtCore.Qt.black)

        _namespaceid = UShared.create_table_item(namespace_data['namespaceid'])
        # _namespaceid = QTableWidgetItem(namespace_data['namespaceid'])
        # _namespaceid.setFlags(UShared.flags())
        # _namespaceid.setForeground(QtCore.Qt.black)

        _shortcode = UShared.create_table_item(namespace_data['shortcode'])
        # _shortcode = QTableWidgetItem(str(namespace_data['shortcode']))
        # _shortcode.setFlags(UShared.flags())
        # _shortcode.setForeground(QtCore.Qt.black)

        _keys = UShared.create_table_item(namespace_data['key_count'])
        # _keys = QTableWidgetItem(str(namespace_data['key_count']))
        # _keys.setFlags(UShared.flags())
        # _keys.setForeground(QtCore.Qt.black)

        _address = UShared.create_table_item(namespace_data['address'])
        # _address = QTableWidgetItem(namespace_data['address'])
        # _address.setFlags(UShared.flags())
        # _address.setForeground(QtCore.Qt.black)

        _dellabel = UShared.create_table_item_graphic(8)
        _dellabel.setToolTip('Transfer Namespace')

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _keys)
        self.setItem(_r, 5, _namespaceid)
        self.setItem(_r, 6, _address)
        self.setCellWidget(_r, 7, _dellabel)
