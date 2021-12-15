from typing import List
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


class UShared():
    @staticmethod
    def set_table_columns(columns, headers: List[str], table: QTableWidget):
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        for c in range(0, columns):
            table.horizontalHeaderItem(c).setTextAlignment(4)
        table.horizontalHeader().setMinimumSectionSize(5)

    @staticmethod
    def create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _vpic = QLabel()

        if pic == 0:
            _p = QPixmap(MShared.get_resource_path('keva-logo.png'))
        if pic == 1:
            _p = QPixmap(MShared.get_resource_path('information'))
            _vpic.setToolTip('View Address Details')
        elif pic == 2:
            _p = QPixmap(MShared.get_resource_path('clipboard.png'))
            _vpic.setToolTip('Copy Address to Clipboard')
        elif pic == 3:
            _p = QPixmap(MShared.get_resource_path('trashcan.png'))
            _vpic.setToolTip('Delete Adderess From Address Book')
        elif pic == 4:
            _p = QPixmap(MShared.get_resource_path('star.png'))
            _vpic.setToolTip('Read-Only Wallet')
        elif pic == 5:
            _p = QPixmap(MShared.get_resource_path('medal2.png'))
        elif pic == 6:
            _p = QPixmap(MShared.get_resource_path('locked.png'))
            _vpic.setToolTip('Wallet is Locked')
        elif pic == 7:
            _p = QPixmap(MShared.get_resource_path('unlocked.png'))
            _vpic.setToolTip('Wallet is Unlocked')
        elif pic == 8:
            _p = QPixmap(MShared.get_resource_path('transfer.png'))
        elif pic == 9:
            _p = QPixmap(MShared.get_resource_path('checkmark.png'))
            _vpic.setToolTip('Valid Bid')
        elif pic == 10:
            _p = (QPixmap(MShared.get_resource_path('exclamation.png')))
            _vpic.setToolTip('Invalid Bid')

        _p = _p.scaledToWidth(20, _transm_st)

        _p = _p.scaledToWidth(20, _transm_st)

        _vpic.setPixmap(_p)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        _vpic.setProperty('class', 'tblImg')
        return _vpic

    @staticmethod
    def flags():
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        # return (QtCore.Qt.ItemIsSelectable |
        #         QtCore.Qt.ItemIsEditable |
        #         QtCore.Qt.ItemIsDragEnabled)

    @staticmethod
    def create_table_item(text):
        if not isinstance(text, str):
            text = str(text)
        _item = QTableWidgetItem(text)
        _item.setFlags(UShared.flags())
        _item.setForeground(QtCore.Qt.black)

        return _item
#########

