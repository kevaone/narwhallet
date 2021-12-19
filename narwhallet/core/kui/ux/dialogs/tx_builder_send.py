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
from narwhallet.core.kui.ux.widgets.amount_input import AmountInput
from narwhallet.core.kui.ux.widgets.address_input import AddressInput
from narwhallet.core.kui.ux.widgets.address_combobox import AddressComboBox
from narwhallet.core.kui.ux.widgets.namespace_combobox import NamespaceComboBox
from narwhallet.core.kui.ux.widgets.namespace_key_input import NamespaceKeyInput
from narwhallet.core.kui.ux.widgets.namespace_value_input import NamespaceValueInput
from narwhallet.core.kui.ux.widgets.transaction_input import TransactionInput
from narwhallet.core.kui.ux.widgets.send_info_frame import SendInfoFrame
from narwhallet.core.kui.ux.widgets.auction_info_frame import AuctionInfoFrame
from narwhallet.core.kui.ux.widgets.dialog_buttonbox import DialogButtonBox
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_send_dlg(QDialog):
    def setupUi(self, mode):
        self.mode: int = mode
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.wallet_combo = WalletComboBox()
        self.ns_combo = NamespaceComboBox()
        self.amount_input = AmountInput()
        self.address_input = AddressInput()
        self.address_combo = AddressComboBox()
        self.transaction_input = TransactionInput()
        self.namespace_key_input = NamespaceKeyInput()
        self.namespace_value_input = NamespaceValueInput()
        self.bid_input = AmountInput()
        self.auction_info = AuctionInfoFrame()
        self.send_info = SendInfoFrame()
        self.buttonBox = DialogButtonBox(self)

        self.address_select = QPushButton(self)

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.wallet_combo)
        self.verticalLayout.addLayout(self.ns_combo)
        self.verticalLayout.addLayout(self.amount_input)
        self.verticalLayout.addLayout(self.address_input)
        self.verticalLayout.addLayout(self.address_combo)
        self.verticalLayout.addWidget(self.address_select)
        self.verticalLayout.addLayout(self.transaction_input)
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
        # self.buttonBox.next.clicked.connect(self.txb_build_simple_send)
        self.buttonBox.back.clicked.connect(self.back_click)
        self.amount_input.amount.textChanged.connect(self.check_next)
        self.address_input.address.textChanged.connect(self.check_next)
        self.address_combo.combo.currentTextChanged.connect(self.check_next)
        self.address_select.clicked.connect(self.select_swap)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('send_dlg', 'Narwhallet - Send'))
        self.address_select.setText(_translate('send_dlg', 'Book'))

    def init_mode(self):
        if self.mode == 0:
            # Simple Send
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
        elif self.mode == 1:
            # Multi Sig Send
            pass
        elif self.mode == 2:
            # Namespace Create
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
        elif self.mode == 3:
            # Namespace Key Create / Edit
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
        elif self.mode == 4:
            # Namespace Key Delete
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
        elif self.mode == 5:
            # Namespace Auction
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
        elif self.mode == 6:
            # Namespace Bid
            self.wallet_combo.show()
            self.ns_combo.show()
            self.amount_input.hide()
            self.address_input.hide()
            self.address_combo.hide()
            self.address_select.setVisible(False)
            self.transaction_input.show()
            self.namespace_key_input.hide()
            self.namespace_value_input.hide()
            self.bid_input.show()
            self.auction_info.show()
        elif self.mode == 7:
            # Namespace Accept Bid
            self.wallet_combo.show()
            self.ns_combo.show()
            self.amount_input.hide()
            self.address_input.hide()
            self.address_combo.hide()
            self.address_select.setVisible(False)
            self.transaction_input.show()
            self.namespace_key_input.hide()
            self.namespace_value_input.hide()
            self.bid_input.show()
            self.auction_info.show()
        elif self.mode == 8:
            # Namespace Transfer
            self.wallet_combo.show()
            self.ns_combo.show()
            self.amount_input.hide()
            self.address_input.show()
            self.address_combo.hide()
            self.transaction_input.hide()
            self.namespace_key_input.hide()
            self.namespace_value_input.hide()
            self.bid_input.hide()
            self.auction_info.hide()

    def check_next(self):
        if self.wallet_combo.combo.currentText() != '-':
            if self.check_amount() and self.check_address():
                self.buttonBox.next.setEnabled(True)
            else:
                self.buttonBox.next.setEnabled(False)
        else:
            self.buttonBox.next.setEnabled(False)

    def check_amount(self):
        try:
            locale = QLocale()
            _result = locale.toDouble(self.amount_input.amount.text())
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
                _ = Base58Decoder.CheckDecode(self.address_input.address.text())
            else:
                _ = Base58Decoder.CheckDecode(self.address_combo.combo.currentData())
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


    def back_click(self):
        self.buttonBox.next.setVisible(True)
        self.buttonBox.back.setVisible(False)
        self.buttonBox.send.setEnabled(False)
        self.amount_input.amount.setFrame(True)
        self.address_input.address.setFrame(True)
        self.send_info.fee.setText('')
        self.send_info.txsize.setText('')
        self.raw_tx = ''
        # self.new_tx.set_vin([])
        # self.new_tx.set_vout([])
        # self.new_tx.input_signatures = []
        self.send_info.tx.setPlainText(self.raw_tx)
        self.wallet_combo.combo.setEnabled(True)
        self.amount_input.amount.setReadOnly(False)
        self.address_input.address.setReadOnly(False)
