from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)
from PyQt5.QtWidgets import QDialog

from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder
from narwhallet.core.kui.ux.widgets.coin_dropdown import _coin_dropdown
from narwhallet.core.kcl.models.book_address import MBookAddress
from narwhallet.control.shared import MShared


class Ui_add_ab_item_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _al_center = QtCore.Qt.AlignCenter

        self.verticalLayout = QVBoxLayout(self)
        self.label_1 = QLabel(self)
        _pic = QtGui.QPixmap(MShared.get_resource_path('narwhal.png'))
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.comboBox = _coin_dropdown(self)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.lineEdit = QLineEdit(self)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_4 = QLabel(self)
        self.lineEdit_3 = QLineEdit(self)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_3 = QLabel(self)
        self.lineEdit_2 = QLineEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('add_addrbook')
        self.setMinimumSize(QtCore.QSize(425, 225))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.label.setVisible(False)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.verticalLayout.addWidget(self.label_1)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addWidget(self.label_4)
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        self._init_wallet()
        self.comboBox.currentTextChanged.connect(self._set_coin)
        self.lineEdit.textChanged.connect(self._set_name)
        self.lineEdit_2.textChanged.connect(self._set_label)
        self.lineEdit_3.textChanged.connect(self._set_address)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        (self.setWindowTitle(_translate('add_addrbook',
         'Narwhallet - Add to Address Book')))
        self.label.setText(_translate('add_addrbook', 'Coin:'))
        self.label_2.setText(_translate('add_addrbook', 'Name:'))
        self.label_3.setText(_translate('add_addrbook', 'Label:'))
        self.label_4.setText(_translate('add_addrbook', 'Address:'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._a = MBookAddress()

    def ret_address(self):
        self._a.set_coin(self.comboBox.currentText().upper())
        return self._a

    def _set_coin(self):
        self._a.set_coin(self.comboBox.currentText().upper())

    def _set_name(self):
        self._a.set_name(self.lineEdit.text())

    def _set_address(self):
        _b_ok = QDialogButtonBox.Ok

        try:
            _ = Base58Decoder.CheckDecode(self.lineEdit_3.text())
            self._a.set_address(self.lineEdit_3.text())
            self.buttonBox.button(_b_ok).setEnabled(True)
        except Exception:
            self._a.set_address(None)
            self.buttonBox.button(_b_ok).setEnabled(False)

    def _set_label(self):
        self._a.set_label(self.lineEdit_2.text())
