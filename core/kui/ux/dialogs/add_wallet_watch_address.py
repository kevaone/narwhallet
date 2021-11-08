import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)

from core.kcl.bip_utils.base58 import Base58Decoder


class Ui_add_watch_addr_dlg(QObject):
    def setupUi(self, add_wallet_watch_address_dialog: QDialog):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _al_center = QtCore.Qt.AlignCenter

        self.verticalLayout = QVBoxLayout(add_wallet_watch_address_dialog)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_1 = QLabel(add_wallet_watch_address_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.label_hl = QHBoxLayout()
        self.label_label = QLabel(add_wallet_watch_address_dialog)
        self.label_d = QLineEdit(add_wallet_watch_address_dialog)
        self.address_hl = QHBoxLayout()
        self.address_label = QLabel(add_wallet_watch_address_dialog)
        self.address_d = QLineEdit(add_wallet_watch_address_dialog)
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(add_wallet_watch_address_dialog)

        add_wallet_watch_address_dialog.setObjectName('a_watch_add_dlg')
        add_wallet_watch_address_dialog.resize(430, 225)
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.horizontalLayout_1.addWidget(self.label_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.label_hl.addWidget(self.label_label)
        self.label_hl.addWidget(self.label_d)
        self.verticalLayout.addLayout(self.label_hl)
        self.address_hl.addWidget(self.address_label)
        self.address_hl.addWidget(self.address_d)
        self.verticalLayout.addLayout(self.address_hl)

        self.horizontalLayout.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(add_wallet_watch_address_dialog)
        self.address_d.textChanged.connect(self._set_address)
        self.buttonBox.accepted.connect(add_wallet_watch_address_dialog.accept)
        self.buttonBox.rejected.connect(add_wallet_watch_address_dialog.reject)

    def retranslateUi(self, addr_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        addr_dlg.setWindowTitle(_translate('a_watch_add_dlg',
                                           'Narwhallet - Address'))
        self.label_label.setText(_translate('a_watch_add_dlg', 'Label:'))
        self.address_label.setText(_translate('a_watch_add_dlg', 'Address:'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _set_address(self):
        try:
            _ = Base58Decoder.CheckDecode(self.address_d.text())
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        except Exception:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
