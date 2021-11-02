import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QComboBox, QPushButton, QPlainTextEdit)

from control.shared import MShared
from core.ksc import Scripts
from core.ksc.utils import Ut
from core.kcl.models.cache import MCache
from core.kcl.models.wallets import MWallets
from core.kcl.models.transaction_builder import MTransactionBuilder


class Ui_keva_op_send_dlg(QObject):
    def setupUi(self, keva_op_send_dialog: QDialog):
        _al_center = QtCore.Qt.AlignCenter
        _bb_br_ar = QDialogButtonBox.ActionRole
        _bb_br_ac = QDialogButtonBox.AcceptRole
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.KEX = None
        self.user_path = None
        self._new_tx = MTransactionBuilder()
        self.raw_tx = None
        self._ns = None
        self._isTransfer: bool = False
        self._ns_address = None
        self._ns_key = None
        self._ns_value = None
        self.verticalLayout = QVBoxLayout(keva_op_send_dialog)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_1 = QLabel(keva_op_send_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.wl = QHBoxLayout()
        self.w_l = QLabel(keva_op_send_dialog)
        self.w = QComboBox(keva_op_send_dialog)
        self.skl = QHBoxLayout()
        self.sk_l = QLabel(keva_op_send_dialog)
        self.sk = QComboBox(keva_op_send_dialog)
        self.hl = QHBoxLayout()
        self.key_v_l = QLabel(keva_op_send_dialog)
        self.key_v = QLineEdit(keva_op_send_dialog)
        self.vhl = QHBoxLayout()
        self.value_l = QLabel(keva_op_send_dialog)
        self.value = QPlainTextEdit(keva_op_send_dialog)
        self.address_book = QComboBox(keva_op_send_dialog)
        # self.ahl = QHBoxLayout()
        # self.address_l = QLabel(keva_op_send_dialog)
        # self.address = QLineEdit(keva_op_send_dialog)
        self.fee_hl = QHBoxLayout()
        self.fee_l = QLabel(keva_op_send_dialog)
        self.fee = QLabel(keva_op_send_dialog)
        self.feerate_hl = QHBoxLayout()
        self.feerate_l = QLabel(keva_op_send_dialog)
        self.feerate = QLabel(keva_op_send_dialog)
        self.tx_hl = QHBoxLayout()
        self.tx_l = QLabel(keva_op_send_dialog)
        self.txsize_l = QLabel(keva_op_send_dialog)
        self.txsize = QLabel(keva_op_send_dialog)
        self.tx = QPlainTextEdit(keva_op_send_dialog)
        self.next_btn = QPushButton(keva_op_send_dialog)
        self.back_btn = QPushButton(keva_op_send_dialog)
        self.cancel_btn = QPushButton(keva_op_send_dialog)
        self.send_btn = QPushButton(keva_op_send_dialog)
        self.buttonBox = QDialogButtonBox(keva_op_send_dialog)

        keva_op_send_dialog.setObjectName('keva_op_send_dlg')
        keva_op_send_dialog.setMinimumSize(QtCore.QSize(475, 350))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        # _pic = _pic.scaledToWidth(20, _transm_st)
        self.label_1.setPixmap(_pic)
        self.w.setMinimumWidth(250)
        self.w.addItem('-', '-')
        self.sk.addItem('Special Keys', '-')
        self.sk.setVisible(False)
        self.sk_l.setVisible(False)
        self.key_v.setMinimumWidth(365)
        self.value.setMinimumHeight(65)
        self.address_book.addItem('-', '-')
        self.address_book.setVisible(False)
        # self.address.setAlignment(_al_center)
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
        self.skl.addWidget(self.sk_l)
        self.skl.addWidget(self.sk)
        self.skl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.skl)
        self.hl.addWidget(self.key_v_l)
        self.hl.addWidget(self.key_v)
        self.hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl)
        self.vhl.addWidget(self.value_l)
        self.vhl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.vhl)
        self.verticalLayout.addWidget(self.value)
        self.verticalLayout.addWidget(self.address_book)
        # self.ahl.addWidget(self.address_l)
        # self.verticalLayout.addLayout(self.ahl)
        # self.verticalLayout.addWidget(self.address)
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

        self.retranslateUi(keva_op_send_dialog)
        self.buttonBox.accepted.connect(keva_op_send_dialog.accept)
        self.buttonBox.rejected.connect(keva_op_send_dialog.reject)
        self.w.currentTextChanged.connect(self.txb_w_changed)
        self.cancel_btn.clicked.connect(keva_op_send_dialog.reject)
        self.next_btn.clicked.connect(self.txb_build_simple_send)
        self.back_btn.clicked.connect(self.back_click)
        self.value.textChanged.connect(self.check_next)
        self.address_book.currentTextChanged.connect(self.check_next)

    def retranslateUi(self, k_op_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        k_op_dlg.setWindowTitle(_translate('keva_op_send_dlg',
                                           'Narwhallet - Create Namespace'))
        self.w_l.setText(_translate('keva_op_send_dlg', 'Wallet:'))
        self.sk_l.setText(_translate('keva_op_send_dlg', 'Special Key:'))
        self.key_v_l.setText(_translate('keva_op_send_dlg', 'Key Name: '))
        self.value_l.setText(_translate('keva_op_send_dlg', 'Name: '))
        # self.address_l.setText(_translate('keva_op_send_dlg',
        #                                   'Send to Address:'))
        self.cancel_btn.setText(_translate('keva_op_send_dlg', 'Cancel'))
        self.send_btn.setText(_translate('keva_op_send_dlg', 'Send'))
        self.next_btn.setText(_translate('keva_op_send_dlg', 'Next'))
        self.back_btn.setText(_translate('keva_op_send_dlg', 'Back'))
        self.txsize_l.setText(_translate('keva_op_send_dlg', 'size:'))
        self.fee_l.setText(_translate('keva_op_send_dlg', 'Fee (KVA):'))
        self.feerate_l.setText(_translate('keva_op_send_dlg',
                                          'Fee Rate (Satoshi per byte):'))
        self.tx_l.setText(_translate('keva_op_send_dlg', 'Raw TX -'))

    def check_next(self):
        if self.w.currentText() != '-' and self.value.toPlainText() != '':
            if self.address_book.isVisible():
                if self.address_book.currentData() != '-':
                    self.next_btn.setEnabled(True)
                else:
                    self.next_btn.setEnabled(False)
            else:
                self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)

    def txb_w_changed(self, data):
        if data != '-':
            self.set_availible_usxo(False)

        self.check_next()

    def set_availible_usxo(self, isChangeOp: bool):
        if self.user_path is not None:
            _n = self.w.currentData()
            wallet = self.wallets.get_wallet_by_name(_n)
            MShared.list_unspents(wallet, self.KEX)
            _tmp_usxo = wallet.get_usxos()
            _usxos = []
            _nsusxo = None

            for tx in _tmp_usxo:
                # TODO Check for usxo's used by bids
                _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

                if _tx is None:
                    _tx = MShared.__get_tx(tx['tx_hash'], self.KEX, True)
                    if _tx is not None:
                        _tx = self.cache.tx.add_fromJson(_tx)

                if _tx is not None:
                    if _tx.confirmations is not None:
                        if _tx.confirmations >= 6:
                            if ('OP_KEVA' not in
                               _tx.vout[tx['tx_pos']].scriptPubKey.asm):
                                _usxos.append(tx)
                            elif ('OP_KEVA'
                                  in _tx.vout[tx['tx_pos']].scriptPubKey.asm
                                  and isChangeOp is True
                                  and tx['a'] == self._ns_address):
                                _nsusxo = tx

            if _nsusxo is not None and isChangeOp is True:
                _usxos.insert(0, _nsusxo)

            self._new_tx._inputs_to_spend = _usxos

    def txb_preimage(self):
        _n = self.w.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        self._new_tx._input_signatures = []
        # print('len(self._new_tx.vin)', len(self._new_tx.vin))
        for _vin_idx in range(0, len(self._new_tx.vin)):
            _npk = self._new_tx.vin[_vin_idx]._tb_address
            _npkc = self._new_tx.vin[_vin_idx]._tb_address_chain
            _pk = wallet.get_publickey_raw(_npk, _npkc)
            _sighash = self._new_tx.make_preimage(_vin_idx, _pk)
            _sig = wallet.sign_message(_npk, _sighash, _npkc)
            _script = Scripts.P2WPKHScriptSig.compile([_pk], True)
            self._new_tx.vin[_vin_idx]._scriptSig.set_hex(_script)
            # HACK - Note assuming signatre was SIGHASH_TYPE.ALL
            # if [_sig+'01', _pk] not in self._new_tx._input_signatures:
            self._new_tx._input_signatures.append([_sig+'01', _pk])

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        return Ut.bytes_to_hex(bytes([53]) + Ut.hash160(_tx + str(vout).encode()))

    def txb_build_simple_send(self):
        self._new_tx._version = Ut.hex_to_bytes('00710000')
        _n = self.w.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        _t = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
        _temp_vout = 0
        _temp_ns = self.tx_to_ns(_t, _temp_vout)
        _namespace_reservation = 1000000

        if self._ns_address is None:
            self._ns_address = wallet.get_unused_address()

        if self.address_book.isVisible():
            if self.address_book.currentData() != '-':
                self._ns_address = self.address_book.currentData()

        if self._ns_value is None:
            self._ns_value = self.value.toPlainText()
        elif self._ns_value == '':
            self._ns_value = None
        else:
            self.value.setPlainText(self._ns_value)

        if self._ns_key is None:
            self._ns_key = self.key_v.text()
        else:
            self.key_v.setText(self._ns_key)

        if self._ns is None:
            _sh = Scripts.KevaNamespaceCreation.compile([_temp_ns,
                                                         self._ns_value,
                                                         self._ns_address
                                                         ], True)
        elif (self._ns is not None and self._ns_key is not None
              and self._ns_value is not None):
            _sh = Scripts.KevaKeyValueUpdate.compile([self._ns, self._ns_key,
                                                      self._ns_value,
                                                      self._ns_address], True)
        elif (self._ns is not None and self._ns_key is not None
              and self._ns_value is None):
            _sh = Scripts.KevaKeyValueDelete.compile([self._ns, self._ns_key,
                                                      self._ns_address], True)

        _ = self._new_tx.add_output(_namespace_reservation, self._ns_address)
        self._new_tx.vout[0].scriptPubKey.set_hex(_sh)

        _inp_sel, _need_change, _est_fee = self._new_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self._new_tx.get_current_values()
            _cv = _fv - _est_fee
            #print('_cv', _cv, 'fv', _fv, 'est_fee', _est_fee)

            if self._ns is None:
                self._ns = self.tx_to_ns(self._new_tx.vin[0].txid,
                                         self._new_tx.vin[0].vout)
                _n_sh = Scripts.KevaNamespaceCreation.compile([self._ns,
                                                               self._ns_value,
                                                               self._ns_address
                                                               ], True)
                if _need_change is True:
                    #_change_address = wallet.get_unused_change_address()
                    _ = self._new_tx.add_output(_cv, self._ns_address)
            elif (self._ns is not None and self._ns_key is not None
                  and self._ns_value is not None):
                _n_sh = Scripts.KevaKeyValueUpdate.compile([self._ns,
                                                            self._ns_key,
                                                            self._ns_value,
                                                            self._ns_address
                                                            ], True)
                if self._isTransfer is True:
                    if _need_change is True:
                        _change_address = wallet.get_unused_change_address()
                        _ = self._new_tx.add_output(_cv, _change_address)
                else:
                    _ = self._new_tx.add_output(_cv, self._ns_address)
            elif (self._ns is not None and self._ns_key is not None
                  and self._ns_value is None):
                _n_sh = Scripts.KevaKeyValueDelete.compile([self._ns,
                                                            self._ns_key,
                                                            self._ns_address
                                                            ], True)
                if _need_change is True:
                    _ = self._new_tx.add_output(_cv, self._ns_address)

            self._new_tx.vout[0].scriptPubKey.set_hex(_n_sh)
            # print('final size', self._new_tx.get_size(len(self._new_tx.vin), len(self._new_tx.vout)))

            self.txb_preimage()
            _stx = self._new_tx.serialize_tx()

            self.fee.setText(str(_est_fee/100000000))
            self.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.tx.setPlainText(self.raw_tx)

            self.w.setEnabled(False)

            # self.value.setFrame(False)
            self.value.setReadOnly(True)

            self.next_btn.setVisible(False)
            self.back_btn.setVisible(True)
            self.send_btn.setEnabled(True)
        else:
            self._new_tx.set_vin([])
            self._new_tx.set_vout([])

    def back_click(self):
        self.next_btn.setVisible(True)
        self.back_btn.setVisible(False)
        self.send_btn.setEnabled(False)
        # self.value.setFrame(True)
        # self.address.setFrame(True)
        self.fee.setText('')
        self.txsize.setText('')
        self.raw_tx = ''
        self._new_tx.set_vin([])
        self._new_tx.set_vout([])
        self._new_tx._input_signatures = []
        self.tx.setPlainText(self.raw_tx)

        self.w.setEnabled(True)
        self.value.setReadOnly(False)
        # self.address.setReadOnly(False)
