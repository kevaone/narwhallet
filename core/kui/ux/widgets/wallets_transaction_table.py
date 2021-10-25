import datetime
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class _transaction_table(QTableWidget):
    def __init__(self, name: str, QWidget):
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

    def add_transactions(self, transactions: list):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

        for i in transactions:
            i['amount'] = round(i['amount'], 8)
            if i['amount'] > 0:
                i['<->'] = 'Receive'
            else:
                i['<->'] = 'Send'

            if i['blockhash'] is None:
                i['<->'] = 'Pending - ' + i['<->']
            elif i['confirmations'] < 6:
                _confirming = 'Confirming -' + str(i['confirmations'])
                i['<->'] = _confirming + ' - ' + i['<->']

            self._add_transaction(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def time_to_str(self, time):
        _d = (datetime.datetime
              .fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
        return _d

    def _add_transaction(self, transaction_data: dict):
        _al_center = QtCore.Qt.AlignCenter
        _if_iied = QtCore.Qt.ItemIsEditable
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iide = QtCore.Qt.ItemIsDragEnabled
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(_r)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/information.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)

        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        _date = QTableWidgetItem(self.time_to_str(transaction_data['time']))
        _date.setFlags(_if_iied | _if_iis | _if_iide)
        _date.setForeground(QtCore.Qt.black)

        _amount = QTableWidgetItem(str(transaction_data['amount']))
        _amount.setFlags(_if_iied | _if_iis | _if_iide)
        _amount.setForeground(QtCore.Qt.black)

        _direction = QTableWidgetItem(transaction_data['<->'])
        _direction.setFlags(_if_iied | _if_iis | _if_iide)
        _direction.setForeground(QtCore.Qt.black)

        _txid = QTableWidgetItem(transaction_data['txid'])
        _txid.setFlags(_if_iied | _if_iis | _if_iide)
        _txid.setForeground(QtCore.Qt.black)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 1, QTableWidgetItem(_date))
        self.setItem(_r, 3, QTableWidgetItem(_amount))
        self.setItem(_r, 4, QTableWidgetItem(_direction))
        self.setItem(_r, 5, QTableWidgetItem(_txid))
