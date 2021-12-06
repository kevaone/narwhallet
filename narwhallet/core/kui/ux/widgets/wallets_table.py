from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.models.wallet import MWallet


class animation_label(QLabel):
    def __init__(self):
        super().__init__()

        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        self._upic = QPixmap(MShared.get_resource_path('return.png'))
        self._upic = self._upic.scaledToWidth(20, _transm_st)
        self.setPixmap(self._upic)
        self.setAlignment(_al_center)
        self.setContentsMargins(0, 0, 0, 0)
        self.setToolTip('Refresh Wallet')

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
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.build_columns()

    def build_columns(self):
        self.setColumnCount(10)
        self.setHorizontalHeaderLabels(['', 'Locked', 'Coin', 'Name',
                                        'Type', 'Kind', 'Balance',
                                        'Bid Locked', 'Last Updated', ''])
        self.horizontalHeaderItem(0).setTextAlignment(4)
        self.setColumnHidden(2, True)
        self.horizontalHeaderItem(1).setTextAlignment(4)
        self.horizontalHeaderItem(2).setTextAlignment(4)
        self.horizontalHeaderItem(3).setTextAlignment(4)
        self.horizontalHeaderItem(4).setTextAlignment(4)
        self.setColumnHidden(4, True)
        self.horizontalHeaderItem(5).setTextAlignment(4)
        self.horizontalHeaderItem(6).setTextAlignment(4)
        self.horizontalHeaderItem(7).setTextAlignment(4)
        self.horizontalHeaderItem(8).setTextAlignment(4)
        self.horizontalHeaderItem(9).setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(25)

    @staticmethod
    def _create_table_item_graphic(pic: int):
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        _vpic = QLabel()

        if pic == 0:
            _p = QPixmap(MShared.get_resource_path('keva-logo.png'))
        elif pic == 1:
            _p = QPixmap(MShared.get_resource_path('star.png'))
            _vpic.setToolTip('Read-Only Wallet')
        elif pic == 2:
            _p = QPixmap(MShared.get_resource_path('medal2.png'))
        elif pic == 3:
            _p = QPixmap(MShared.get_resource_path('locked.png'))
            _vpic.setToolTip('Wallet is Locked')
        elif pic == 4:
            _p = QPixmap(MShared.get_resource_path('unlocked.png'))
            _vpic.setToolTip('Wallet is Unlocked')

        _p = _p.scaledToWidth(20, _transm_st)

        _vpic.setPixmap(_p)
        _vpic.setAlignment(_al_center)
        _vpic.setContentsMargins(0, 0, 0, 0)

        return _vpic

    @staticmethod
    def flags():
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def add_wallet(self, wallet_data: dict):
        self.setSortingEnabled(False)
        _r = self.rowCount()
        self.insertRow(_r)

        _vpic = self._create_table_item_graphic(0)

        _coin = QTableWidgetItem(wallet_data['coin'])
        _coin.setFlags(self.flags())
        _coin.setForeground(QtCore.Qt.black)

        _name = QTableWidgetItem(wallet_data['name'])
        _name.setFlags(self.flags())
        _name.setForeground(QtCore.Qt.black)

        _wtype = QTableWidgetItem('')
        _wtype.setFlags(self.flags())
        _wtype.setForeground(QtCore.Qt.black)

        _kvpic = QLabel()

        if wallet_data['kind'] != 0:
            if wallet_data['kind'] == 1:
                _kvpic = self._create_table_item_graphic(1)
            elif wallet_data['kind'] == 2:
                _kvpic = self._create_table_item_graphic(2)
            elif wallet_data['kind'] == 3:
                _kvpic = self._create_table_item_graphic(1)

        _bal = wallet_data['balance'] - wallet_data['bid_balance']
        wallet_data['balance'] = round(_bal, 8)
        _balance = QTableWidgetItem(str(wallet_data['balance']))
        _balance.setFlags(self.flags())
        _balance.setForeground(QtCore.Qt.black)

        wallet_data['bid_balance'] = round(wallet_data['bid_balance'], 8)
        _bid_balance = QTableWidgetItem(str(wallet_data['bid_balance']))
        _bid_balance.setFlags(self.flags())
        _bid_balance.setForeground(QtCore.Qt.black)

        if wallet_data['locked'] is True:
            _lvpic = self._create_table_item_graphic(3)
        else:
            _lvpic = self._create_table_item_graphic(4)

        # if wallet_data['state_lock'] != 0:
        #    _lvpic.setPixmap(_lpic)

        _upd = '-'

        if 'last_updated' in wallet_data:
            if wallet_data['last_updated'] is not None:
                _upd = MShared.get_timestamp(wallet_data['last_updated'])[1]

        _updated = QTableWidgetItem(_upd)
        _updated.setFlags(self.flags())
        _updated.setForeground(QtCore.Qt.black)

        _synch = QTableWidgetItem('')
        _synch.setFlags(self.flags())
        _synch.setForeground(QtCore.Qt.black)

        self._vupic = animation_label()

        self.setCellWidget(_r, 0, _vpic)
        self.setCellWidget(_r, 1, _lvpic)
        self.setItem(_r, 2, _coin)
        self.setItem(_r, 3, _name)
        self.setItem(_r, 4, _wtype)
        self.setCellWidget(_r, 5, _kvpic)
        self.setItem(_r, 6, _balance)
        self.setItem(_r, 7, _bid_balance)
        self.setItem(_r, 8, _updated)
        self.setItem(_r, 9, _synch)
        self.setCellWidget(_r, 9, self._vupic)
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)

    def update_wallet(self, _w: MWallet, row: int):
        if _w.locked is True:
            _lvpic = self._create_table_item_graphic(3)
        else:
            _lvpic = self._create_table_item_graphic(4)

        _kvpic = QLabel()

        if _w.kind != 0 and _w.kind is not None:
            if _w.kind == 1:
                _kvpic = self._create_table_item_graphic(1)
            elif _w.kind == 2:
                _kvpic = self._create_table_item_graphic(2)

        if _w.last_updated is not None:
            _upd = MShared.get_timestamp(_w.last_updated)[1]
        else:
            _upd = '-'

        self.setCellWidget(row, 1, _lvpic)
        self.item(row, 2).setText(_w.coin)
        self.item(row, 4).setText(_w.bip)
        self.setCellWidget(row, 5, _kvpic)
        self.item(row, 6).setText(str(round(_w.balance, 8)))
        self.item(row, 7).setText(str(round(_w.bid_balance, 8)))
        self.item(row, 8).setText(_upd)
        self.resizeColumnsToContents()
