import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)


class Ui_add_wallet_watch_dlg(QObject):
    def setupUi(self, add_wallet_watch_dialog: QDialog):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _al_center = QtCore.Qt.AlignCenter

        self.verticalLayout = QVBoxLayout(add_wallet_watch_dialog)
        self.horizontalLayout_1 = QHBoxLayout()
        self.label_1 = QLabel(add_wallet_watch_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.name_hl = QHBoxLayout()
        self.name_label = QLabel(add_wallet_watch_dialog)
        self.name_d = QLineEdit(add_wallet_watch_dialog)
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(add_wallet_watch_dialog)

        add_wallet_watch_dialog.setObjectName('add_wallet_watch_dlg')
        add_wallet_watch_dialog.resize(430, 225)
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.horizontalLayout_1.addWidget(self.label_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.name_hl.addWidget(self.name_label)
        self.name_hl.addWidget(self.name_d)
        self.verticalLayout.addLayout(self.name_hl)

        self.horizontalLayout.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(add_wallet_watch_dialog)
        self.name_d.textChanged.connect(self._test_name)
        self.buttonBox.accepted.connect(add_wallet_watch_dialog.accept)
        self.buttonBox.rejected.connect(add_wallet_watch_dialog.reject)

    def retranslateUi(self, addr_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        addr_dlg.setWindowTitle(_translate('add_wallet_watch_dlg',
                                           'Narwhallet - Watch Only Wallet'))
        self.name_label.setText(_translate('add_wallet_watch_dlg', 'Name:'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _test_name(self):
        _b_ok = QDialogButtonBox.Ok

        if self.name_d.text() != '':
            self.buttonBox.button(_b_ok).setEnabled(True)
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)
