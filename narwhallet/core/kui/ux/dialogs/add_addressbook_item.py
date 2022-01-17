from PyQt5 import QtCore
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QComboBox)
from PyQt5.QtWidgets import QDialog
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kcl.addr_book import MBookAddress
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_add_ab_item_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.coin = HLSection('Coin:', QComboBox(self))
        self.name = HLSection('Name:', QLineEdit(self))
        self.label = HLSection('Label:', QLineEdit(self))
        self.address = HLSection('Address:', QLineEdit(self))
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('add_addrbook')
        self.setMinimumSize(QtCore.QSize(425, 225))

        self.coin.widgets[0].addItem('Kevacoin', 'KEVACOIN')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.name)
        self.verticalLayout.addLayout(self.address)
        self.verticalLayout.addLayout(self.label)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        self._init_wallet()
        self.coin.widgets[0].currentTextChanged.connect(self._set_coin)
        self.name.widgets[0].textChanged.connect(self._set_name)
        self.label.widgets[0].textChanged.connect(self._set_label)
        self.address.widgets[0].textChanged.connect(self._set_address)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        (self.setWindowTitle(_translate('add_addrbook',
         'Narwhallet - Add to Address Book')))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._a = MBookAddress()

    def ret_address(self):
        self._a.set_coin(self.coin.widgets[0].currentText().upper())
        return self._a

    def _set_coin(self):
        self._a.set_coin(self.coin.widgets[0].currentText().upper())

    def _set_name(self):
        self._a.set_name(self.name.widgets[0].text())

    def _set_address(self):
        _b_ok = QDialogButtonBox.Ok

        try:
            _ = Base58Decoder.CheckDecode(self.address.widgets[0].text())
            self._a.set_address(self.address.widgets[0].text())
            self.buttonBox.button(_b_ok).setEnabled(True)
        except Exception:
            self._a.set_address(None)
            self.buttonBox.button(_b_ok).setEnabled(False)

    def _set_label(self):
        self._a.set_label(self.label.widgets[0].text())
