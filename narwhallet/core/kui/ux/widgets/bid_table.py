from PyQt5.QtWidgets import QWidget
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.ntablewidget import NTableWidget


class _bid_table(NTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.set_properties(name)
        self.set_columns(7, ['', '', 'Date', 'Shortcode',
                                      'Bid', '', ''])
        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 20)
        self.setColumnWidth(4, 20)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)

    def add_bids(self, bids: list):
        self.setSortingEnabled(False)
        for bid in bids:
            _d = {}
            _d['date'] = bid[0]
            _d['shortcode'] = bid[1]
            _d['bid'] = bid[2]
            _d['valid'] = bid[3]
            _d['bid_tx'] = bid[4]

            self._add_bid(_d)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)
        self.setColumnWidth(5, 20)

    def _add_bid(self, bid_data: dict):
        _r = self.rowCount()
        self.insertRow(_r)

        _coin = UShared.create_table_item_graphic(0)
        if bid_data['valid'] is True:
            _valid = UShared.create_table_item_graphic(9)
            _valid.setToolTip('Valid Bid, Click to Accept')
        else:
            _valid = UShared.create_table_item_graphic(10)
            _valid.setToolTip('Invalid Bid')

        _accept = UShared.create_table_item_graphic(5)
        _date = (UShared.create_table_item(
            MShared.get_timestamp(bid_data['date'])[1]))
        _shortcode = UShared.create_table_item(bid_data['shortcode'])
        _bid = UShared.create_table_item(bid_data['bid'])
        _bid_tx = UShared.create_table_item(bid_data['bid_tx'])

        self.setCellWidget(_r, 0, _coin)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setCellWidget(_r, 1, _valid)
        self.setItem(_r, 1, UShared.create_table_item(''))
        self.setItem(_r, 2, _date)
        self.setItem(_r, 3, _shortcode)
        self.setItem(_r, 4, _bid)
        self.setItem(_r, 5, UShared.create_table_item(''))
        if bid_data['valid'] is True:
            self.setCellWidget(_r, 5, _accept)
        self.setItem(_r, 6, _bid_tx)
