import json
from PyQt5 import QtCore
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from narwhallet.control.shared import MShared
from narwhallet.core.kex import KEXclient
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction import keva_psbt
from narwhallet.core.kcl.wallet.wallets import MWallets
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kui.ux.widgets.wallet_combobox import WalletComboBox
from narwhallet.core.kui.ux.widgets.amount_input import AmountInput
from narwhallet.core.kui.ux.widgets.address_input import AddressInput
from narwhallet.core.kui.ux.widgets.address_combobox import AddressComboBox
from narwhallet.core.kui.ux.widgets.namespace_combobox import NamespaceComboBox
from narwhallet.core.kui.ux.widgets.namespace_special_keys_combobox import NamespaceSpecialKeysComboBox
from narwhallet.core.kui.ux.widgets.namespace_key_input import NamespaceKeyInput
from narwhallet.core.kui.ux.widgets.namespace_value_input import NamespaceValueInput
from narwhallet.core.kui.ux.widgets.transaction_input import TransactionInput
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame
from narwhallet.core.kui.ux.widgets.auction_info_frame import AuctionInfoFrame
from narwhallet.core.kui.ux.widgets.dialog_buttonbox import DialogButtonBox
from narwhallet.core.kui.ux.widgets.generator import UShared

TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000


class Ui_send_dlg(QDialog):
    def setupUi(self, mode):
        self.mode: int = mode
        self.wallets: MWallets = None
        self.wallet: MWallet = None
        self.cache: MCache = None
        self.kex: KEXclient = None
        self.new_tx = MTransactionBuilder()
        self.bid_tx = MTransactionBuilder()
        self.raw_tx: str = ''
        self.action: str = ''
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.wallet_combo = WalletComboBox()
        self.ns_combo = NamespaceComboBox()
        self.amount_input = AmountInput()
        self.address_input = AddressInput()
        self.address_combo = AddressComboBox()
        self.transaction_input = TransactionInput()
        self.special_keys_combo = NamespaceSpecialKeysComboBox()
        self.namespace_key_input = NamespaceKeyInput()
        self.namespace_value_input = NamespaceValueInput()
        self.bid_input = AmountInput()
        self.auction_info = AuctionInfoFrame()
        self.send_info = SendInfoFrame()
        self.buttonBox = DialogButtonBox(self)

        self.address_select = QPushButton(self)

        # self.setMinimumSize(QtCore.QSize(485, 225))

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.wallet_combo)
        self.verticalLayout.addLayout(self.ns_combo)
        self.verticalLayout.addLayout(self.amount_input)
        self.verticalLayout.addLayout(self.address_input)
        self.verticalLayout.addLayout(self.address_combo)
        self.verticalLayout.addWidget(self.address_select)
        self.verticalLayout.addLayout(self.transaction_input)
        self.verticalLayout.addLayout(self.special_keys_combo)
        self.verticalLayout.addLayout(self.namespace_key_input)
        self.verticalLayout.addLayout(self.namespace_value_input)
        self.verticalLayout.addLayout(self.bid_input)
        self.verticalLayout.addWidget(self.auction_info)
        self.verticalLayout.addWidget(self.send_info)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.init_mode()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.cancel.clicked.connect(self.reject)
        self.buttonBox.next.clicked.connect(self.build_send)
        self.buttonBox.back.clicked.connect(self.back_click)
        (self.wallet_combo.combo.currentTextChanged
         .connect(self.wallet_combo_changed))
        (self.ns_combo.combo.currentTextChanged
         .connect(self.ns_combo_changed))
        (self.special_keys_combo.combo.currentTextChanged
         .connect(self.special_keys_combo_changed))
        self.amount_input.amount.textChanged.connect(self.check_next)
        self.address_input.address.textChanged.connect(self.check_next)
        self.address_combo.combo.currentTextChanged.connect(self.check_next)
        (self.namespace_key_input.key.textChanged
         .connect(self.check_ns_key_input))
        self.namespace_value_input.value.textChanged.connect(self.check_next)
        self.address_select.clicked.connect(self.select_swap)
        self.auction_info.nft_desc.textChanged.connect(self.check_next)
        self.auction_info.nft_name.textChanged.connect(self.check_next)
        self.auction_info.nft_hashtags.textChanged.connect(self.check_next)
        self.auction_info.nft_price.textChanged.connect(self.check_next)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('send_dlg', 'Narwhallet - Send'))
        self.address_select.setText(_translate('send_dlg', 'Book'))

    def _mode_simple_send(self):
        # Simple Send
        self.setWindowTitle('Narwhallet - Send')
        self.wallet_combo.show()
        self.ns_combo.hide()
        self.amount_input.show()
        self.address_input.show()
        self.address_combo.hide()
        self.transaction_input.hide()
        self.namespace_key_input.hide()
        self.namespace_value_input.hide()
        self.bid_input.hide()
        self.auction_info.hide()

    def _mode_multi_sig_send(self):
        # Multi Sig Send
        self.setWindowTitle('Narwhallet - Multi-Sig Send')

    def _mode_namespace_create(self):
        # Namespace Create
        self.setWindowTitle('Narwhallet - Create Namespace')
        self.wallet_combo.show()
        self.ns_combo.hide()
        self.amount_input.hide()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.hide()
        self.namespace_value_input.show()
        self.bid_input.hide()
        self.auction_info.hide()
        self.namespace_value_input.value.setMinimumHeight(28)
        self.namespace_value_input.value.setMaximumHeight(28)

    def _mode_namespace_create_key(self):
        # Namespace Key Create
        self.setWindowTitle('Narwhallet - Create Key')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.hide()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.special_keys_combo.show()
        self.namespace_key_input.show()
        self.namespace_value_input.show()
        self.bid_input.hide()
        self.auction_info.hide()
        self.wallet_combo.combo.setEnabled(False)
        self.ns_combo.combo.setEnabled(False)

    def _mode_namespace_update_key(self):
        # Namespace Key Update
        self.setWindowTitle('Narwhallet - Update Key')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.hide()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_value_input.show()
        self.bid_input.hide()
        self.auction_info.hide()
        self.wallet_combo.combo.setEnabled(False)
        self.ns_combo.combo.setEnabled(False)
        self.namespace_key_input.key.setReadOnly(True)

    def _mode_namespace_delete_key(self):
        # Namespace Key Delete
        self.setWindowTitle('Narwhallet - Delete Key')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.hide()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_value_input.hide()
        self.bid_input.hide()
        self.auction_info.hide()
        self.wallet_combo.combo.setEnabled(False)
        self.ns_combo.combo.setEnabled(False)
        self.namespace_key_input.key.setReadOnly(True)

    def _mode_create_auction(self):
        # Namespace Auction
        self.setWindowTitle('Narwhallet - Create Auction')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.hide()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.hide()
        self.namespace_value_input.hide()
        self.bid_input.hide()
        self.auction_info.show()
        self.namespace_key_input.key.setText('\x01_KEVA_NS_')
        self.namespace_key_input.key.setReadOnly(True)
        self.auction_info.nft_ns.setVisible(False)
        self.auction_info.ns_l.setVisible(False)
        self.auction_info.nft_address.setReadOnly(True)

    def _mode_create_bid(self):
        # Namespace Bid
        self.setWindowTitle('Narwhallet - Create Bid')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.show()
        self.address_input.hide()
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_value_input.hide()
        self.bid_input.hide()
        self.auction_info.show()
        self.address_select.setVisible(False)
        self.auction_info.nft_desc.setReadOnly(True)
        self.auction_info.nft_name.setReadOnly(True)
        self.auction_info.nft_hashtags.setReadOnly(True)
        self.auction_info.nft_ns.setReadOnly(True)
        self.auction_info.nft_address.setReadOnly(True)
        self.auction_info.nft_price.setReadOnly(True)

    def _mode_accept_bid(self):
        # Namespace Accept Bid
        self.setWindowTitle('Narwhallet - Accept Bid')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.show()
        self.address_input.hide()
        self.address_combo.hide()
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_value_input.hide()
        self.bid_input.hide()
        self.auction_info.show()
        self.wallet_combo.combo.setEnabled(False)
        self.ns_combo.combo.setEnabled(False)
        self.address_select.setVisible(False)
        # self.bid_input.amount.setReadOnly(True)
        self.auction_info.nft_desc.setReadOnly(True)
        self.auction_info.nft_name.setReadOnly(True)
        self.auction_info.nft_hashtags.setReadOnly(True)
        self.auction_info.nft_ns.setReadOnly(True)
        self.auction_info.nft_address.setReadOnly(True)
        self.auction_info.nft_price.setReadOnly(True)

    def _mode_namespace_transfer(self):
        # Namespace Transfer
        self.setWindowTitle('Narwhallet - Namespace Transfer')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.hide()
        self.address_input.show()
        self.address_combo.hide()
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_value_input.show()
        self.bid_input.hide()
        self.auction_info.hide()
        self.wallet_combo.combo.setEnabled(False)
        self.ns_combo.combo.setEnabled(False)

    def _mode_namespace_reward(self):
        # Namespace Key Reward
        self.setWindowTitle('Narwhallet - Create Reward')
        self.wallet_combo.show()
        self.ns_combo.show()
        self.amount_input.show()
        self.address_input.show()
        self.address_input.address.setReadOnly(True)
        self.address_combo.hide()
        self.address_select.setVisible(False)
        self.transaction_input.hide()
        self.namespace_key_input.show()
        self.namespace_key_input.key.setReadOnly(True)
        self.namespace_value_input.show()
        self.namespace_value_input.value.setReadOnly(True)
        self.bid_input.hide()
        self.auction_info.hide()

    def init_mode(self):
        if self.mode == 0:
            # Simple Send
            self._mode_simple_send()
        elif self.mode == 1:
            # Multi Sig Send
            self._mode_multi_sig_send()
        elif self.mode == 2:
            # Namespace Create
            self._mode_namespace_create()
        elif self.mode == 3:
            # Namespace Key Create
            self._mode_namespace_create_key()
        elif self.mode == 4:
            # Namespace Key Update
            self._mode_namespace_update_key()
        elif self.mode == 5:
            # Namespace Key Delete
            self._mode_namespace_delete_key()
        elif self.mode == 6:
            # Namespace Auction
            self._mode_create_auction()
        elif self.mode == 7:
            # Namespace Bid
            self._mode_create_bid()
        elif self.mode == 8:
            # Namespace Accept Bid
            self._mode_accept_bid()
        elif self.mode == 9:
            # Namespace Transfer
            self._mode_namespace_transfer()
        elif self.mode == 10:
            # Namespace Key Reward
            self._mode_namespace_reward()

    def set_availible_usxo(self, is_change: bool, isBidOp: bool, ns_address):
        # MShared.list_unspents(self.wallet, self.kex)
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []
        _nsusxo = None

        for tx in _tmp_usxo:
            # TODO Check for usxo's used by bids
            _tx = self.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], self.kex, True)

            if _tx is not None and isinstance(_tx, dict):
                _tx = self.cache.tx.add_from_json(_tx)

            # if self._test_tx(_tx) is False:
            #     continue

            if 'OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
                if isBidOp is False:
                    _used = False
                    for _vin in self.bid_tx.vin:
                        if _vin.txid == _tx.txid:
                            _used = True
                            print('used')

                    if _used is False:
                        _usxos.append(tx)
                else:
                    _usxos.append(tx)
            elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
                    and is_change is True and tx['a'] == ns_address):
                _nsusxo = tx

        if _nsusxo is not None and is_change is True and isBidOp is False:
            _usxos.insert(0, _nsusxo)

        if isBidOp is True:
            self.bid_tx.inputs_to_spend = _usxos
        else:
            self.new_tx.inputs_to_spend = _usxos

    def check_ns_key_input(self):
        if self.mode == 7:
            self.check_tx_is_auction()

        self.check_next()

    def check_tx_is_ns_key(self):
        _action_tx = self.namespace_key_input.key.text()

        if _action_tx[:4] in ('0001', '0002', '0003'):
            _action_tx = _action_tx[4:]

        _action_tx = MShared.check_tx_is_ns_key(_action_tx, self.kex, self.cache)

        if _action_tx[0] is True:
            self.address_input.address.setText(_action_tx[4])

    def check_tx_is_bid(self):
        _nft_tx = self.namespace_key_input.key.text()
        _nft_tx = MShared.check_tx_is_bid(_nft_tx, self.kex, self.cache)
        if _nft_tx[0] is True:
            _bid_psbt = keva_psbt(_nft_tx[2])
            _sh = (Scripts.AddressScriptHash
                   (self.auction_info.nft_address.text()))
            _sh = Scripts.compile(_sh, True)
            if _bid_psbt.tx.vout[1].scriptPubKey.hex == _sh:
                (self.amount_input.amount
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
            self.buttonBox.next.setEnabled(False)

    def check_tx_is_auction(self):
        _nft_tx = self.namespace_key_input.key.text()

        _nft_tx = MShared.check_tx_is_auction(_nft_tx, self.kex, self.cache)
        if _nft_tx[0] is True:
            self.auction_info.nft_name.setText(_nft_tx[2]['displayName'])
            self.auction_info.nft_desc.setText(_nft_tx[2]['desc'])
            if 'hashtags' in _nft_tx[1]:
                self.auction_info.nft_hashtags.setText(_nft_tx[1]['hashtags'])
            self.auction_info.nft_price.setText(_nft_tx[2]['price'])
            self.auction_info.nft_ns.setText(_nft_tx[1])
            self.auction_info.nft_address.setText(_nft_tx[2]['addr'])

    def build_bid(self):
        self.bid_tx.set_version(Ut.hex_to_bytes('00710000'))

        locale = QLocale()
        _b_amount = locale.toDouble(self.amount_input.amount.text())
        _bid_amount = int(_b_amount[0] * 100000000)

        _auc = {}
        _auc['displayName'] = self.auction_info.nft_name.text()
        _ns = self.auction_info.nft_ns.text()
        _ns_key = '\x01_KEVA_NS_'
        _ns_value = json.dumps(_auc, separators=(',', ':'))
        _trans_address = self.wallet.get_unused_address()
        _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                         _trans_address)
        _sh = Scripts.compile(_sh, True)
        _ = self.bid_tx.add_output(NS_RESERVATION, _trans_address)
        self.bid_tx.vout[0].scriptPubKey.set_hex(_sh)
        _ = self.bid_tx.add_output(_bid_amount,
                                   self.auction_info.nft_address.text())

        self.set_availible_usxo(False, True, self.ns_combo.combo.currentData())
        _inp_sel, _need_change, _est_fee = self.bid_tx.select_inputs(True)

        if _inp_sel is True:
            _, _, _fv = self.bid_tx.get_current_values(True)
            _cv = _fv - _est_fee

            if _need_change is True:
                _ = self.bid_tx.add_output(_cv, _trans_address)

            self.bid_tx.txb_preimage(self.wallet,
                                     SIGHASH_TYPE.ALL_ANYONECANPAY)

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def check_next(self):
        if self.mode in (0, 1):
            if self.wallet_combo.combo.currentText() != '-':
                if self.check_amount() and self.check_address():
                    self.buttonBox.next.setEnabled(True)
                else:
                    self.buttonBox.next.setEnabled(False)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 2:
            if self.wallet_combo.combo.currentText() != '-':
                if self.namespace_value_input.value.toPlainText() != '':
                    self.buttonBox.next.setEnabled(True)
                else:
                    self.buttonBox.next.setEnabled(False)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 3:
            if self.wallet_combo.combo.currentText() != '-':
                if (self.ns_combo.combo.currentText() != '' and
                        self.namespace_key_input.key.text() != '' and
                        self.namespace_value_input.value.toPlainText() != ''):
                    self.buttonBox.next.setEnabled(True)
                else:
                    self.buttonBox.next.setEnabled(False)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 4:
            if (self.wallet_combo.combo.currentText() != '-' and
                    self.ns_combo.combo.currentText() != '-' and
                    self.namespace_key_input.key.text() != '' and
                    self.namespace_value_input.value.toPlainText() != ''):
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 5:
            if self.wallet_combo.combo.currentText() != '-':
                if (self.wallet_combo.combo.currentText() != '-' and
                        self.ns_combo.combo.currentText() != '-' and
                        self.namespace_key_input.key.text() != ''):
                    self.buttonBox.next.setEnabled(True)
                else:
                    self.buttonBox.next.setEnabled(False)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 6:
            if (self.check_auction_amount() and
                    self.wallet_combo.combo.currentText() != '-' and
                    self.ns_combo.combo.currentText() != '-' and
                    self.auction_info.nft_name.text() != '' and
                    self.auction_info.nft_desc.text() != '' and
                    # self.nft_hashtags.text() != '' and
                    self.auction_info.nft_price.text() != ''):
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 7:
            if (self.wallet_combo.combo.currentText() != '-' and
                    self.ns_combo.combo.currentText() != '-' and
                    self.check_amount() and
                    self.auction_info.nft_ns.text() != '' and
                    self.auction_info.nft_price.text() != ''):
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 8:
            if (self.wallet_combo.combo.currentText() != '-' and
                    self.amount_input.amount.text() != '' and
                    self.auction_info.nft_ns.text() != '' and
                    self.auction_info.nft_price.text() != ''):
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 9:
            if self.wallet_combo.combo.currentText() != '-':
                if (self.check_address() and
                        self.ns_combo.combo.currentText() != '' and
                        self.namespace_key_input.key.text() != '' and
                        self.namespace_value_input.value.toPlainText() != ''):
                    self.buttonBox.next.setEnabled(True)
                else:
                    self.buttonBox.next.setEnabled(False)
            else:
                self.buttonBox.next.setEnabled(False)
        elif self.mode == 10:
            if (self.check_address() and self.check_amount() and
                    self.wallet_combo.combo.currentText() != '-' and
                    self.ns_combo.combo.currentText() != '-' and
                    self.namespace_key_input.key.text() != '' and
                    self.namespace_value_input.value.toPlainText() == ''):
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)

    def check_amount(self):
        return self._check_amount(self.amount_input.amount.text())

    def check_auction_amount(self):
        return self._check_amount(self.auction_info.nft_price.text())

    def _check_amount(self, amount):
        try:
            locale = QLocale()
            _result = locale.toDouble(amount)
            if _result[1] is True:
                _return = True
            else:
                _return = False
        except Exception:
            _return = False
        return _return

    def check_address(self):
        try:
            if self.address_input.address.isVisible():
                _ = (Base58Decoder
                     .CheckDecode(self.address_input.address.text()))
            else:
                _ = (Base58Decoder
                     .CheckDecode(self.address_combo.combo.currentData()))
            return True
        except Exception:
            return False

    def select_swap(self):
        self.address_input.address.setText('')
        self.address_combo.combo.setCurrentText('-')

        if self.address_input.address.isVisible():
            self.address_input.hide()
            self.address_combo.show()
            self.address_select.setText('Entry')
        else:
            self.address_input.show()
            self.address_combo.hide()
            self.address_select.setText('Book')

    def wallet_combo_changed(self, data):
        if data != '-':
            _n = self.wallet_combo.combo.currentData()
            self.wallet = self.wallets.get_wallet_by_name(_n)

            MShared.list_unspents(self.wallet, self.kex)
            self.set_namespace_combo()

        self.check_next()

    def ns_combo_changed(self, data):
        if data not in ('-', ''):
            if self.mode == 6:
                _ns = self.ns_combo.combo.currentText()
                _block = self.cache.ns.ns_block(_ns)[0]
                _b_s = str(_block[0])
                _block = str(str(len(_b_s)) + _b_s + str(_block[1]))
                _name = (self.cache.ns.get_namespace_by_key_value(
                             _ns, '\x01_KEVA_NS_'))

                if len(_name) == 0:
                    _name = (self.cache.ns
                             .get_namespace_by_key_value(_ns, '_KEVA_NS_'))

                if len(_name) > 0:
                    _name = _name[0][1]

                if 'displayName' in _name:
                    _name = json.loads(_name)['displayName']
                self.auction_info.nft_shortcode.setText(_block)
                self.auction_info.nft_name.setText(_name)
        else:
            if self.mode == 6:
                self.auction_info.nft_shortcode.setText('')
                self.auction_info.nft_name.setText('')
        self.check_next()

    def special_keys_combo_changed(self, data):
        if data not in ('-', ''):
            _data = self.special_keys_combo.combo.currentData()
            self.namespace_key_input.key.setText(_data)
            self.namespace_key_input.key.setReadOnly(True)
        else:
            self.namespace_key_input.key.setReadOnly(False)

    def set_namespace_combo(self):
        self.ns_combo.combo.clear()
        self.ns_combo.combo.addItem('-', '-')

        _tmp_usxo = self.wallet.get_usxos()

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

                    self.ns_combo.combo.addItem(_ns, tx['a'])

    def reset_transactions(self):
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []
        self.bid_tx.set_vin([])
        self.bid_tx.set_vout([])
        self.bid_tx.input_signatures = []

    def set_ready(self, _stx, _est_fee):
        self.send_info.fee.setText(str(_est_fee/100000000))
        self.send_info.txsize.setText(str(len(_stx)))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.send_info.tx.setPlainText(self.raw_tx)
        self.wallet_combo.combo.setEnabled(False)
        # self.value.setFrame(False)
        # self.value.setReadOnly(True)
        # self.address.setReadOnly(True)
        # self.address.setFrame(False)
        self.buttonBox.next.setVisible(False)
        self.buttonBox.back.setVisible(True)
        self.buttonBox.send.setEnabled(True)

    def set_output(self):
        _locale = QLocale()

        if self.address_input.address.isVisible():
            if self.mode != 10:
                _address = self.address_input.address.text()
            else:
                _reward_address = self.address_input.address.text()
        elif self.address_combo.combo.isVisible():
            _address = self.address_combo.combo.currentData()

        if self.ns_combo.combo.isVisible():
            _ns = self.ns_combo.combo.currentText()
            _ns_address = self.ns_combo.combo.currentData()
            _ns_key = self.namespace_key_input.key.text()
            _ns_value = self.namespace_value_input.value.toPlainText()

        _sh = ''

        if self.mode == 0:
            # Simple Send
            _result = _locale.toDouble(self.amount_input.amount.text())
            _amount = int(_result[0] * 100000000)
        elif self.mode == 1:
            # Multi Sig Send
            pass
        elif self.mode == 2:
            # Namespace Create
            _address = self.wallet.get_unused_address()
            self.address_input.address.setText(_address)
            _amount = NS_RESERVATION
            _temp_ns = self.tx_to_ns(TEMP_TX, 0)
            _ns_value = self.namespace_value_input.value.toPlainText()
            _sh = Scripts.KevaNamespaceCreation(_temp_ns, _ns_value,
                                                _address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode in (3, 4):
            # Namespace Key Create, Update
            _amount = NS_RESERVATION
            _address = _ns_address
            _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key,
                                             _ns_value, _ns_address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode == 5:
            # Namespace Key Delete
            _amount = NS_RESERVATION
            _address = _ns_address
            _sh = Scripts.KevaKeyValueDelete(_ns, _ns_key,
                                             _ns_address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode == 6:
            # Namespace Auction
            _amount = NS_RESERVATION
            _address = _ns_address
            _auc = {}
            _auc['displayName'] = self.auction_info.nft_name.text()
            _auc['price'] = str(self.auction_info.nft_price.text())
            _auc['desc'] = self.auction_info.nft_desc.text()

            _tags = {}
            _hashtags = self.auction_info.nft_hashtags.text().split(' ')
            for tag in _hashtags:
                tag = tag.split(',')
                for t in tag:
                    t = t.replace('#', '').strip()
                    if t != '':
                        _tags['#' + t] = ''
            _tags = list(_tags.keys())
            if len(_tags) > 0:
                _auc['hashtags'] = _tags
            _payment_addr = self.wallet.get_unused_change_address()
            self.auction_info.nft_address.setText(_payment_addr)
            _auc['addr'] = _payment_addr
            _ns_value = json.dumps(_auc, separators=(',', ':'))

            _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                             _ns_address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode == 7:
            # Namespace Bid
            _amount = NS_RESERVATION
            _address = _ns_address
            self.build_bid()

            _ns_key = (Ut.hex_to_bytes('0001') + Ut.hex_to_bytes(_ns_key))
            _ns_value = self.bid_tx.to_psbt()
            _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                             _ns_address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode == 8:
            # Namespace Accept Bid
            # self.check_tx_is_bid()
            pass
        elif self.mode == 9:
            # Namespace Transfer
            _amount = NS_RESERVATION
            _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key,
                                             _ns_value, _address)
            _sh = Scripts.compile(_sh, True)
        elif self.mode == 10:
            # Namespace Key Reward
            _amount = NS_RESERVATION
            _address = _ns_address
            _result = _locale.toDouble(self.amount_input.amount.text())
            _reward_value = int(_result[0] * 100000000)
            _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                             _ns_address)
            _sh = Scripts.compile(_sh, True)

        if self.mode != 8:
            _ = self.new_tx.add_output(_amount, _address)

        if _sh != '':
            self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

        if self.action == 'reward':
            _ = self.new_tx.add_output(_reward_value, _reward_address)

    def build_send(self):
        if self.mode not in (0, 1):
            self.new_tx.set_version(Ut.hex_to_bytes('00710000'))

        self.set_output()
        if self.mode in (0, 1, 2):
            self.set_availible_usxo(False, False, '')
            _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        elif self.mode in (3, 4, 5, 6, 7, 9, 10):
            _ns_address = self.ns_combo.combo.currentData()
            self.set_availible_usxo(True, False, _ns_address)
            _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        else:
            _ns_address = self.ns_combo.combo.currentData()
            self.set_availible_usxo(True, False, _ns_address)
            if len(self.new_tx.inputs_to_spend) == 0:
                _inp_sel = False
            else:
                tx = self.new_tx.inputs_to_spend[0]
                self.new_tx.add_input(tx['value'],
                                      str(tx['a_idx'])+':'+str(tx['ch']),
                                      tx['tx_hash'], tx['tx_pos'])
                _inp_sel = True
                _need_change = False

        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            if _need_change is True:
                _cv = _fv - _est_fee

            if self.mode == 2:
                _ns = self.tx_to_ns(self.new_tx.vin[0].txid,
                                    self.new_tx.vin[0].vout)
                _ns_value = self.namespace_value_input.value.toPlainText()
                _n_sh = (Scripts.KevaNamespaceCreation
                         (_ns, _ns_value, self.address_input.address.text()))
                _n_sh = Scripts.compile(_n_sh, True)
                self.new_tx.vout[0].scriptPubKey.set_hex(_n_sh)

            if _need_change is True:
                if self.mode in (0, 1, 2, 9):
                    _change_address = self.wallet.get_unused_change_address()
                    _ = self.new_tx.add_output(_cv, _change_address)
                else:
                    # _ns_dat = self.ns_combo.combo.currentData().split(':')
                    _ns_address = self.ns_combo.combo.currentData()
                    _ = self.new_tx.add_output(_cv, _ns_address)

            if self.mode == 8:
                self.new_tx.txb_preimage(self.wallet,
                                         SIGHASH_TYPE.ALL_ANYONECANPAY, True)
                _, _, _est_fee = self.new_tx.get_current_values(False)
            else:
                self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)

            _stx = self.new_tx.serialize_tx()
            self.set_ready(_stx, _est_fee)
        else:
            self.reset_transactions()

    def back_click(self):
        self.buttonBox.next.setVisible(True)
        self.buttonBox.back.setVisible(False)
        self.buttonBox.send.setEnabled(False)
        self.amount_input.amount.setFrame(True)
        self.address_input.address.setFrame(True)
        self.send_info.fee.setText('')
        self.send_info.txsize.setText('')

        self.send_info.tx.setPlainText(self.raw_tx)
        self.reset_transactions()
        self.wallet_combo.combo.setEnabled(True)
        self.amount_input.amount.setReadOnly(False)
        self.address_input.address.setReadOnly(False)
