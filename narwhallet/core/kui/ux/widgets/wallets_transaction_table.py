from PyQt5.QtWidgets import QWidget
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.ntablewidget import NTableWidget


class _transaction_table(NTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.set_properties(name)
        self.set_columns(6, ['', 'Date', 'Tx', 'Amount',
                                      'Type', 'txid'])
        self.setColumnHidden(2, True)
        self.setColumnHidden(5, True)

    def add_transactions(self, transactions: list):
        self.clear_rows()
        self.setSortingEnabled(False)
        for c, dat in enumerate(transactions):
            dat['amount'] = round(dat['amount'], 8)
            if dat['amount'] > 0:
                dat['<->'] = 'Receive'
            else:
                dat['<->'] = 'Send'

            if dat['blockhash'] == '':
                dat['<->'] = 'Pending - ' + dat['<->']
            elif dat['confirmations'] < 6:
                _confirming = ('Confirming -' + str(dat['confirmations']))
                dat['<->'] = (_confirming + ' - ' + dat['<->'])

            self._add_transaction(c, dat)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def _add_transaction(self, idx: int, transaction_data: dict):
        if idx == self.rowCount():
            self.insertRow(idx)
            _vpic = UShared.create_table_item_graphic(1)
            _vpic.setToolTip('View Transaction Details')
            _date = (UShared.create_table_item(
                MShared.get_timestamp(transaction_data['time'])[1]))
            _amount = UShared.create_table_item(transaction_data['amount'])
            _direction = UShared.create_table_item(transaction_data['<->'])
            _txid = UShared.create_table_item(transaction_data['txid'])
            self.setCellWidget(idx, 0, _vpic)
            self.setItem(idx, 0, UShared.create_table_item(''))
            self.setItem(idx, 1, _date)
            self.setItem(idx, 2, UShared.create_table_item(''))
            self.setItem(idx, 3, _amount)
            self.setItem(idx, 4, _direction)
            self.setItem(idx, 5, _txid)
        elif idx <= self.rowCount():
            (self.set_text(idx, 1,
                MShared.get_timestamp(transaction_data['time'])[1]))
            self.set_text(idx, 3, str(transaction_data['amount']))
            self.set_text(idx, 4, transaction_data['<->'])
            self.set_text(idx, 5, transaction_data['txid'])
            self.setRowHidden(idx, False)
