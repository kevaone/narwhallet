from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


class _bid_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['', '', 'Date', 'Shortcode',
                                        'Bid', '', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)
        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 20)
        self.setColumnWidth(4, 20)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)

    @staticmethod
    def flags():
        return (QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsDragEnabled)

    @staticmethod
    def _create_table_item(text):
        if not isinstance(text, str):
            text = str(text)
        _item = QTableWidgetItem(text)
        _item.setFlags(_bid_table.flags())
        _item.setForeground(QtCore.Qt.black)

        return _item

    @staticmethod
    def _create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        if pic == 0:
            _p = QtGui.QPixmap(MShared.get_resource_path('keva-logo.png'))
        elif pic == 1:
            _p = QtGui.QPixmap(MShared.get_resource_path('checkmark.png'))
        elif pic == 2:
            _p = (QtGui.QPixmap(MShared.get_resource_path('exclamation.png')))
        elif pic == 3:
            _p = QtGui.QPixmap(MShared.get_resource_path('medal2.png'))
        _p = _p.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setPixmap(_p)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        return _vpic

    def set_row_color(self, row: int, color=QtCore.Qt.red):
        for _column in range(0, self.columnCount()-1):
            self.item(row, _column).setBackground(color)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_bids(self, bids: list):
        for bid in bids:
            _d = {}
            _d['date'] = bid[0]
            _d['shortcode'] = bid[1]
            _d['bid'] = bid[2]
            _d['valid'] = bid[3]
            _d['bid_tx'] = bid[4]

            self._add_bid(_d)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)
        self.setColumnWidth(5, 20)

    def _add_bid(self, bid_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = self._create_table_item_graphic(0)
        if bid_data['valid'] is True:
            _valid = self._create_table_item_graphic(1)
        else:
            _valid = self._create_table_item_graphic(2)

        _accept = self._create_table_item_graphic(3)
        _date = (self._create_table_item(
            MShared.get_timestamp(bid_data['date'])[1]))
        _shortcode = self._create_table_item(str(bid_data['shortcode']))
        _bid = self._create_table_item(str(bid_data['bid']))
        _empty_item = self._create_table_item('')
        _empty_item2 = self._create_table_item('')
        _empty_item3 = self._create_table_item('')
        _bid_tx = self._create_table_item(bid_data['bid_tx'])

        self.setCellWidget(_r, 0, _coin)
        self.setItem(_r, 0, _empty_item)
        self.setCellWidget(_r, 1, _valid)
        self.setItem(_r, 1, _empty_item2)
        self.setItem(_r, 2, _date)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _bid)
        self.setItem(_r, 5, _empty_item3)
        if bid_data['valid'] is True:
            self.setCellWidget(_r, 5, _accept)
        self.setItem(_r, 6, _bid_tx)