from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared


class _transaction_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['', 'Date', 'Tx', 'Amount',
                                        'Type', 'txid'])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.setColumnHidden(2, True)
        self.setColumnHidden(5, True)
        self.horizontalHeader().setMinimumSectionSize(25)

    def clear_row(self, row):
        self.setRowHidden(row, True)
        # self.cellWidget(row, 0).setHidden(True) #.setCellWidget(_r, 0, _vpic)
        self.item(row, 1).setText('')
        self.item(row, 3).setText('')
        self.item(row, 4).setText('')
        self.item(row, 5).setText('')

    def clear_rows(self):
        for i in range(0, self.rowCount()):
            self.clear_row(i)

    @staticmethod
    def flags():
        return (QtCore.Qt.ItemIsSelectable |
                QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsDragEnabled)

    def add_transactions(self, transactions: list):
        for i in range(0, self.rowCount()):
            self.clear_row(i)

        for c, dat in enumerate(transactions):
            dat['amount'] = round(dat['amount'], 8)
            if dat['amount'] > 0:
                dat['<->'] = 'Receive'
            else:
                dat['<->'] = 'Send'

            if dat['blockhash'] is None:
                dat['<->'] = 'Pending - ' + dat['<->']
            elif dat['confirmations'] < 6:
                _confirming = ('Confirming -' + str(dat['confirmations']))
                dat['<->'] = (_confirming + ' - ' + dat['<->'])

            self._add_transaction(c, dat)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    @staticmethod
    def _create_table_item(text):
        if not isinstance(text, str):
            text = str(text)
        _item = QTableWidgetItem(text)
        _item.setFlags(_transaction_table.flags())
        _item.setForeground(QtCore.Qt.black)

        return _item

    @staticmethod
    def _create_table_item_graphic():
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation
        _pic = QtGui.QPixmap(MShared.get_resource_path('information.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setToolTip('View TX Details')
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)
        _vpic.setProperty('class', 'tblImg')
        return _vpic

    def _add_transaction(self, idx: int, transaction_data: dict):
        if idx == self.rowCount():
            self.insertRow(idx)
            _vpic = self._create_table_item_graphic()
            _date = (self._create_table_item(
                MShared.get_timestamp(transaction_data['time'])[1]))
            _amount = self._create_table_item(str(transaction_data['amount']))
            _direction = self._create_table_item(transaction_data['<->'])
            _txid = self._create_table_item(transaction_data['txid'])
            self.setCellWidget(idx, 0, _vpic)
            self.setItem(idx, 1, _date)
            self.setItem(idx, 3, _amount)
            self.setItem(idx, 4, _direction)
            self.setItem(idx, 5, _txid)
        elif idx <= self.rowCount():
            (self.item(idx, 1).setText(
                MShared.get_timestamp(transaction_data['time'])[1]))
            self.item(idx, 3).setText(str(transaction_data['amount']))
            self.item(idx, 4).setText(transaction_data['<->'])
            self.item(idx, 5).setText(transaction_data['txid'])
            self.setRowHidden(idx, False)
