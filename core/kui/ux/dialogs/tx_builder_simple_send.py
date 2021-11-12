import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QComboBox, QPushButton, QPlainTextEdit)

from control.shared import MShared
from core.ksc import Scripts
from core.ksc.utils import Ut
from core.kcl.bip_utils.base58 import Base58Decoder

from core.kcl.models.cache import MCache
from core.kcl.models.wallets import MWallets
from core.kcl.models.transaction_builder import MTransactionBuilder


class Ui_simple_send_dlg(QDialog):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignCenter
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _bb_br_ar = QDialogButtonBox.ActionRole
        _bb_br_ac = QDialogButtonBox.AcceptRole

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.kex = None
        self.user_path = None
        self.new_tx = MTransactionBuilder()
        self.raw_tx = None
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_1 = QLabel(self)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.wl = QHBoxLayout()
        self.w_l = QLabel(self)
        self.w = QComboBox(self)
        self.hl = QHBoxLayout()
        self.value_l = QLabel(self)
        self.value = QLineEdit(self)
        self.ahl = QHBoxLayout()
        self.address_l = QLabel(self)
        self.ahl_1 = QHBoxLayout()
        self.address = QLineEdit(self)
        self.address_book = QComboBox(self)
        self.address_select = QPushButton(self)
        self.fee_hl = QHBoxLayout()
        self.fee_l = QLabel(self)
        self.fee = QLabel(self)
        self.feerate_hl = QHBoxLayout()
        self.feerate_l = QLabel(self)
        self.feerate = QLabel(self)
        self.tx_hl = QHBoxLayout()
        self.tx_l = QLabel(self)
        self.txsize_l = QLabel(self)
        self.txsize = QLabel(self)
        self.tx = QPlainTextEdit(self)
        self.next_btn = QPushButton(self)
        self.back_btn = QPushButton(self)
        self.cancel_btn = QPushButton(self)
        self.send_btn = QPushButton(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('send_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        # _pic = _pic.scaledToWidth(20, _transm_st)
        self.label_1.setPixmap(_pic)
        self.w.setMinimumWidth(250)
        self.w.addItem('-', '-')
        self.value.setMaximumWidth(250)
        self.address.setAlignment(_al_center)
        self.address_book.setVisible(False)
        self.address_book.addItem('-', '-')
        self.address_select.setMinimumWidth(55)
        self.address_select.setMaximumWidth(55)
        self.tx.setMaximumHeight(65)
        self.tx.setReadOnly(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.cancel_btn, _bb_br_ar)
        self.buttonBox.addButton(self.next_btn, _bb_br_ar)
        self.buttonBox.addButton(self.back_btn, _bb_br_ar)
        self.buttonBox.addButton(self.send_btn, _bb_br_ac)
        # self.buttonBox.addButton(QDialogButtonBox.StandardButton.Cancel)
        # self.buttonBox.addButton(_b_ok)
        # self.buttonBox.button(_b_ok).setEnabled(False)
        self.back_btn.setVisible(False)
        self.next_btn.setEnabled(False)
        self.send_btn.setEnabled(False)

        self.horizontalLayout_1.addWidget(self.label_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.wl.addWidget(self.w_l)
        self.wl.addWidget(self.w)
        self.wl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.wl)
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
        self.fee_hl.addWidget(self.fee_l)
        self.fee_hl.addWidget(self.fee)
        self.fee_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.fee_hl)
        self.feerate_hl.addWidget(self.feerate_l)
        self.feerate_hl.addWidget(self.feerate)
        self.feerate_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.feerate_hl)
        self.tx_hl.addWidget(self.tx_l)
        self.tx_hl.addWidget(self.txsize_l)
        self.tx_hl.addWidget(self.txsize)
        self.tx_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.tx_hl)
        self.verticalLayout.addWidget(self.tx)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.w.currentTextChanged.connect(self.txb_w_changed)
        self.cancel_btn.clicked.connect(self.reject)
        self.next_btn.clicked.connect(self.txb_build_simple_send)
        self.back_btn.clicked.connect(self.back_click)
        self.value.textChanged.connect(self.check_next)
        self.address.textChanged.connect(self.check_next)
        self.address_book.currentTextChanged.connect(self.check_next)
        self.address_select.clicked.connect(self.select_swap)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('send_dlg', 'Narwhallet - Send'))
        self.w_l.setText(_translate('send_dlg', 'Wallet:'))
        self.value_l.setText(_translate('send_dlg', 'Value: '))
        self.address_l.setText(_translate('send_dlg', 'Send to Address:'))
        self.address_select.setText(_translate('send_dlg', 'Book'))
        self.cancel_btn.setText(_translate('send_dlg', 'Cancel'))
        self.send_btn.setText(_translate('send_dlg', 'Send'))
        self.next_btn.setText(_translate('send_dlg', 'Next'))
        self.back_btn.setText(_translate('send_dlg', 'Back'))
        self.txsize_l.setText(_translate('send_dlg', 'size:'))
        self.fee_l.setText(_translate('send_dlg', 'Fee (KVA):'))
        self.feerate_l.setText(_translate('send_dlg',
                                          'Fee Rate (Satoshi per byte):'))
        self.tx_l.setText(_translate('send_dlg', 'Raw TX -'))

    def check_next(self):
        if self.w.currentText() != '-':
            if self.check_value() and self.check_address():
                self.next_btn.setEnabled(True)
            else:
                self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(False)

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
            _n = self.w.currentData()
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

    def txb_preimage(self):
        _n = self.w.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        self.new_tx.input_signatures = []
        # print('len(self.new_tx.vin)', len(self.new_tx.vin))
        for c, _vin_idx in enumerate(self.new_tx.vin):
            _npk = _vin_idx.tb_address
            _npkc = _vin_idx.tb_address_chain
            _pk = wallet.get_publickey_raw(_npk, _npkc)
            _sighash = self.new_tx.make_preimage(c, _pk)
            _sig = wallet.sign_message(_npk, _sighash, _npkc)
            _script = Scripts.P2WPKHScriptSig.compile([_pk], True)
            _vin_idx.scriptSig.set_hex(_script)
            # HACK - Note assuming signatre was SIGHASH_TYPE.ALL
            # if [_sig+'01', _pk] not in self.new_tx.input_signatures:
            self.new_tx.input_signatures.append([_sig+'01', _pk])

            _addr = wallet.get_address_by_index(_npk, False)
            _r = Scripts.P2SHAddressScriptHash.compile([_addr], False)
            _ref = Ut.int_to_bytes(_vin_idx.tb_value, 8, 'little')
            _ref = _ref + Ut.to_cuint(len(_r)) + _r
            self.new_tx.input_ref_scripts.append(_ref)

    def txb_build_simple_send(self):
        locale = QLocale()
        _result = locale.toDouble(self.value.text())
        _v = int(_result[0] * 100000000)

        if self.address.isVisible():
            _a = self.address.text()
        else:
            _a = self.address_book.currentData()

        _ = self.new_tx.add_output(_v, _a)
        _n = self.w.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)

        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            _cv = _fv - _est_fee
            # print('_cv', _cv, 'fv', _fv, 'est_fee', _est_fee)
            if _need_change is True:
                _change_address = wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)

            # print('final size', self.new_tx.get_size(len(self.new_tx.vin),
            #       len(self.new_tx.vout)))
            self.txb_preimage()
            _stx = self.new_tx.serialize_tx()

            self.fee.setText(str(_est_fee/100000000))
            self.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.tx.setPlainText(self.raw_tx)

            self.w.setEnabled(False)
            # self.value.setStyle(QFrame.Shape.NoFrame)
            self.value.setFrame(False)
            self.value.setReadOnly(True)
            self.address.setReadOnly(True)
            self.address.setFrame(False)
            # self.address.setStyle(QFrame.Shape.NoFrame)
            self.next_btn.setVisible(False)
            self.back_btn.setVisible(True)
            self.send_btn.setEnabled(True)
        else:
            self.new_tx.set_vin([])
            self.new_tx.set_vout([])

    def back_click(self):
        self.next_btn.setVisible(True)
        self.back_btn.setVisible(False)
        self.send_btn.setEnabled(False)
        self.value.setFrame(True)
        self.address.setFrame(True)
        self.fee.setText('')
        self.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.tx.setPlainText(self.raw_tx)

        self.w.setEnabled(True)
        self.value.setReadOnly(False)
        self.address.setReadOnly(False)
