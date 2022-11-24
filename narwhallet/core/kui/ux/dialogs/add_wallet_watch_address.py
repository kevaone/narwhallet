from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QComboBox, QLineEdit)
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_add_watch_addr_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.coin = HLSection('Coin:', QComboBox(self))
        self.label = HLSection('Label:', QLineEdit(self))
        self.address = HLSection('Address:', QLineEdit(self))
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('a_watch_add_dlg')
        self.resize(430, 225)
        self.coin.widgets[0].addItem('Kevacoin', 'KEVACOIN')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.label)
        self.verticalLayout.addLayout(self.address)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.address.widgets[0].textChanged.connect(self._set_address)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('a_watch_add_dlg',
                                       'Narwhallet - Address'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _set_address(self):
        try:
            _ = Base58Decoder.CheckDecode(self.address.widgets[0].text())
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        except Exception:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
