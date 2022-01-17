from PyQt5 import QtCore
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QDialogButtonBox)
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_lockbox_dlg(QDialog):
    def setupUi(self, mode: int):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.mode = mode
        self.verticalLayout = QVBoxLayout(self)
        self.npass = HLSection('Password:', QLineEdit(self))
        self.npass.widgets[0].setEchoMode(QLineEdit.Password)
        if self.mode == 1:
            self.npass_confirm = HLSection('Confirm:', QLineEdit(self))
            self.npass_confirm.widgets[0].setEchoMode(QLineEdit.Password)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('lb_dlg')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.npass)
        if self.mode == 1:
            self.verticalLayout.addLayout(self.npass_confirm)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        if self.mode == 1:
            (self.npass.widgets[0]
             .textChanged.connect(self._test_password_match))
            (self.npass_confirm.widgets[0]
             .textChanged.connect(self._test_password_match))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('lb_dlg', 'Narwhallet'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def ret(self):
        return self.npass.widgets[0].text()

    def _test_password_match(self):
        _b_ok = QDialogButtonBox.Ok

        if (self.npass.widgets[0].text() !=
                self.npass_confirm.widgets[0].text()):
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)
