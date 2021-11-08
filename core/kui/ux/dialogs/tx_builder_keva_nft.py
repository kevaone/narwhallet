import json
import os
from PyQt5 import QtCore, QtGui
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


class Ui_keva_op_nft_dlg(QDialog):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignCenter
        _bb_br_ar = QDialogButtonBox.ActionRole
        _bb_br_ac = QDialogButtonBox.AcceptRole
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.kex = None
        self.new_tx = MTransactionBuilder()
        self.raw_tx = None

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_1 = QLabel(self)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))

        self.hl_0 = QHBoxLayout()
        self.hl_1 = QHBoxLayout()
        self.hl_2 = QHBoxLayout()
        self.hl_3 = QHBoxLayout()
        self.hl_4 = QHBoxLayout()
        self.hl_5 = QHBoxLayout()

        self.combo_wallet_l = QLabel(self)
        self.combo_wallet = QComboBox(self)

        self.combo_ns_l = QLabel(self)
        self.combo_ns = QComboBox(self)

        self.nft_name_l = QLabel(self)
        self.nft_name = QLineEdit(self)
        self.nft_desc_l = QLabel(self)
        self.nft_desc = QLineEdit(self)
        self.nft_hashtags_l = QLabel(self)
        self.nft_hashtags = QLineEdit(self)
        self.nft_price_l = QLabel(self)
        self.nft_price = QLineEdit(self)

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

        self.setObjectName('keva_op_nft_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.combo_wallet.addItem('-', '-')
        self.combo_ns.addItem('-', '-')
        self.combo_ns.setMinimumWidth(250)
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

        self.horizontalLayout_1.addWidget(self.label_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.hl_0.addWidget(self.combo_wallet_l)
        self.hl_0.addWidget(self.combo_wallet)
        self.hl_0.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_0)
        self.hl_1.addWidget(self.combo_ns_l)
        self.hl_1.addWidget(self.combo_ns)
        self.hl_1.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_1)
        self.hl_2.addWidget(self.nft_name_l)
        self.hl_2.addWidget(self.nft_name)
        self.hl_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_2)
        self.hl_3.addWidget(self.nft_desc_l)
        self.hl_3.addWidget(self.nft_desc)
        self.hl_3.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_3)
        self.hl_4.addWidget(self.nft_hashtags_l)
        self.hl_4.addWidget(self.nft_hashtags)
        self.hl_4.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_4)
        self.hl_5.addWidget(self.nft_price_l)
        self.hl_5.addWidget(self.nft_price)
        self.hl_5.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_5)
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
        self.combo_wallet.currentTextChanged.connect(self.txb_w_changed)
        self.combo_ns.currentTextChanged.connect(self.txb_ns_changed)
        self.cancel_btn.clicked.connect(self.reject)
        self.next_btn.clicked.connect(self.txb_build_simple_send)
        self.back_btn.clicked.connect(self.back_click)

        self.nft_name.textChanged.connect(self.check_next)
        self.nft_desc.textChanged.connect(self.check_next)
        self.nft_hashtags.textChanged.connect(self.check_next)
        self.nft_price.textChanged.connect(self.check_next)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('keva_op_send_dlg',
                                       'Narwhallet - Create Namespace'))
        self.combo_wallet_l.setText(_translate('keva_op_send_dlg', 'Wallet:'))
        self.combo_ns_l.setText(_translate('keva_op_send_dlg', 'Namespace:'))
        self.nft_name_l.setText(_translate('keva_op_send_dlg', 'Name: '))
        (self.nft_desc_l
         .setText(_translate('keva_op_send_dlg', 'Description: ')))
        (self.nft_hashtags_l
         .setText(_translate('keva_op_send_dlg', 'Hashtags: ')))
        self.nft_price_l.setText(_translate('keva_op_send_dlg', 'Price: '))

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
        if (self.combo_wallet.currentText() != '-' and
                self.combo_ns.currentText() != '-' and
                self.nft_name.text() != '' and
                self.nft_desc.text() != '' and
                # self.nft_hashtags.text() != '' and
                self.nft_price.text() != ''):
            self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)

    def txb_w_changed(self, data):
        if data != '-':
            self.set_namespace_combo()

        self.check_next()

    def txb_ns_changed(self, data):
        if data not in ('-', ''):
            self.nft_name.setText(self.combo_ns.currentText().split(' - ')[1])
            self.set_availible_usxo(True)

        self.check_next()

    def set_namespace_combo(self):
        self.combo_ns.clear()
        self.combo_ns.addItem('-', '-')
        self.nft_name.setText('')
        _n = self.combo_wallet.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        MShared.list_unspents(wallet, self.kex)
        _tmp_usxo = wallet.get_usxos()
        for tx in _tmp_usxo:
            # TODO Check for usxo's used by bids
            _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)
                if _tx is not None:
                    _tx = self.cache.tx.add_from_json(_tx)

            if _tx is not None:
                if ('OP_KEVA'
                        in _tx.vout[tx['tx_pos']].scriptPubKey.asm):

                    _ns = _tx.vout[tx['tx_pos']].scriptPubKey.asm.split(' ')[1]
                    _ns = self.cache.ns.convert_to_namespaceid(_ns)
                    _block = self.cache.ns.ns_block(_ns)[0]
                    _b_s = str(_block[0])
                    _block = str(str(len(_b_s)) + _b_s + str(_block[1]))
                    _name = (self.cache.ns.get_namespace_by_key_value(
                        _ns, '\x01_KEVA_NS_'))
                    if len(_name) == 0:
                        _name = (self.cache.ns
                                 .get_namespace_by_key_value(_ns, '_KEVA_NS_'))
                        if len(_name) > 0:
                            _name = _name[0][0]
                    else:
                        _name = _name[0][0]

                    if 'displayName' in _name:
                        _name = json.loads(_name)['displayName']

                    self.combo_ns.addItem(_block+' - '+_name, _ns+':'+tx['a'])

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

    def set_availible_usxo(self, isChangeOp: bool):
        _n = self.combo_wallet.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)

        _tmp_usxo = wallet.get_usxos()
        _usxos = []
        _nsusxo = None

        for tx in _tmp_usxo:
            _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)
            if _tx is not None and isinstance(_tx, dict):
                _tx = self.cache.tx.add_from_json(_tx)

            if self._test_tx(_tx) is False:
                continue

            if ('OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm):
                _usxos.append(tx)
            elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
                    and isChangeOp is True):

                _test = _tx.vout[tx['tx_pos']].scriptPubKey.asm.split(' ')[1]
                _test = self.cache.ns.convert_to_namespaceid(_test)

                if _test == self.combo_ns.currentData().split(':')[0]:
                    _nsusxo = tx

        if _nsusxo is not None and isChangeOp is True:
            _usxos.insert(0, _nsusxo)
        elif _nsusxo is None and isChangeOp is True:
            _usxos = []

        self.new_tx.inputs_to_spend = _usxos

    def txb_preimage(self):
        _n = self.combo_wallet.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        self.new_tx.input_signatures = []

        for c, _vin_idx in enumerate(self.new_tx.vin):
            _npk = _vin_idx.tb_address
            _npkc = _vin_idx.tb_address_chain
            _pk = wallet.get_publickey_raw(_npk, _npkc)
            _sighash = self.new_tx.make_preimage(c, _pk)
            _sig = wallet.sign_message(_npk, _sighash, _npkc)
            _script = Scripts.P2WPKHScriptSig.compile([_pk], True)
            _vin_idx.scriptSig.set_hex(_script)
            # HACK - Note assuming signatre was SIGHASH_TYPE.ALL
            self.new_tx.input_signatures.append([_sig+'01', _pk])

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def txb_build_simple_send(self):
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        _n = self.combo_wallet.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        _namespace_reservation = 1000000
        _ns_dat = self.combo_ns.currentData().split(':')
        _ns = _ns_dat[0]
        _ns_address = _ns_dat[1]

        _auc = {}
        _auc['displayName'] = self.nft_name.text()
        _auc['price'] = str(self.nft_price.text())
        _auc['desc'] = self.nft_desc.text()

        _tags = {}
        _hashtags = self.nft_hashtags.text().split(' ')
        for tag in _hashtags:
            tag = tag.split(',')
            for t in tag:
                t = t.replace('#', '').strip()
                if t != '':
                    _tags['#' + t] = ''
        _tags = list(_tags.keys())
        if len(_tags) > 0:
            _auc['hashtags'] = _tags
        _auc['addr'] = wallet.get_unused_change_address()

        _ns_key = '\x01_KEVA_NS_'
        _ns_value = json.dumps(_auc, separators=(',', ':'))

        _sh = Scripts.KevaKeyValueUpdate.compile([_ns, _ns_key,
                                                  _ns_value,
                                                  _ns_address], True)

        _ = self.new_tx.add_output(_namespace_reservation, _ns_address)
        self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        # print('_inp_sel, _need_change, _est_fee',
        #       _inp_sel, _need_change, _est_fee)

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            _cv = _fv - _est_fee
            # print('_cv', _cv)

            if _need_change is True:
                _ = self.new_tx.add_output(_cv, _ns_address)

            self.txb_preimage()
            _stx = self.new_tx.serialize_tx()

            self.fee.setText(str(_est_fee/100000000))
            self.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.tx.setPlainText(self.raw_tx)

            self.combo_wallet.setEnabled(False)
            self.combo_ns.setEnabled(False)
            self.nft_name.setReadOnly(True)
            self.nft_desc.setReadOnly(True)
            self.nft_hashtags.setReadOnly(True)
            self.nft_price.setReadOnly(True)

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

        self.fee.setText('')
        self.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.tx.setPlainText(self.raw_tx)

        self.combo_wallet.setEnabled(True)
        self.combo_ns.setEnabled(True)
        self.nft_name.setReadOnly(False)
        self.nft_desc.setReadOnly(False)
        self.nft_hashtags.setReadOnly(False)
        self.nft_price.setReadOnly(False)
        # self.address.setReadOnly(False)
