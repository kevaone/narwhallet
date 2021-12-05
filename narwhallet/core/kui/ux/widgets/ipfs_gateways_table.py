from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


class _ipfs_gateways_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(['', 'Online', 'CORS', 'Origin',
                                        'Host', 'Delay', '', 'Active'])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.setColumnHidden(1, True)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.setColumnHidden(5, True)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    def add_gateway_from_list(self, gateway_data: list):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(self.rowCount())

        _pic = QtGui.QPixmap(MShared.get_resource_path('exclamation.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        _gpic = QtGui.QPixmap(MShared.get_resource_path('gear.png'))
        _gpic = _gpic.scaledToWidth(20, _transm_st)
        _gvpic = QLabel()
        _gvpic.setToolTip('Edit IPFS Gateway')
        _gvpic.setPixmap(_gpic)
        _gvpic.setAlignment(_al_center)
        _gvpic.setContentsMargins(0, 0, 0, 0)

        _dpic = QtGui.QPixmap(MShared.get_resource_path('trashcan.png'))
        _dpic = _dpic.scaledToWidth(20, _transm_st)
        _dellabel = QLabel()
        _dellabel.setToolTip('Delete IPFS Gateway')
        _dellabel.setPixmap(_dpic)
        _dellabel.setAlignment(_al_center)
        _dellabel.setContentsMargins(0, 0, 0, 0)

        self.setCellWidget(_r, 0, _gvpic)
        self.setCellWidget(_r, 1, _vpic)
        self.setItem(_r, 2, QTableWidgetItem(gateway_data[0]))
        self.setItem(_r, 3, QTableWidgetItem(gateway_data[1]))
        self.setItem(_r, 4, QTableWidgetItem(gateway_data[2]))
        self.setItem(_r, 5, QTableWidgetItem('~ms'))
        self.setCellWidget(_r, 6, _dellabel)

        self.resizeColumnsToContents()

    def update_gateway_status(self, row: int, status: str):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _pic = QtGui.QPixmap(MShared.get_resource_path('star.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(row, 1, _vpic)

    def update_active(self, active_row: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        for row in range(0, self.rowCount()):
            self.removeCellWidget(row, 7)

        _pic = QtGui.QPixmap(MShared.get_resource_path('checkmark.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setToolTip('Default IPFS Gateway')
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(active_row, 7, _vpic)
