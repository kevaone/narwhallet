from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QComboBox, QPushButton, QPlainTextEdit)
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.models.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallets import MWallets
from narwhallet.core.kcl.models.transaction_builder import MTransactionBuilder
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.wallet_combobox import WalletComboBox
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame


class Ui_keva_op_send_dlg(QDialog):
    def setupUi(self):
        _bb_br_ar = QDialogButtonBox.ActionRole
        _bb_br_ac = QDialogButtonBox.AcceptRole
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.kex = None
        self.user_path = None
        self.new_tx = MTransactionBuilder()
        self.raw_tx = None
        self.ns = None
        self.is_transfer: bool = False
        self.ns_address = None
        self.ns_key = None
        self.ns_value = None
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        # self.wl = QHBoxLayout()
        # self.w_l = QLabel(self)
        self.w = WalletComboBox()
        self.wnsl = QHBoxLayout()
        self.wns_l = QLabel(self)
        self.wns = QLabel(self)
        self.skl = QHBoxLayout()
        self.sk_l = QLabel(self)
        self.sk = QComboBox(self)
        self.hl = QHBoxLayout()
        self.key_v_l = QLabel(self)
        self.key_v = QLineEdit(self)
        self.vhl = QHBoxLayout()
        self.value_l = QLabel(self)
        self.value = QPlainTextEdit(self)
        self.address_book = QComboBox(self)
        self.send_info = SendInfoFrame()
        # self.fee_hl = QHBoxLayout()
        # self.fee_l = QLabel(self)
        # self.fee = QLabel(self)
        # self.feerate_hl = QHBoxLayout()
        # self.feerate_l = QLabel(self)
        # self.feerate = QLabel(self)
        # self.tx_hl = QHBoxLayout()
        # self.tx_l = QLabel(self)
        # self.txsize_l = QLabel(self)
        # self.txsize = QLabel(self)
        # self.tx = QPlainTextEdit(self)
        self.next_btn = QPushButton(self)
        self.back_btn = QPushButton(self)
        self.cancel_btn = QPushButton(self)
        self.send_btn = QPushButton(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('keva_op_send_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        # self.w.setMinimumWidth(250)
        # self.w.addItem('-', '-')
        self.sk.addItem('Special Keys', '-')
        self.sk.setVisible(False)
        self.sk_l.setVisible(False)
        self.key_v.setMinimumWidth(365)
        self.value.setMinimumHeight(65)
        self.address_book.addItem('-', '-')
        self.address_book.setVisible(False)
        # self.tx.setMaximumHeight(65)
        # self.tx.setReadOnly(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.cancel_btn, _bb_br_ar)
        self.buttonBox.addButton(self.next_btn, _bb_br_ar)
        self.buttonBox.addButton(self.back_btn, _bb_br_ar)
        self.buttonBox.addButton(self.send_btn, _bb_br_ac)
        self.back_btn.setVisible(False)
        self.next_btn.setEnabled(False)
        self.send_btn.setEnabled(False)

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        # self.wl.addWidget(self.w_l)
        # self.wl.addWidget(self.w)
        # self.wl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.w)
        self.wnsl.addWidget(self.wns_l)
        self.wnsl.addWidget(self.wns)
        self.wnsl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.wnsl)
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
        # self.fee_hl.addWidget(self.fee_l)
        # self.fee_hl.addWidget(self.fee)
        # self.fee_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        # self.verticalLayout.addLayout(self.fee_hl)
        # self.feerate_hl.addWidget(self.feerate_l)
        # self.feerate_hl.addWidget(self.feerate)
        # self.feerate_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        # self.verticalLayout.addLayout(self.feerate_hl)
        # self.tx_hl.addWidget(self.tx_l)
        # self.tx_hl.addWidget(self.txsize_l)
        # self.tx_hl.addWidget(self.txsize)
        # self.tx_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        # self.verticalLayout.addLayout(self.tx_hl)
        self.verticalLayout.addWidget(self.send_info)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.w.combo.currentTextChanged.connect(self.txb_w_changed)
        self.cancel_btn.clicked.connect(self.reject)
        self.next_btn.clicked.connect(self.txb_build_simple_send)
        self.back_btn.clicked.connect(self.back_click)
        self.value.textChanged.connect(self.check_next)
        self.address_book.currentTextChanged.connect(self.check_next)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('keva_op_send_dlg',
                                       'Narwhallet - Create Namespace'))
        # self.w_l.setText(_translate('keva_op_send_dlg', 'Wallet:'))
        self.wns_l.setText(_translate('keva_op_send_dlg', 'Namespace:'))
        self.sk_l.setText(_translate('keva_op_send_dlg', 'Special Key:'))
        self.key_v_l.setText(_translate('keva_op_send_dlg', 'Key Name: '))
        self.value_l.setText(_translate('keva_op_send_dlg', 'Name: '))
        self.cancel_btn.setText(_translate('keva_op_send_dlg', 'Cancel'))
        self.send_btn.setText(_translate('keva_op_send_dlg', 'Send'))
        self.next_btn.setText(_translate('keva_op_send_dlg', 'Next'))
        self.back_btn.setText(_translate('keva_op_send_dlg', 'Back'))
        # self.txsize_l.setText(_translate('keva_op_send_dlg', 'size:'))
        # self.fee_l.setText(_translate('keva_op_send_dlg', 'Fee (KVA):'))
        # self.feerate_l.setText(_translate('keva_op_send_dlg',
        #                                   'Fee Rate (Satoshi per byte):'))
        # self.tx_l.setText(_translate('keva_op_send_dlg', 'Raw TX -'))

    def check_next(self):
        if self.w.combo.currentText() != '-' and self.value.toPlainText() != '':
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
            _n = self.w.combo.currentData()
            wallet = self.wallets.get_wallet_by_name(_n)
            self.new_tx.set_availible_usxo(wallet, False, False, self.ns_address, self.cache, self.kex)

        self.check_next()

    @staticmethod
    def _test_tx(tx: MTransactionBuilder) -> bool:
        _return = True
        if tx is None:
            _return = False
        elif tx.confirmations is None:
            _return = False
        elif tx.confirmations < 6:
            _return = False

        return _return

    # def set_availible_usxo(self, is_change: bool):
    #     if self.user_path is not None:
    #         _n = self.w.currentData()
    #         wallet = self.wallets.get_wallet_by_name(_n)
    #         MShared.list_unspents(wallet, self.kex)
    #         _tmp_usxo = wallet.get_usxos()
    #         _usxos = []
    #         _nsusxo = None

    #         for tx in _tmp_usxo:
    #             # TODO Check for usxo's used by bids
    #             _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

    #             if _tx is None:
    #                 _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)

    #             if _tx is not None and isinstance(_tx, dict):
    #                 _tx = self.cache.tx.add_from_json(_tx)

    #             if self._test_tx(_tx) is False:
    #                 continue

    #             if 'OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
    #                 _usxos.append(tx)
    #             elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
    #                     and is_change is True and tx['a'] == self.ns_address):
    #                 _nsusxo = tx

    #         if _nsusxo is not None and is_change is True:
    #             _usxos.insert(0, _nsusxo)

    #         self.new_tx.inputs_to_spend = _usxos

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def txb_build_simple_send(self):
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        _n = self.w.combo.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        _t = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
        _temp_vout = 0
        _temp_ns = self.tx_to_ns(_t, _temp_vout)
        _namespace_reservation = 1000000

        if self.ns_address is None:
            self.ns_address = wallet.get_unused_address()

        if self.address_book.isVisible():
            if self.address_book.currentData() != '-':
                self.ns_address = self.address_book.currentData()

        if self.ns_value is None:
            self.ns_value = self.value.toPlainText()
        elif self.ns_value == '':
            self.ns_value = None
        else:
            self.value.setPlainText(self.ns_value)

        if self.ns_key is None:
            self.ns_key = self.key_v.text()
        else:
            self.key_v.setText(self.ns_key)

        if self.ns is None:
            _sh = Scripts.KevaNamespaceCreation(_temp_ns, self.ns_value,
                                                self.ns_address)
            _sh = Scripts.compile(_sh, True)
        elif (self.ns is not None and self.ns_key is not None
              and self.ns_value is not None):
            _sh = Scripts.KevaKeyValueUpdate(self.ns, self.ns_key,
                                             self.ns_value, self.ns_address)
            _sh = Scripts.compile(_sh, True)
        elif (self.ns is not None and self.ns_key is not None
              and self.ns_value is None):
            _sh = Scripts.KevaKeyValueDelete(self.ns, self.ns_key,
                                             self.ns_address)
            _sh = Scripts.compile(_sh, True)

        _ = self.new_tx.add_output(_namespace_reservation, self.ns_address)
        self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            _cv = _fv - _est_fee

            if self.ns is None:
                self.ns = self.tx_to_ns(self.new_tx.vin[0].txid,
                                        self.new_tx.vin[0].vout)
                _n_sh = Scripts.KevaNamespaceCreation(self.ns, self.ns_value,
                                                      self.ns_address)
                _n_sh = Scripts.compile(_n_sh, True)
                if _need_change is True:
                    _ = self.new_tx.add_output(_cv, self.ns_address)
            elif (self.ns is not None and self.ns_key is not None
                  and self.ns_value is not None):
                _n_sh = Scripts.KevaKeyValueUpdate(self.ns, self.ns_key,
                                                   self.ns_value,
                                                   self.ns_address)
                _n_sh = Scripts.compile(_n_sh, True)

                if self.is_transfer is True:
                    if _need_change is True:
                        _change_address = wallet.get_unused_change_address()
                        _ = self.new_tx.add_output(_cv, _change_address)
                else:
                    _ = self.new_tx.add_output(_cv, self.ns_address)
            elif (self.ns is not None and self.ns_key is not None
                  and self.ns_value is None):
                _n_sh = Scripts.KevaKeyValueDelete(self.ns, self.ns_key,
                                                   self.ns_address)
                _n_sh = Scripts.compile(_n_sh, True)

                if _need_change is True:
                    _ = self.new_tx.add_output(_cv, self.ns_address)

            self.new_tx.vout[0].scriptPubKey.set_hex(_n_sh)

            self.new_tx.txb_preimage(wallet, SIGHASH_TYPE.ALL)
            _stx = self.new_tx.serialize_tx()

            self.send_info.fee.setText(str(_est_fee/100000000))
            self.send_info.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.send_info.tx.setPlainText(self.raw_tx)
            self.w.combo.setEnabled(False)
            self.value.setReadOnly(True)
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
        self.send_info.fee.setText('')
        self.send_info.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.send_info.tx.setPlainText(self.raw_tx)
        self.w.combo.setEnabled(True)
        self.value.setReadOnly(False)
