from PyQt5 import QtCore
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QDialog)
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_lockbox_dlg(QDialog):
    def setupUi(self, mode: int):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.mode = mode
        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.lineEdit = QLineEdit(self)
        if self.mode == 1:
            self.label_3 = QLabel(self)
            self.lineEdit1 = QLineEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('lb_dlg')
        self.lineEdit.setEchoMode(QLineEdit.Password)
        if self.mode == 1:
            self.lineEdit1.setEchoMode(QLineEdit.Password)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        if self.mode == 1:
            self.horizontalLayout_3.addWidget(self.label_3)
            self.horizontalLayout_3.addWidget(self.lineEdit1)
            self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        if self.mode == 1:
            self.lineEdit.textChanged.connect(self._test_password_match)
            self.lineEdit1.textChanged.connect(self._test_password_match)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('lb_dlg', 'Narwhallet'))
        self.label_2.setText(_translate('lb_dlg', 'Password:'))
        if self.mode == 1:
            self.label_3.setText(_translate('lb_dlg', 'Confirm:'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def ret(self):
        return self.lineEdit.text()

    def _test_password_match(self):
        _b_ok = QDialogButtonBox.Ok

        if self.lineEdit.text() != self.lineEdit1.text():
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)
