from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_add_watch_addr_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_hl = QHBoxLayout()
        self.label_label = QLabel(self)
        self.label_d = QLineEdit(self)
        self.address_hl = QHBoxLayout()
        self.address_label = QLabel(self)
        self.address_d = QLineEdit(self)
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('a_watch_add_dlg')
        self.resize(430, 225)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
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

        self.retranslateUi()
        self.address_d.textChanged.connect(self._set_address)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('a_watch_add_dlg',
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
