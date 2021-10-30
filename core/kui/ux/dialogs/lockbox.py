import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)


class Ui_lockbox_dlg(QObject):
    def setupUi(self, lockbox_dialog: QDialog, mode: int):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        _b_cancel = QDialogButtonBox.Cancel
        _al_center = QtCore.Qt.AlignCenter

        self.mode = mode
        self.verticalLayout = QVBoxLayout(lockbox_dialog)
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_1 = QLabel(lockbox_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.label_2 = QLabel(lockbox_dialog)
        self.lineEdit = QLineEdit(lockbox_dialog)
        if self.mode == 1:
            self.label_3 = QLabel(lockbox_dialog)
            self.lineEdit1 = QLineEdit(lockbox_dialog)
        self.buttonBox = QDialogButtonBox(lockbox_dialog)

        lockbox_dialog.setObjectName('lb_dlg')
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        if self.mode == 1:
            self.lineEdit1.setEchoMode(QLineEdit.Password)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_cancel | _b_ok)

        self.horizontalLayout_1.addWidget(self.label_1)
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

        self.retranslateUi(lockbox_dialog)
        self.buttonBox.accepted.connect(lockbox_dialog.accept)
        self.buttonBox.rejected.connect(lockbox_dialog.reject)

        if self.mode == 1:
            self.lineEdit.textChanged.connect(self._test_password_match)
            self.lineEdit1.textChanged.connect(self._test_password_match)

    def retranslateUi(self, lockbox_dialog: QDialog):
        _translate = QtCore.QCoreApplication.translate
        lockbox_dialog.setWindowTitle(_translate('lb_dlg', 'Narwhallet'))
        self.label_2.setText(_translate('lb_dlg', 'Password:'))
        if self.mode == 1:
            self.label_3.setText(_translate('lb_dlg', 'Confirm:'))

    def ret(self):
        return self.lineEdit.text()

    def _test_password_match(self):
        _b_ok = QDialogButtonBox.Ok

        if self.lineEdit.text() != self.lineEdit1.text():
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)
