from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.control.shared import MShared

from narwhallet.core.kui.ux.widgets.generator import UShared

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
        UShared.set_table_columns(12, ['', 'Date', 'Wallet', 'Bid From',
                                       'Bid On', 'Asking', 'High Bid',
                                       'Your Bid', 'Is High Bid', '', '',
                                       ''], self)
        self.setColumnWidth(0, 20)
        self.setColumnWidth(8, 20)
        self.setColumnHidden(10, True)
        self.setColumnHidden(11, True)

    def set_row_color(self, row: int, color=QtCore.Qt.red):
        for _column in range(0, self.columnCount()-1):
            self.item(row, _column).setBackground(color)

    def clear_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def add_bids(self, wallet: str, bids: list):
        self.setSortingEnabled(False)
        for bid in bids:
            _d = {}
            _d['date'] = bid[0]
            _d['wallet'] = wallet
            _d['from_shortcode'] = bid[1]
            _d['to_shortcode'] = bid[2]
            _d['asking'] = bid[3]
            _d['high_bid'] = bid[4]
            _d['your_bid'] = bid[5]
            _d['ns'] = bid[6]
            _d['tx'] = bid[7]

            self._add_bid(_d)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_bid(self, bid_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = UShared.create_table_item_graphic(0)
        _date = (UShared.create_table_item(
            MShared.get_timestamp(bid_data['date'])[1]))
        _wallet = UShared.create_table_item(bid_data['wallet'])
        _from_shortcode = (UShared.create_table_item(
            str(bid_data['from_shortcode'])))
        _to_shortcode = UShared.create_table_item(bid_data['to_shortcode'])
        _asking = UShared.create_table_item(bid_data['asking'])
        _high_bid = UShared.create_table_item(bid_data['high_bid'])
        _your_bid = UShared.create_table_item(bid_data['your_bid'])
        _is_high_bid = (UShared.create_table_item(
            str(bid_data['your_bid'] >= bid_data['high_bid'])))
        _auc_ns = UShared.create_table_item(bid_data['ns'])
        _auc_tx = UShared.create_table_item(bid_data['tx'])
        _empty_item = UShared.create_table_item('')
        _empty_item2 = UShared.create_table_item('')

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
        self.setItem(_r, 10, _auc_ns)
        self.setItem(_r, 11, _auc_tx)
        # self.setCellWidget(_r, 7, _dellabel)
