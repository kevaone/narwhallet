import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from control.shared import MShared


class _auctions_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(['', 'Date', 'Wallet', 'Shortcode',
                                        'Asking', 'Bids', 'High Bid', '', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeaderItem(8).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)
        self.setColumnWidth(0, 20)
        self.setColumnWidth(7, 20)
        self.setColumnHidden(8, True)

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

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_auctions(self, wallet: str, auctions: list):
        for auction in auctions:
            _d = {}
            _d['date'] = auction[0]
            _d['wallet'] = wallet
            _d['shortcode'] = auction[1]
            _d['asking'] = auction[2]
            _d['bids'] = auction[3]
            _d['high_bid'] = auction[4]
            _d['tx'] = auction[5]
            self._add_auction(_d)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_auction(self, auction_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = self._create_table_item_graphic(0)
        _date = (self._create_table_item(
            MShared.get_timestamp(auction_data['date'])[1]))
        _wallet = self._create_table_item(auction_data['wallet'])
        _shortcode = self._create_table_item(str(auction_data['shortcode']))
        _asking = self._create_table_item(str(auction_data['asking']))
        _bids = self._create_table_item(auction_data['bids'])
        _high_bid = self._create_table_item(auction_data['high_bid'])
        _auc_tx = self._create_table_item(auction_data['tx'])

        self.setCellWidget(_r, 0, _coin)
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _asking)
        self.setItem(_r, 5, _bids)
        self.setItem(_r, 6, _high_bid)
        self.setItem(_r, 8, _auc_tx)
        # self.setCellWidget(_r, 7, _dellabel)
