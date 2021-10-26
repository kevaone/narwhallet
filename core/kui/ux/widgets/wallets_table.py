import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from control.shared import MShared
from core.kcl.models.wallet import MWallet


class animation_label(QLabel):
    def __init__(self):
        super().__init__()

        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        __path = os.path.dirname(__file__)
        self._upic = QPixmap(os.path.join(__path, '../assets/return.png'))
        self._upic = self._upic.scaledToWidth(20, _transm_st)
        self.setPixmap(self._upic)
        self.setAlignment(_al_center)
        self.setContentsMargins(0, 0, 0, 0)

        self.ani = QtCore.QVariantAnimation()
        self.ani.setDuration(1000)

        self.ani.setStartValue(0.0)
        self.ani.setEndValue(360.0)
        self.ani.setLoopCount(300)
        self.ani.valueChanged.connect(self.animate)

    def animate(self, value):
        _transm_st = QtCore.Qt.SmoothTransformation

        t = QTransform()
        t.rotate(value)
        self.setPixmap(self._upic.transformed(t, _transm_st))


class _wallets_table(QTableWidget):
    def __init__(self, name: str, QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(['', 'Locked', 'Coin', 'Name',
                                        'Type', 'Kind', 'Balance',
                                        'Last Updated', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.setColumnHidden(2, True)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeaderItem(8).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    def add_wallet(self, wallet_data: dict):
        _al_center = QtCore.Qt.AlignCenter
        _if_iis = QtCore.Qt.ItemIsSelectable
        _if_iie = QtCore.Qt.ItemIsEnabled
        _transm_st = QtCore.Qt.SmoothTransformation

        _r = self.rowCount()
        self.insertRow(_r)
        __path = os.path.dirname(__file__)
        _pic = QPixmap(os.path.join(__path, '../assets/keva-logo.png'))
        _pic = _pic.scaledToWidth(20, _transm_st)
        _vpic = QLabel()
        _vpic.setPixmap(_pic)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        _coin = QTableWidgetItem(wallet_data['coin'])
        _coin.setFlags(_if_iie | _if_iis)
        _coin.setForeground(QtCore.Qt.black)

        _name = QTableWidgetItem(wallet_data['name'])
        _name.setFlags(_if_iie | _if_iis)
        _name.setForeground(QtCore.Qt.black)

        _wtype = QTableWidgetItem(wallet_data['bip'])
        _wtype.setFlags(_if_iie | _if_iis)
        _wtype.setForeground(QtCore.Qt.black)

        _kvpic = QLabel()
        _kvpic.setAlignment(_al_center)
        _kvpic.setContentsMargins(0, 0, 0, 0)
        if wallet_data['kind'] != 0:
            if wallet_data['kind'] == 1:
                _kpic = QPixmap(os.path.join(__path, '../assets/star.png'))
            elif wallet_data['kind'] == 2:
                _kpic = QPixmap(os.path.join(__path, '../assets/medal2.png'))
            elif wallet_data['kind'] == 3:
                _kpic = QPixmap(os.path.join(__path, '../assets/star.png'))
            _kpic = _kpic.scaledToWidth(20, _transm_st)
            _kvpic.setPixmap(_kpic)

        wallet_data['balance'] = round(wallet_data['balance'], 8)
        _balance = QTableWidgetItem(str(wallet_data['balance']))
        _balance.setFlags(_if_iie | _if_iis)
        _balance.setForeground(QtCore.Qt.black)

        if wallet_data['locked'] is True:
            _lpic = QPixmap(os.path.join(__path, '../assets/locked.png'))
        else:
            _lpic = QPixmap(os.path.join(__path, '../assets/unlocked.png'))
        _lpic = _lpic.scaledToWidth(20, _transm_st)
        _lvpic = QLabel()
        _lvpic.setAlignment(_al_center)
        _lvpic.setContentsMargins(0, 0, 0, 0)

        if wallet_data['state_lock'] != 0:
            _lvpic.setPixmap(_lpic)

        _upd = '-'

        if 'last_updated' in wallet_data:
            if wallet_data['last_updated'] is not None:
                _time_stamp = wallet_data['last_updated']
                _upd = MShared.get_timestamp(_time_stamp)[1]

        _updated = QTableWidgetItem(_upd)
        _updated.setFlags(_if_iie | _if_iis)
        _updated.setForeground(QtCore.Qt.black)

        _synch = QTableWidgetItem('')
        _synch.setFlags(_if_iie | _if_iis)
        _synch.setForeground(QtCore.Qt.black)

        self._vupic = animation_label()

        self.setCellWidget(_r, 0, _vpic)
        self.setCellWidget(_r, 1, _lvpic)
        self.setItem(_r, 2, _coin)
        self.setItem(_r, 3, _name)
        self.setItem(_r, 4, _wtype)
        self.setCellWidget(_r, 5, _kvpic)
        self.setItem(_r, 6, _balance)
        self.setItem(_r, 7, _updated)
        self.setItem(_r, 8, _synch)
        self.setCellWidget(_r, 8, self._vupic)
        self.resizeColumnsToContents()

    def update_wallet(self, _w: MWallet, row: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation
        __path = os.path.dirname(__file__)
        if _w.locked is True:
            _lpic = QPixmap(os.path.join(__path, '../assets/locked.png'))
        else:
            _lpic = QPixmap(os.path.join(__path, '../assets/unlocked.png'))
        _lpic = _lpic.scaledToWidth(20, _transm_st)
        _lvpic = QLabel()
        _lvpic.setPixmap(_lpic)
        _lvpic.setAlignment(_al_center)
        _lvpic.setContentsMargins(0, 0, 0, 0)

        _kvpic = QLabel()
        _kvpic.setAlignment(_al_center)
        _kvpic.setContentsMargins(0, 0, 0, 0)
        if _w.kind != 0 and _w.kind is not None:
            if _w.kind == 1:
                _kpic = QPixmap(os.path.join(__path, '../assets/star.png'))
            elif _w.kind == 2:
                _kpic = QPixmap(os.path.join(__path, '../assets/medal2.png'))
            _kpic = _kpic.scaledToWidth(20, _transm_st)
            _kvpic.setPixmap(_kpic)

        if _w.last_updated is not None:
            _upd = MShared.get_timestamp(_w.last_updated)[1]
        else:
            _upd = '-'

        self.setCellWidget(row, 1, _lvpic)
        self.item(row, 2).setText(_w.coin)
        self.item(row, 4).setText(_w.bip)
        self.setCellWidget(row, 5, _kvpic)
        self.item(row, 6).setText(str(_w.balance))

        self.item(row, 7).setText(_upd)
        self.resizeColumnsToContents()
