from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QComboBox, QPlainTextEdit,
                             QPushButton, QHBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QDialogButtonBox, QFrame, QDialog)
from narwhallet.core.kui.ux.widgets.coin_dropdown import _coin_dropdown
from narwhallet.core.kcl.models.wallet import MWallet
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_create_wallet_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        # _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout_0 = QHBoxLayout()
        # self.label_1 = QLabel(self)
        # _pic = QPixmap(MShared.get_resource_path('narwhal.png'))
        self.label_4 = QLabel(self)
        self.lineEdit_2 = QLineEdit(self)
        self.horizontalLayout = QHBoxLayout()
        self.label_5 = QLabel(self)
        self.comboBox1 = QComboBox(self)
        self.label = QLabel(self)
        self.comboBox = _coin_dropdown(self)
        self.label_6 = QLabel(self)
        self.lineEdit_1 = QLineEdit(self)
        self.horizontalLayout_2 = QHBoxLayout()
        self.pushButton = QPushButton(self)
        self.plainTextEdit = QPlainTextEdit(self)
        self.horizontalLayout_3 = QHBoxLayout()
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.adv_hl = QHBoxLayout()
        self.adv_label = QLabel(self)
        self.adv_label_p = QPushButton(self)
        self.adv_f = QFrame(self)
        self.adv_f_vl = QVBoxLayout(self.adv_f)
        self.label_2 = QLabel(self)
        self.lineEdit = QLineEdit(self)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_7 = QLabel(self)
        self.lineEdit1 = QLineEdit(self)
        self.buttonBox = QDialogButtonBox(self)
        self.label_3 = QLabel(self)

        self.setObjectName('create_dlg')
        self.resize(400, 475)
        # self.label_1.setAlignment(_al_center)
        # self.label_1.setContentsMargins(0, 0, 0, 0)
        # self.label_1.setPixmap(_pic)
        self.label_5.setVisible(False)
        self.comboBox1.addItem('-')
        # self.comboBox1.addItem('bip44')
        self.comboBox1.addItem('bip49')
        self.comboBox1.setCurrentText('bip49')
        self.comboBox1.setVisible(False)
        self.label.setVisible(False)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self.label_6.setVisible(False)
        self.lineEdit_1.setText('1')
        self.lineEdit_1.setVisible(False)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.adv_label_p.setIcon(QIcon(self._ppic))
        self.adv_label_p.setFlat(True)
        self.adv_label_p.setVisible(False)
        self.adv_label.setVisible(False)
        self.adv_f.setVisible(False)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.lineEdit1.setEchoMode(QLineEdit.Password)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout_0.addWidget(self.label_4)
        self.horizontalLayout_0.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_0)
        self.horizontalLayout.addWidget(self.label_5)
        self.horizontalLayout.addWidget(self.comboBox1)
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.comboBox)
        self.horizontalLayout.addWidget(self.label_6)
        self.horizontalLayout.addWidget(self.lineEdit_1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.adv_hl.addWidget(self.adv_label)
        self.adv_hl.addWidget(self.adv_label_p)
        self.adv_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.adv_hl)
        self.horizontalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.adv_f_vl.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addWidget(self.label_7)
        self.horizontalLayout_4.addWidget(self.lineEdit1)
        self.adv_f_vl.addLayout(self.horizontalLayout_4)
        self.adv_f_vl.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.adv_f)
        self.verticalLayout.addWidget(self.buttonBox)

        self._init_wallet()
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.pushButton.clicked.connect(self._generate_mnemonic)
        self.lineEdit_2.textChanged.connect(self._set_name)
        self.plainTextEdit.textChanged.connect(self._mnemonic_changed)
        self.lineEdit.textChanged.connect(self._test_password_match)
        self.lineEdit1.textChanged.connect(self._test_password_match)
        self.comboBox.currentTextChanged.connect(self._set_coin)
        self.comboBox1.currentTextChanged.connect(self.set_wallet_type)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.adv_label_p.clicked.connect(self._display_advanced)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('create_dlg',
                                       'Narwhallet - Create Wallet'))
        self.label_4.setText(_translate('create_dlg', 'Name:'))
        self.label_6.setText(_translate('create_dlg', 'PreGen Addresses:'))
        self.label.setText(_translate('create_dlg', 'Coin:'))
        self.label_5.setText(_translate('create_dlg', 'Type:'))
        self.label_2.setText(_translate('create_dlg', '*Password:'))
        self.label_7.setText(_translate('create_dlg', 'Confirm:'))
        self.pushButton.setText(_translate('create_dlg', 'Generate Mnemonic'))
        self.adv_label.setText(_translate('create_dlg', 'Advanced'))
        self.label_3.setText(_translate('create_dlg',
                                        '* = Optional Mnemonic Seed Password'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._w = MWallet()

    def _display_advanced(self, _event):
        if self.adv_f.isVisible() is True:
            self.adv_f.setVisible(False)
            self.adv_label_p.setIcon(QIcon(self._ppic))
        else:
            self.adv_f.setVisible(True)
            self.adv_label_p.setIcon(QIcon(self._mpic))

    def ret_wallet(self) -> MWallet:
        self._w.set_bip('bip49')
        self._w.set_coin(self.comboBox.currentText().upper())

        if (self._w.mnemonic is None
           and self.plainTextEdit.toPlainText() != ''):

            _m = self.plainTextEdit.toPlainText().replace('\n', ' ')
            self._w.set_mnemonic(_m)

        self._w.generate_seed(self.lineEdit.text())
        return self._w

    def _test_password_match(self):
        _b_ok = QDialogButtonBox.Ok

        if self.lineEdit.text() != self.lineEdit1.text():
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)

    def _generate_mnemonic(self):
        self._w.generate_mnemonic()
        self.plainTextEdit.setPlainText(self._w.mnemonic)

    def _mnemonic_changed(self):
        _b_ok = QDialogButtonBox.Ok

        if len(self.plainTextEdit.toPlainText().strip().split(' ')) != 24:
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()

    def _set_coin(self):
        self._w.set_coin(self.comboBox.currentText().upper())

    def set_wallet_type(self):
        if self.comboBox1.currentText() == 'bip44':
            self.comboBox.set_coins(44)
            self._w.set_bip('bip44')
        elif self.comboBox1.currentText() == 'bip49':
            self.comboBox.set_coins(49)
            self._w.set_bip('bip49')

    def _set_name(self):
        _b_ok = QDialogButtonBox.Ok

        _name = self.lineEdit_2.text().strip()
        _filters = ['\\', '/', '\'', '"', ',', '*',
                    '?', '<', '>', ':', ';', '|']
        for _filter in _filters:
            if _filter in _name:
                self.buttonBox.button(_b_ok).setEnabled(False)
                return

        if _name != '' and self.plainTextEdit.toPlainText().strip() != '':
            self._w.set_name(_name)
            self.buttonBox.button(_b_ok).setEnabled(True)
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)
