import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from control.shared import MShared


class _bids_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(11)
        self.setHorizontalHeaderLabels(['', 'Date', 'Wallet', 'Bid From',
                                        'Bid On', 'Asking', 'High Bid',
                                        'Your Bid', 'Is High Bid', '', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeaderItem(8).setTextAlignment(4)
        self.horizontalHeaderItem(9).setTextAlignment(4)
        self.horizontalHeaderItem(10).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)
        self.setColumnWidth(0, 20)
        self.setColumnWidth(8, 20)
        self.setColumnHidden(10, True)

    @staticmethod
    def _create_table_item(text):
        _if_iied = QtCore.Qt.ItemIsEditable
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iide = QtCore.Qt.ItemIsDragEnabled

        if not isinstance(text, str):
            text = str(text)
        _item = QTableWidgetItem(text)
        _item.setFlags(_if_iied | _if_iis | _if_iide)
        _item.setForeground(QtCore.Qt.black)

        return _item

    @staticmethod
    def _create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation
        __path = os.path.dirname(__file__)
        if pic == 0:
            _p = QtGui.QPixmap(os.path.join(__path, '../assets/keva-logo.png'))
        elif pic == 1:
            _p = QtGui.QPixmap(os.path.join(__path, '../assets/clipboard.png'))
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

    def add_bids(self, wallet: str, bids: list):
        for bid in bids:
            _d = {}
            _d['date'] = bid[0]
            _d['wallet'] = wallet
            _d['from_shortcode'] = bid[1]
            _d['to_shortcode'] = bid[2]
            _d['asking'] = bid[3]
            _d['high_bid'] = bid[4]
            _d['your_bid'] = bid[5]
            _d['tx'] = bid[6]

            self._add_bid(_d)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_bid(self, bid_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = self._create_table_item_graphic(0)
        _date = (self._create_table_item(
            MShared.get_timestamp(bid_data['date'])[1]))
        _wallet = self._create_table_item(bid_data['wallet'])
        _from_shortcode = (self._create_table_item(
            str(bid_data['from_shortcode'])))
        _to_shortcode = self._create_table_item(str(bid_data['to_shortcode']))
        _asking = self._create_table_item(str(bid_data['asking']))
        _high_bid = self._create_table_item(str(bid_data['high_bid']))
        _your_bid = self._create_table_item(str(bid_data['your_bid']))
        _is_high_bid = (self._create_table_item(
            str(bid_data['your_bid'] >= bid_data['high_bid'])))
        _auc_tx = self._create_table_item(str(bid_data['tx']))
        _empty_item = self._create_table_item('')
        _empty_item2 = self._create_table_item('')

        self.setCellWidget(_r, 0, _coin)
        self.setItem(_r, 0, _empty_item)
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _from_shortcode)
        self.setItem(_r, 4, _to_shortcode)
        self.setItem(_r, 5, _asking)
        self.setItem(_r, 6, _high_bid)
        self.setItem(_r, 7, _your_bid)
        self.setItem(_r, 8, _is_high_bid)
        self.setItem(_r, 9, _empty_item2)
        self.setItem(_r, 10, _auc_tx)
        # self.setCellWidget(_r, 7, _dellabel)
