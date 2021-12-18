from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QComboBox, QPushButton, QPlainTextEdit)

from narwhallet.control.shared import MShared
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.models.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallet import MWallet
from narwhallet.core.kcl.models.transaction_builder import MTransactionBuilder
from narwhallet.core.kcl.models.psbt_decoder import keva_psbt
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_keva_op_nft_accept_bid_dlg(QDialog):
    def setupUi(self):
        # _al_center = QtCore.Qt.AlignCenter
        _bb_br_ar = QDialogButtonBox.ActionRole
        _bb_br_ac = QDialogButtonBox.AcceptRole
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallet: MWallet = None
        self.cache: MCache = None
        self.kex = None
        self.new_tx = MTransactionBuilder()
        self.raw_tx = None

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        # self.label_1 = QLabel(self)
        # _pic = QtGui.QPixmap(MShared.get_resource_path('narwhal.png'))

        self.hl_0 = QHBoxLayout()
        self.hl_1 = QHBoxLayout()
        self.hl_2 = QHBoxLayout()
        self.hl_3 = QHBoxLayout()
        self.hl_4 = QHBoxLayout()
        self.hl_5 = QHBoxLayout()
        self.hl_6 = QHBoxLayout()
        self.hl_7 = QHBoxLayout()
        self.hl_8 = QHBoxLayout()
        self.hl_9 = QHBoxLayout()
        self.hl_10 = QHBoxLayout()

        self.combo_wallet_l = QLabel(self)
        self.combo_wallet = QComboBox(self)

        self.bid_nft_tx_l = QLabel(self)
        self.bid_nft_tx = QLineEdit(self)
        self.bid_amount_l = QLabel(self)
        self.bid_amount = QLabel(self)

        self.nft_name_l = QLabel(self)
        self.nft_name = QLabel(self)
        self.nft_desc_l = QLabel(self)
        self.nft_desc = QLabel(self)
        self.nft_hashtags_l = QLabel(self)
        self.nft_hashtags = QLabel(self)
        self.nft_price_l = QLabel(self)
        self.nft_price = QLabel(self)
        self.nft_ns_l = QLabel(self)
        self.nft_ns = QLabel(self)
        self.nft_shortcode_l = QLabel(self)
        self.nft_shortcode = QLabel(self)
        self.nft_address_l = QLabel(self)
        self.nft_address = QLabel(self)
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

        self.setObjectName('keva_op_nft_accept_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        # self.label_1.setAlignment(_al_center)
        # self.label_1.setContentsMargins(0, 0, 0, 0)
        # self.label_1.setPixmap(_pic)
        self.combo_wallet.addItem('-', '-')
        self.bid_nft_tx.setReadOnly(True)
        self.tx.setMaximumHeight(65)
        self.tx.setReadOnly(True)
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
        self.hl_0.addWidget(self.combo_wallet_l)
        self.hl_0.addWidget(self.combo_wallet)
        self.hl_0.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_0)
        self.hl_1.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_1)

        self.hl_2.addWidget(self.bid_nft_tx_l)
        self.hl_2.addWidget(self.bid_nft_tx)
        self.verticalLayout.addLayout(self.hl_2)

        self.hl_3.addWidget(self.bid_amount_l)
        self.hl_3.addWidget(self.bid_amount)
        self.hl_3.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_3)

        self.hl_4.addWidget(self.nft_name_l)
        self.hl_4.addWidget(self.nft_name)
        self.hl_4.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_4)
        self.hl_5.addWidget(self.nft_desc_l)
        self.hl_5.addWidget(self.nft_desc)
        self.hl_5.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_5)
        self.hl_6.addWidget(self.nft_hashtags_l)
        self.hl_6.addWidget(self.nft_hashtags)
        self.hl_6.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_6)
        self.hl_7.addWidget(self.nft_price_l)
        self.hl_7.addWidget(self.nft_price)
        self.hl_7.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_7)
        self.hl_8.addWidget(self.nft_ns_l)
        self.hl_8.addWidget(self.nft_ns)
        self.hl_8.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_8)
        self.hl_9.addWidget(self.nft_shortcode_l)
        self.hl_9.addWidget(self.nft_shortcode)
        self.hl_9.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_9)
        self.hl_10.addWidget(self.nft_address_l)
        self.verticalLayout.addLayout(self.hl_10)
        self.verticalLayout.addWidget(self.nft_address)
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
        self.cancel_btn.clicked.connect(self.reject)
        self.next_btn.clicked.connect(self.txb_build_simple_send)
        self.back_btn.clicked.connect(self.back_click)

        self.bid_nft_tx.textChanged.connect(self.check_tx_is_bid)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('keva_op_nft_accept_dlg',
                                       'Narwhallet - Create Namespace'))
        (self.combo_wallet_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Wallet:')))
        (self.bid_nft_tx_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Bid on TX: ')))
        (self.bid_amount_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Bid Amount: ')))
        self.nft_name_l.setText(_translate('keva_op_nft_accept_dlg', 'Name: '))
        (self.nft_desc_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Description: ')))
        (self.nft_hashtags_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Hashtags: ')))
        (self.nft_price_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Asking Price: ')))
        self.nft_ns_l.setText(_translate('keva_op_nft_accept_dlg', 'NS: '))
        (self.nft_shortcode_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Shortcode: ')))
        (self.nft_address_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Payment Address: ')))

        self.cancel_btn.setText(_translate('keva_op_nft_accept_dlg', 'Cancel'))
        self.send_btn.setText(_translate('keva_op_nft_accept_dlg', 'Send'))
        self.next_btn.setText(_translate('keva_op_nft_accept_dlg', 'Next'))
        self.back_btn.setText(_translate('keva_op_nft_accept_dlg', 'Back'))
        self.txsize_l.setText(_translate('keva_op_nft_accept_dlg', 'size:'))
        self.fee_l.setText(_translate('keva_op_nft_accept_dlg', 'Fee (KVA):'))
        self.feerate_l.setText(_translate('keva_op_nft_accept_dlg',
                                          'Fee Rate (Satoshi per byte):'))
        self.tx_l.setText(_translate('keva_op_nft_accept_dlg', 'Raw TX -'))

    def check_next(self):
        if (self.combo_wallet.currentText() != '-' and
                self.bid_amount.text() != '' and
                self.nft_ns.text() != '' and
                self.nft_price.text() != ''):
            self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)

    def check_tx_is_bid(self):
        _nft_tx = self.bid_nft_tx.text()
        _nft_tx = MShared.check_tx_is_bid(_nft_tx, self.kex, self.cache)
        if _nft_tx[0] is True:
            _bid_psbt = keva_psbt(_nft_tx[2])
            _sh = Scripts.P2SHAddressScriptHash(self.nft_address.text())
            _sh = Scripts.compile(_sh, True)
            # _sh = (Scripts.P2SHAddressScriptHash
            #        .compile([self.nft_address.text()], True))
            if _bid_psbt.tx.vout[1].scriptPubKey.hex == _sh:
                (self.bid_amount
                 .setText(str(_bid_psbt.tx.vout[1].value/100000000)))
                self.new_tx = _bid_psbt.tx
                _idx = 0
                for _, _r in enumerate(_bid_psbt.psbt_records):
                    if _r[0] == 'PSBT_IN_WITNESS_UTXO':
                        self.new_tx.vin[_idx].tb_value = (Ut
                                                          .bytes_to_int(
                                                              _r[2][:8],
                                                              'little'))
                    elif _r[0] == 'PSBT_IN_PARTIAL_SIG':
                        (self.new_tx.input_signatures
                         .append([Ut.bytes_to_hex(_r[2]),
                                 Ut.bytes_to_hex(_r[1][1:])]))
                    elif _r[0] == 'PSBT_IN_REDEEM_SCRIPT':
                        (self.new_tx.vin[_idx].scriptSig
                         .set_hex(Ut.bytes_to_hex(_r[2])))
                        _idx += 1

            self.check_next()
        else:
            self.next_btn.setEnabled(False)

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

    # def set_availible_usxo(self):
    #     _tmp_usxo = self.wallet.get_usxos()
    #     _usxos = []
    #     _nsusxo = None

    #     for tx in _tmp_usxo:
    #         _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

    #         if _tx is None:
    #             _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)
    #         if _tx is not None and isinstance(_tx, dict):
    #             _tx = self.cache.tx.add_from_json(_tx)

    #         if self._test_tx(_tx) is False:
    #             continue

    #         if 'OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
    #             _test = _tx.vout[tx['tx_pos']].scriptPubKey.asm.split(' ')[1]
    #             _test = self.cache.ns.convert_to_namespaceid(_test)

    #             if _test == self.nft_ns.text():
    #                 _nsusxo = tx

    #     if _nsusxo is not None:
    #         _usxos.insert(0, _nsusxo)
    #     elif _nsusxo is None:
    #         _usxos = []

    #     self.new_tx.inputs_to_spend = _usxos

    # def txb_preimage(self, tx: MTransactionBuilder, hash_type: SIGHASH_TYPE):
    #     wallet = self.wallet

    #     _vin_idx = tx.vin[-1]
    #     _npk = _vin_idx.tb_address
    #     _npkc = _vin_idx.tb_address_chain
    #     _pk = wallet.get_publickey_raw(_npk, _npkc)
    #     _sighash = tx.make_preimage(len(tx.vin)-1, _pk, hash_type)
    #     _sig = wallet.sign_message(_npk, _sighash, _npkc)
    #     _script = Scripts.P2WPKHScriptSig(_pk)
    #     _script = Scripts.compile(_script, True)
    #     # _script = Scripts.P2WPKHScriptSig.compile([_pk], True)
    #     _vin_idx.scriptSig.set_hex(_script)
    #     (tx.input_signatures.append(
    #      [_sig+Ut.bytes_to_hex(Ut.to_cuint(hash_type.value)), _pk]))

    #     _addr = wallet.get_address_by_index(_npk, False)
    #     _r = Scripts.P2SHAddressScriptHash(_addr)
    #     _r = Scripts.compile(_r, False)
    #     # _r = Scripts.P2SHAddressScriptHash.compile([_addr], False)

    #     _ref = Ut.int_to_bytes(_vin_idx.tb_value, 8, 'little')
    #     _ref = _ref + Ut.to_cuint(len(_r)) + _r
    #     tx.input_ref_scripts.append(_ref)

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def txb_build_simple_send(self):
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_availible_usxo(self.wallet, False, False, self.nft_ns.text(), self.cache, self.kex)

        if len(self.new_tx.inputs_to_spend) != 1:
            _inp_sel = False
        else:
            tx = self.new_tx.inputs_to_spend[0]
            self.new_tx.add_input(tx['value'],
                                  str(tx['a_idx'])+':'+str(tx['ch']),
                                  tx['tx_hash'], tx['tx_pos'])
            _inp_sel = True

        if _inp_sel is True:
            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL_ANYONECANPAY)
            _stx = self.new_tx.serialize_tx()
            _, _, _fv = self.new_tx.get_current_values(False)
            self.fee.setText(str(_fv/100000000))
            self.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.tx.setPlainText(self.raw_tx)

            self.bid_nft_tx.setReadOnly(True)
            self.next_btn.setVisible(False)
            self.back_btn.setVisible(True)
            self.send_btn.setEnabled(True)
        else:
            self.new_tx.set_vin([])
            self.new_tx.set_vout([])
            self.new_tx.input_signatures = []

    def back_click(self):
        self.next_btn.setVisible(True)
        self.back_btn.setVisible(False)
        self.send_btn.setEnabled(False)

        self.fee.setText('')
        self.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.tx.setPlainText(self.raw_tx)
        self.bid_nft_tx.setReadOnly(False)
