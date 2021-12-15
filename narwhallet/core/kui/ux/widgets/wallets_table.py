from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.models.wallet import MWallet
from narwhallet.core.kui.ux.widgets.generator import UShared


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
        self.setProperty('class', 'tblImg')
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
        UShared.set_table_columns(10, ['', 'Locked', 'Coin', 'Name', 'Type',
                                       'Kind', 'Balance', 'Bid Locked',
                                       'Last Updated', ''], self)
        self.setColumnHidden(2, True)
        self.setColumnHidden(4, True)

    def add_wallet(self, wallet_data: dict):
        self.setSortingEnabled(False)
        _r = self.rowCount()
        self.insertRow(_r)

        _vpic = UShared.create_table_item_graphic(0)
        _coin = UShared.create_table_item(wallet_data['coin'])
        _name = UShared.create_table_item(wallet_data['name'])
        _wtype = UShared.create_table_item('')
        if wallet_data['kind'] != 0:
            if wallet_data['kind'] == 1:
                _kvpic = UShared.create_table_item_graphic(4)
            elif wallet_data['kind'] == 2:
                _kvpic = UShared.create_table_item_graphic(2)
            elif wallet_data['kind'] == 3:
                _kvpic = UShared.create_table_item_graphic(4)
        else:
            _kvpic = QLabel()
            _kvpic.setContentsMargins(0, 0, 0, 0)
            _kvpic.setProperty('class', 'tblImg')

        _bal = wallet_data['balance'] - wallet_data['bid_balance']
        wallet_data['balance'] = round(_bal, 8)
        _balance = UShared.create_table_item(wallet_data['balance'])
        wallet_data['bid_balance'] = round(wallet_data['bid_balance'], 8)
        _bid_balance = UShared.create_table_item(wallet_data['bid_balance'])
        if wallet_data['locked'] is True:
            _lvpic = UShared.create_table_item_graphic(6)
        else:
            _lvpic = UShared.create_table_item_graphic(7)

        _upd = '-'
        if 'last_updated' in wallet_data:
            if wallet_data['last_updated'] is not None:
                _upd = MShared.get_timestamp(wallet_data['last_updated'])[1]

        _updated = UShared.create_table_item(_upd)
        _synch = UShared.create_table_item('')
        self._vupic = animation_label()

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setCellWidget(_r, 1, _lvpic)
        self.setItem(_r, 1, UShared.create_table_item(''))
        self.setItem(_r, 2, _coin)
        self.setItem(_r, 3, _name)
        self.setItem(_r, 4, _wtype)
        self.setCellWidget(_r, 5, _kvpic)
        self.setItem(_r, 5, UShared.create_table_item(''))
        self.setItem(_r, 6, _balance)
        self.setItem(_r, 7, _bid_balance)
        self.setItem(_r, 8, _updated)
        self.setItem(_r, 9, _synch)
        self.setCellWidget(_r, 9, self._vupic)
        self.setItem(_r, 9, UShared.create_table_item(''))
        self.resizeColumnsToContents()
        self.setSortingEnabled(True)

    def update_wallet(self, _w: MWallet, row: int):
        if _w.locked is True:
            _lvpic = UShared.create_table_item_graphic(6)
        else:
            _lvpic = UShared.create_table_item_graphic(7)

        if _w.kind != 0 and _w.kind is not None:
            if _w.kind == 1:
                _kvpic = UShared.create_table_item_graphic(4)
            elif _w.kind == 2:
                _kvpic = UShared.create_table_item_graphic(2)
            elif _w.kind == 3:
                _kvpic = UShared.create_table_item_graphic(4)
        else:
            _kvpic = QLabel()
            _kvpic.setContentsMargins(0, 0, 0, 0)
            _kvpic.setProperty('class', 'tblImg')

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
