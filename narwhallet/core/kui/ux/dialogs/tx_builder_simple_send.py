from PyQt5 import QtCore
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy,
                             QComboBox, QPushButton)
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kcl.models.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallets import MWallets
from narwhallet.core.kcl.models.transaction_builder import MTransactionBuilder
from narwhallet.core.kui.ux.widgets.wallet_combobox import WalletComboBox
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame
from narwhallet.core.kui.ux.widgets.dialog_buttonbox import DialogButtonBox
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_simple_send_dlg(QDialog):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignCenter
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.kex = None
        self.user_path = None
        self.new_tx = MTransactionBuilder()
        self.raw_tx = None
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.wallet_combo = WalletComboBox()
        self.hl = QHBoxLayout()
        self.value_l = QLabel(self)
        self.value = QLineEdit(self)
        self.ahl = QHBoxLayout()
        self.address_l = QLabel(self)
        self.ahl_1 = QHBoxLayout()
        self.address = QLineEdit(self)
        self.address_book = QComboBox(self)
        self.address_select = QPushButton(self)
        self.send_info = SendInfoFrame()
        self.buttonBox = DialogButtonBox(self)

        self.setObjectName('send_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        self.value.setMaximumWidth(250)
        self.address.setAlignment(_al_center)
        self.address_book.setVisible(False)
        self.address_book.addItem('-', '-')

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.wallet_combo)
        self.hl.addWidget(self.value_l)
        self.hl.addWidget(self.value)
        self.hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl)
        self.ahl.addWidget(self.address_l)
        self.verticalLayout.addLayout(self.ahl)
        self.ahl_1.addWidget(self.address)
        self.ahl_1.addWidget(self.address_book)
        self.ahl_1.addWidget(self.address_select)
        self.verticalLayout.addLayout(self.ahl_1)
        self.verticalLayout.addWidget(self.send_info)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.cancel.clicked.connect(self.reject)
        self.buttonBox.next.clicked.connect(self.txb_build_simple_send)
        self.buttonBox.back.clicked.connect(self.back_click)
        self.value.textChanged.connect(self.check_next)
        self.address.textChanged.connect(self.check_next)
        self.address_book.currentTextChanged.connect(self.check_next)
        self.address_select.clicked.connect(self.select_swap)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('send_dlg', 'Narwhallet - Send'))
        self.value_l.setText(_translate('send_dlg', 'Value: '))
        self.address_l.setText(_translate('send_dlg', 'Send to Address:'))
        self.address_select.setText(_translate('send_dlg', 'Book'))

    def check_next(self):
        if self.wallet_combo.combo.currentText() != '-':
            if self.check_value() and self.check_address():
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        else:
            self.buttonBox.next.setEnabled(False)

    def check_value(self):
        try:
            locale = QLocale()
            _result = locale.toDouble(self.value.text())
            if _result[1] is True:
                _return = True
            else:
                _return = False
        except Exception:
            _return = False
        return _return

    def check_address(self):
        try:
            if self.address.isVisible():
                _ = Base58Decoder.CheckDecode(self.address.text())
            else:
                _ = Base58Decoder.CheckDecode(self.address_book.currentData())
            return True
        except Exception:
            return False

    def select_swap(self):
        self.address.setText('')
        self.address_book.setCurrentText('-')

        if self.address.isVisible():
            self.address.setVisible(False)
            self.address_book.setVisible(True)
            self.address_select.setText('Entry')
        else:
            self.address.setVisible(True)
            self.address_book.setVisible(False)
            self.address_select.setText('Book')

    def txb_w_changed(self, data):
        if data != '-':
            _n = self.wallet_combo.combo.currentData()
            wallet = self.wallets.get_wallet_by_name(_n)
            MShared.list_unspents(wallet, self.kex)
            _tmp_usxo = wallet.get_usxos()
            _usxos = []

            for tx in _tmp_usxo:
                # TODO Check for usxo's used by bids
                _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

                if _tx is None:
                    _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)

                if _tx is not None and isinstance(_tx, dict):
                    _tx = self.cache.tx.add_from_json(_tx)

                if _tx is None:
                    continue

                if _tx.confirmations is None:
                    continue

                if _tx.confirmations < 6:
                    continue

                if 'OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
                    _usxos.append(tx)

            self.new_tx.inputs_to_spend = _usxos
        self.check_next()

    def txb_build_simple_send(self):
        locale = QLocale()
        _result = locale.toDouble(self.value.text())
        _v = int(_result[0] * 100000000)

        if self.address.isVisible():
            _a = self.address.text()
        else:
            _a = self.address_book.currentData()

        _ = self.new_tx.add_output(_v, _a)
        _n = self.wallet_combo.combo.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)

        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            _cv = _fv - _est_fee

            if _need_change is True:
                _change_address = wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)

            self.new_tx.txb_preimage(wallet, SIGHASH_TYPE.ALL)
            _stx = self.new_tx.serialize_tx()

            self.send_info.fee.setText(str(_est_fee/100000000))
            self.send_info.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.send_info.tx.setPlainText(self.raw_tx)
            self.wallet_combo.combo.setEnabled(False)
            self.value.setFrame(False)
            self.value.setReadOnly(True)
            self.address.setReadOnly(True)
            self.address.setFrame(False)
            self.buttonBox.next.setVisible(False)
            self.buttonBox.back.setVisible(True)
            self.buttonBox.send.setEnabled(True)
        else:
            self.new_tx.set_vin([])
            self.new_tx.set_vout([])

    def back_click(self):
        self.buttonBox.next.setVisible(True)
        self.buttonBox.back.setVisible(False)
        self.buttonBox.send.setEnabled(False)
        self.value.setFrame(True)
        self.address.setFrame(True)
        self.send_info.fee.setText('')
        self.send_info.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.send_info.tx.setPlainText(self.raw_tx)
        self.wallet_combo.combo.setEnabled(True)
        self.value.setReadOnly(False)
        self.address.setReadOnly(False)
