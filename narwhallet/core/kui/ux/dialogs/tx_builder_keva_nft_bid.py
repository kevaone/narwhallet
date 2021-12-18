import json
from PyQt5 import QtCore
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy)

from narwhallet.control.shared import MShared
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.models.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallets import MWallets
from narwhallet.core.kcl.models.transaction_builder import MTransactionBuilder
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.wallet_combobox import WalletComboBox
from narwhallet.core.kui.ux.widgets.namespace_combobox import NamespaceComboBox
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame
from narwhallet.core.kui.ux.widgets.auction_info_frame import AuctionInfoFrame
from narwhallet.core.kui.ux.widgets.dialog_buttonbox import DialogButtonBox


class Ui_keva_op_nft_bid_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallets: MWallets = None
        self.cache: MCache = None
        self.kex = None
        self.new_tx = MTransactionBuilder()
        self.bid_tx = MTransactionBuilder()
        self.raw_tx = None

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
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

        self.combo_wallet = WalletComboBox()
        self.combo_ns = NamespaceComboBox()

        self.bid_nft_tx_l = QLabel(self)
        self.bid_nft_tx = QLineEdit(self)
        self.bid_amount_l = QLabel(self)
        self.bid_amount = QLineEdit(self)
        self.auction_info = AuctionInfoFrame()
        self.send_info = SendInfoFrame()
        self.buttonBox = DialogButtonBox(self)

        self.setObjectName('keva_op_nft_bid_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.combo_wallet)
        self.verticalLayout.addLayout(self.combo_ns)

        self.hl_2.addWidget(self.bid_nft_tx_l)
        self.hl_2.addWidget(self.bid_nft_tx)
        self.hl_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_2)

        self.hl_3.addWidget(self.bid_amount_l)
        self.hl_3.addWidget(self.bid_amount)
        self.hl_3.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_3)

        self.verticalLayout.addWidget(self.auction_info)
        self.verticalLayout.addWidget(self.send_info)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.combo_wallet.combo.currentTextChanged.connect(self.txb_w_changed)
        self.combo_ns.combo.currentTextChanged.connect(self.txb_ns_changed)
        self.buttonBox.cancel.clicked.connect(self.reject)
        self.buttonBox.next.clicked.connect(self.txb_build_simple_send)
        self.buttonBox.back.clicked.connect(self.back_click)

        self.bid_nft_tx.textChanged.connect(self.check_tx_is_auction)
        self.bid_amount.textChanged.connect(self.check_next)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('keva_op_nft_bid_dlg',
                                       'Narwhallet - Create Namespace'))
        (self.bid_nft_tx_l
         .setText(_translate('keva_op_nft_bid_dlg', 'Bid on TX: ')))
        (self.bid_amount_l
         .setText(_translate('keva_op_nft_bid_dlg', 'Bid Amount: ')))

    def check_next(self):
        if (self.combo_wallet.combo.currentText() != '-' and
                self.combo_ns.combo.currentText() != '-' and
                self.auction_info.nft_name.text() != '' and
                self.auction_info.nft_desc.text() != '' and
                # self.nft_hashtags.text() != '' and
                self.auction_info.nft_price.text() != ''):
            self.buttonBox.next.setEnabled(True)
        else:
            self.buttonBox.next.setEnabled(False)

    def check_tx_is_auction(self):
        _nft_tx = self.bid_nft_tx.text()

        _nft_tx = MShared.check_tx_is_auction(_nft_tx, self.kex, self.cache)
        if _nft_tx[0] is True:
            self.auction_info.nft_name.setText(_nft_tx[2]['displayName'])
            self.auction_info.nft_desc.setText(_nft_tx[2]['desc'])
            if 'hashtags' in _nft_tx[1]:
                self.auction_info.nft_hashtags.setText(_nft_tx[1]['hashtags'])
            self.auction_info.nft_price.setText(_nft_tx[2]['price'])
            self.auction_info.nft_ns.setText(_nft_tx[1])
            self.auction_info.nft_address.setText(_nft_tx[2]['addr'])

            self.check_next()

    def build_bid(self):
        self.bid_tx.set_version(Ut.hex_to_bytes('00710000'))
        _n = self.combo_wallet.combo.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        _namespace_reservation = 1000000

        locale = QLocale()
        _b_amount = locale.toDouble(self.bid_amount.text())
        _bid_amount = int(_b_amount[0] * 100000000)

        _auc = {}
        _auc['displayName'] = self.auction_info.nft_name.text()
        _ns = self.auction_info.nft_ns.text()
        _ns_key = '\x01_KEVA_NS_'
        _ns_value = json.dumps(_auc, separators=(',', ':'))
        _trans_address = wallet.get_unused_address()
        _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                         _trans_address)
        _sh = Scripts.compile(_sh, True)
        _ = self.bid_tx.add_output(_namespace_reservation, _trans_address)
        self.bid_tx.vout[0].scriptPubKey.set_hex(_sh)
        _ = self.bid_tx.add_output(_bid_amount, self.auction_info.nft_address.text())

        self.bid_tx.set_availible_usxo(wallet, False, True, self.combo_ns.combo.currentData().split(':')[0], self.cache, self.kex)
        _inp_sel, _need_change, _est_fee = self.bid_tx.select_inputs(True)

        if _inp_sel is True:
            _, _, _fv = self.bid_tx.get_current_values(True)
            _cv = _fv - _est_fee

            if _need_change is True:
                _ = self.bid_tx.add_output(_cv, _trans_address)

            self.bid_tx.txb_preimage(wallet, SIGHASH_TYPE.ALL_ANYONECANPAY)

    def txb_w_changed(self, data):
        if data != '-':
            self.set_namespace_combo()

        self.check_next()

    def txb_ns_changed(self, data):
        if data not in ('-', ''):
            self.auction_info.nft_name.setText(self.combo_ns.combo.currentText().split(' - ')[1])

        self.check_next()

    def set_namespace_combo(self):
        self.combo_ns.combo.clear()
        self.combo_ns.combo.addItem('-', '-')
        self.auction_info.nft_name.setText('')
        _n = self.combo_wallet.combo.currentData()
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

                    self.combo_ns.combo.addItem(_block+' - '+_name, _ns+':'+tx['a'])

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

    # def set_availible_usxo(self, isChangeOp: bool, isBidOp: bool = False):
    #     _n = self.combo_wallet.currentData()
    #     wallet = self.wallets.get_wallet_by_name(_n)

    #     _tmp_usxo = wallet.get_usxos()
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

    #         if ('OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm):
    #             if isBidOp is False:
    #                 _used = False
    #                 for _vin in self.bid_tx.vin:
    #                     if _vin.txid == _tx.txid:
    #                         _used = True
    #                         print('used')

    #                 if _used is False:
    #                     _usxos.append(tx)
    #             else:
    #                 _usxos.append(tx)
    #         elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
    #                 and isChangeOp is True):

    #             _test = _tx.vout[tx['tx_pos']].scriptPubKey.asm.split(' ')[1]
    #             _test = self.cache.ns.convert_to_namespaceid(_test)

    #             if _test == self.combo_ns.currentData().split(':')[0]:
    #                 _nsusxo = tx

    #     if _nsusxo is not None and isChangeOp is True:
    #         _usxos.insert(0, _nsusxo)
    #     elif _nsusxo is None and isChangeOp is True:
    #         _usxos = []

    #     if isBidOp is False:
    #         self.new_tx.inputs_to_spend = _usxos
    #     else:
    #         self.bid_tx.inputs_to_spend = _usxos

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def txb_build_simple_send(self):
        _n = self.combo_wallet.combo.currentData()
        wallet = self.wallets.get_wallet_by_name(_n)
        self.build_bid()
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_availible_usxo(wallet, True, False, self.combo_ns.combo.currentData().split(':')[0], self.cache, self.kex)
        _namespace_reservation = 1000000
        _ns_dat = self.combo_ns.combo.currentData().split(':')
        _ns = _ns_dat[0]
        _ns_address = _ns_dat[1]

        _ns_key = (Ut.hex_to_bytes('0001') +
                   Ut.hex_to_bytes(self.bid_nft_tx.text()))
        _ns_value = self.bid_tx.to_psbt()
        _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                         _ns_address)
        _sh = Scripts.compile(_sh, True)

        _ = self.new_tx.add_output(_namespace_reservation, _ns_address)
        self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            _cv = _fv - _est_fee

            if _need_change is True:
                _ = self.new_tx.add_output(_cv, _ns_address)

            self.new_tx.txb_preimage(wallet, SIGHASH_TYPE.ALL)
            _stx = self.new_tx.serialize_tx()

            self.send_info.fee.setText(str(_est_fee/100000000))
            self.send_info.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.send_info.tx.setPlainText(self.raw_tx)

            self.combo_wallet.combo.setEnabled(False)
            self.combo_ns.combo.setEnabled(False)
            self.bid_nft_tx.setReadOnly(True)
            self.bid_amount.setReadOnly(True)

            self.buttonBox.next.setVisible(False)
            self.buttonBox.back.setVisible(True)
            self.buttonBox.send.setEnabled(True)
        else:
            self.new_tx.set_vin([])
            self.new_tx.set_vout([])
            self.new_tx.input_signatures = []
            self.bid_tx.set_vin([])
            self.bid_tx.set_vout([])
            self.bid_tx.input_signatures = []

    def back_click(self):
        self.buttonBox.next.setVisible(True)
        self.buttonBox.back.setVisible(False)
        self.buttonBox.send.setEnabled(False)

        self.send_info.fee.setText('')
        self.send_info.txsize.setText('')
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.bid_tx.set_vin([])
        self.bid_tx.set_vout([])
        self.bid_tx.input_signatures = []
        self.send_info.tx.setPlainText(self.raw_tx)

        self.combo_wallet.combo.setEnabled(True)
        self.combo_ns.combo.setEnabled(True)
        self.bid_nft_tx.setReadOnly(False)
        self.bid_amount.setReadOnly(False)
