from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel
from narwhallet.control.shared import MShared

from narwhallet.core.kui.ux.widgets.generator import UShared

class _electrumx_peers_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(10, ['', 'Coin', 'Host', 'Port',
                                       'Type', 'TLS', 'Ping', 'Status',
                                       '', 'Active'], self)
        self.setColumnHidden(1, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)

    def add_peer(self, coin, host, port, tls):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(self.rowCount())

        _pic = QtGui.QPixmap(MShared.get_resource_path('gear.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setToolTip('Edit ElectrumX Peer')
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        _vpic.setProperty('class', 'tblImg')

        _dpic = QtGui.QPixmap(MShared.get_resource_path('trashcan.png'))
        _dpic = _dpic.scaledToWidth(20, _transm_st)
        _dellabel = QLabel()
        _dellabel.setToolTip('Delete ElectrumX Peer')
        _dellabel.setPixmap(_dpic)
        _dellabel.setAlignment(_al_center)
        _dellabel.setContentsMargins(0, 0, 0, 0)
        _dellabel.setProperty('class', 'tblImg')

        if isinstance(tls, bool):
            if tls is True:
                tls = 'True'
            elif tls is False:
                tls = 'False'

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, UShared._create_table_item(coin))
        self.setItem(_r, 2, UShared._create_table_item(host))
        self.setItem(_r, 3, UShared._create_table_item(port))
        self.setItem(_r, 4, UShared._create_table_item('HTTP'))
        self.setItem(_r, 5, UShared._create_table_item(tls))
        self.setItem(_r, 6, UShared._create_table_item('0ms'))
        self.setItem(_r, 7, UShared._create_table_item('disconnected'))
        self.setCellWidget(_r, 8, _dellabel)
        self.resizeColumnsToContents()

    def update_peer_status(self, row: int, status: str):
        self.setItem(row, 7, UShared._create_table_item(status))
        self.resizeColumnsToContents()

    def update_active(self, active_row: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        for row in range(0, self.rowCount()):
            self.removeCellWidget(row, 9)

        _pic = QtGui.QPixmap(MShared.get_resource_path('checkmark.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setToolTip('Default ElectrumX Peer')
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        _vpic.setProperty('class', 'tblImg')
        self.setCellWidget(active_row, 9, _vpic)
        self.resizeColumnsToContents()
