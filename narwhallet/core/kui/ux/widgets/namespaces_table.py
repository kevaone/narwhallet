from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


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
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(['', 'Date', 'Wallet', 'Shortcode',
                                        'Keys', 'NamespaceId', 'Address', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)
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

    @staticmethod
    def _create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        if pic == 0:
            _p = QPixmap(MShared.get_resource_path('information.png'))
        elif pic == 1:
            _p = QPixmap(MShared.get_resource_path('transfer.png'))
        _p = _p.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setPixmap(_p)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        return _vpic

    @staticmethod
    def flags():
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def _add_namespace(self, namespace_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)
        _vpic = self._create_table_item_graphic(0)

        _date = (QTableWidgetItem(
            MShared.get_timestamp(namespace_data['date'])[1], 0))
        _date.setFlags(self.flags())
        _date.setForeground(QtCore.Qt.black)

        _wallet = QTableWidgetItem(namespace_data['wallet'])
        _wallet.setFlags(self.flags())
        _wallet.setForeground(QtCore.Qt.black)

        _namespaceid = QTableWidgetItem(namespace_data['namespaceid'])
        _namespaceid.setFlags(self.flags())
        _namespaceid.setForeground(QtCore.Qt.black)

        _shortcode = QTableWidgetItem(str(namespace_data['shortcode']))
        _shortcode.setFlags(self.flags())
        _shortcode.setForeground(QtCore.Qt.black)

        _keys = QTableWidgetItem(str(namespace_data['key_count']))
        _keys.setFlags(self.flags())
        _keys.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(namespace_data['address'])
        _address.setFlags(self.flags())
        _address.setForeground(QtCore.Qt.black)

        _dellabel = self._create_table_item_graphic(1)
        _dellabel.setToolTip('Transfer Namespace')

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _keys)
        self.setItem(_r, 5, _namespaceid)
        self.setItem(_r, 6, _address)
        self.setCellWidget(_r, 7, _dellabel)
