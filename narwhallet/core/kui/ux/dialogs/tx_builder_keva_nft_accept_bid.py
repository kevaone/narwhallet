from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy)

from narwhallet.control.shared import MShared
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.models.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallet import MWallet
from narwhallet.core.kcl.models.transaction_builder import MTransactionBuilder
from narwhallet.core.kcl.models.psbt_decoder import keva_psbt
from narwhallet.core.kui.ux.widgets.generator import UShared
from narwhallet.core.kui.ux.widgets.wallet_combobox import WalletComboBox
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame
from narwhallet.core.kui.ux.widgets.auction_info_frame import AuctionInfoFrame
from narwhallet.core.kui.ux.widgets.dialog_buttonbox import DialogButtonBox


class Ui_keva_op_nft_accept_bid_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.wallet: MWallet = None
        self.cache: MCache = None
        self.kex = None
        self.new_tx = MTransactionBuilder()
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
        self.hl_10 = QHBoxLayout()

        self.combo_wallet = WalletComboBox()

        self.bid_nft_tx_l = QLabel(self)
        self.bid_nft_tx = QLineEdit(self)
        self.bid_amount_l = QLabel(self)
        self.bid_amount = QLabel(self)
        self.auction_info = AuctionInfoFrame()
        self.send_info = SendInfoFrame()
        self.buttonBox = DialogButtonBox(self)

        self.setObjectName('keva_op_nft_accept_dlg')
        self.setMinimumSize(QtCore.QSize(475, 350))
        self.bid_nft_tx.setReadOnly(True)

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.combo_wallet)
        self.hl_1.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.hl_1)

        self.hl_2.addWidget(self.bid_nft_tx_l)
        self.hl_2.addWidget(self.bid_nft_tx)
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
        self.buttonBox.cancel.clicked.connect(self.reject)
        self.buttonBox.next.clicked.connect(self.txb_build_simple_send)
        self.buttonBox.back.clicked.connect(self.back_click)

        self.bid_nft_tx.textChanged.connect(self.check_tx_is_bid)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('keva_op_nft_accept_dlg',
                                       'Narwhallet - Create Namespace'))
        (self.bid_nft_tx_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Bid on TX: ')))
        (self.bid_amount_l
         .setText(_translate('keva_op_nft_accept_dlg', 'Bid Amount: ')))

    def check_next(self):
        if (self.combo_wallet.combo.currentText() != '-' and
                self.bid_amount.text() != '' and
                self.auction_info.nft_ns.text() != '' and
                self.auction_info.nft_price.text() != ''):
            self.buttonBox.next.setEnabled(True)
        else:
            self.buttonBox.next.setEnabled(False)

    def check_tx_is_bid(self):
        _nft_tx = self.bid_nft_tx.text()
        _nft_tx = MShared.check_tx_is_bid(_nft_tx, self.kex, self.cache)
        if _nft_tx[0] is True:
            _bid_psbt = keva_psbt(_nft_tx[2])
            _sh = Scripts.P2SHAddressScriptHash(self.auction_info.nft_address.text())
            _sh = Scripts.compile(_sh, True)
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
            self.buttonBox.next.setEnabled(False)

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

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def txb_build_simple_send(self):
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_availible_usxo(self.wallet, False, False, self.auction_info.nft_ns.text(), self.cache, self.kex)

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
            self.send_info.fee.setText(str(_fv/100000000))
            self.send_info.txsize.setText(str(len(_stx)))
            self.raw_tx = Ut.bytes_to_hex(_stx)
            self.send_info.tx.setPlainText(self.raw_tx)

            self.bid_nft_tx.setReadOnly(True)
            self.buttonBox.next.setVisible(False)
            self.buttonBox.back.setVisible(True)
            self.buttonBox.send.setEnabled(True)
        else:
            self.new_tx.set_vin([])
            self.new_tx.set_vout([])
            self.new_tx.input_signatures = []

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
        self.send_info.tx.setPlainText(self.raw_tx)
        self.bid_nft_tx.setReadOnly(False)
