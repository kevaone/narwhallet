import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from control.shared import MShared


class _namespaces_table(QTableWidget):
    def __init__(self, name: str, QWidget):
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

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_namespaces(self, wallet: str, namespaces: list):
        for i in namespaces:
            if i['wallet'] != 'live':
                self._add_namespace(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_namespace(self, namespace_data: dict):
        _al_center = QtCore.Qt.AlignCenter
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iie = QtCore.Qt.ItemIsEnabled
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(_r)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/information.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        _date = QTableWidgetItem(MShared.get_timestamp(namespace_data['date'])[1], 0)
        _date.setFlags(_if_iie | _if_iis)
        _date.setForeground(QtCore.Qt.black)

        _wallet = QTableWidgetItem(namespace_data['wallet'])
        _wallet.setFlags(_if_iie | _if_iis)
        _wallet.setForeground(QtCore.Qt.black)

        _namespaceid = QTableWidgetItem(namespace_data['namespaceid'])
        _namespaceid.setFlags(_if_iie | _if_iis)
        _namespaceid.setForeground(QtCore.Qt.black)

        _shortcode = QTableWidgetItem(str(namespace_data['shortcode']))
        _shortcode.setFlags(_if_iie | _if_iis)
        _shortcode.setForeground(QtCore.Qt.black)

        _keys = QTableWidgetItem(str(namespace_data['key_count']))
        _keys.setFlags(_if_iie | _if_iis)
        _keys.setForeground(QtCore.Qt.black)

        _address = QTableWidgetItem(namespace_data['address'])
        _address.setFlags(_if_iie | _if_iis)
        _address.setForeground(QtCore.Qt.black)

        _dpic = QtGui.QPixmap(os.path.join(__path, '../assets/transfer.png'))
        _dpic = _dpic.scaledToWidth(20, _transm_st)
        _dellabel = QLabel()
        _dellabel.setPixmap(_dpic)
        _dellabel.setAlignment(_al_center)
        _dellabel.setContentsMargins(0, 0, 0, 0)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _keys)
        self.setItem(_r, 5, _namespaceid)
        self.setItem(_r, 6, _address)
        self.setCellWidget(_r, 7, _dellabel)
