from typing import List
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QLabel, QSizePolicy, QSpacerItem)
from narwhallet.control.shared import MShared


class HLSection(QHBoxLayout):
    def __init__(self, label: str, widgets):
        super().__init__()

        self.label = QLabel()
        self.label.setText(label)
        self.widgets = []
        self.addWidget(self.label)
        if isinstance(widgets, list):
            for _w in widgets:
                self.widgets.append(_w)
                self.addWidget(self.widgets[-1])
        elif widgets is not None:
            self.widgets.append(widgets)
            self.addWidget(self.widgets[-1])
        # self.addItem(QSpacerItem(0, 0, QSizePolicy.MinimumExpanding,
        #                          QSizePolicy.Minimum))


class UShared():
    @staticmethod
    def dialog_header_graphic():
        _label = QLabel()
        _pic = QPixmap(MShared.get_resource_path('narwhal.png'))
        _label.setAlignment(QtCore.Qt.AlignCenter)
        _label.setContentsMargins(0, 0, 0, 0)
        _label.setPixmap(_pic)

        return _label

    @staticmethod
    def set_table_properties(table: QTableWidget, name: str):
        table.setObjectName(name)
        table.setSelectionBehavior(table.SelectRows)
        table.setSelectionMode(table.SingleSelection)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)

    @staticmethod
    def set_table_columns(columns, headers: List[str], table: QTableWidget):
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        for c in range(0, columns):
            table.horizontalHeaderItem(c).setTextAlignment(4)
        table.horizontalHeader().setMinimumSectionSize(5)

    @staticmethod
    def remove_table_rows(table: QTableWidget):
        _m = table.rowCount()

        while _m > -1:
            table.removeRow(_m)
            _m = _m - 1

    @staticmethod
    def clear_table_row(table: QTableWidget, row: int):
        table.setRowHidden(row, True)
        for c in range(0, table.columnCount()):
            table.item(row, c).setText('')

    @staticmethod
    def clear_table_rows(table: QTableWidget):
        for i in range(0, table.rowCount()):
            UShared.clear_table_row(table, i)

    @staticmethod
    def set_table_row_color(table: QTableWidget, row: int, color: QColor):
        for c in range(0, table.columnCount()):
            table.item(row, c).setBackground(color)

    @staticmethod
    def create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _vpic = QLabel()

        if pic == 0:
            _p = QPixmap(MShared.get_resource_path('keva-logo.png'))
        if pic == 1:
            _p = QPixmap(MShared.get_resource_path('information'))
        elif pic == 2:
            _p = QPixmap(MShared.get_resource_path('clipboard.png'))
        elif pic == 3:
            _p = QPixmap(MShared.get_resource_path('trashcan.png'))
        elif pic == 4:
            _p = QPixmap(MShared.get_resource_path('star.png'))
        elif pic == 5:
            _p = QPixmap(MShared.get_resource_path('medal2.png'))
        elif pic == 6:
            _p = QPixmap(MShared.get_resource_path('locked.png'))
        elif pic == 7:
            _p = QPixmap(MShared.get_resource_path('unlocked.png'))
        elif pic == 8:
            _p = QPixmap(MShared.get_resource_path('transfer.png'))
        elif pic == 9:
            _p = QPixmap(MShared.get_resource_path('checkmark.png'))
        elif pic == 10:
            _p = QPixmap(MShared.get_resource_path('exclamation.png'))
        elif pic == 11:
            _p = QPixmap(MShared.get_resource_path('gear.png'))
        elif pic == 12:
            _p = QPixmap(MShared.get_resource_path('return.png'))

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
