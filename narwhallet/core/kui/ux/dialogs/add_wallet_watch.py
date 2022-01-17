from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QDialogButtonBox)
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_add_wallet_watch_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.name = HLSection('Name:', QLineEdit(self))
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('add_wallet_watch_dlg')
        self.resize(430, 225)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.name)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.name.widgets[0].textChanged.connect(self._test_name)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('add_wallet_watch_dlg',
                                       'Narwhallet - Watch Only Wallet'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _test_name(self):
        _b_ok = QDialogButtonBox.Ok

        if self.name.widgets[0].text() != '':
            self.buttonBox.button(_b_ok).setEnabled(True)
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)
