from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared


class _auctions_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        UShared.set_table_columns(10, ['', 'Date', 'Wallet', 'Shortcode',
                                       'Asking', 'Bids', 'High Bid', '',
                                       '', ''], self)
        self.setColumnWidth(0, 20)
        self.setColumnWidth(7, 20)
        self.setColumnHidden(8, True)
        self.setColumnHidden(9, True)

    def add_auctions(self, wallet: str, auctions: list):
        self.setSortingEnabled(False)
        for auction in auctions:
            _d = {}
            _d['date'] = auction[0]
            _d['wallet'] = wallet
            _d['shortcode'] = auction[1]
            _d['asking'] = auction[2]
            _d['bids'] = auction[3]
            _d['high_bid'] = auction[4]
            _d['ns'] = auction[5]
            _d['tx'] = auction[6]
            self._add_auction(_d)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_auction(self, auction_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = UShared.create_table_item_graphic(0)
        _date = (UShared.create_table_item(
            MShared.get_timestamp(auction_data['date'])[1]))
        _wallet = UShared.create_table_item(auction_data['wallet'])
        _shortcode = UShared.create_table_item(auction_data['shortcode'])
        _asking = UShared.create_table_item(auction_data['asking'])
        _bids = UShared.create_table_item(auction_data['bids'])
        _high_bid = UShared.create_table_item(auction_data['high_bid'])
        _auc_ns = UShared.create_table_item(auction_data['ns'])
        _auc_tx = UShared.create_table_item(auction_data['tx'])

        self.setCellWidget(_r, 0, _coin)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setItem(_r, 1, _date)
        self.setItem(_r, 2, _wallet)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _asking)
        self.setItem(_r, 5, _bids)
        self.setItem(_r, 6, _high_bid)
        self.setItem(_r, 8, _auc_ns)
        self.setItem(_r, 9, _auc_tx)
