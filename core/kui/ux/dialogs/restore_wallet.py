import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QComboBox,
                             QPlainTextEdit, QHBoxLayout, QLineEdit,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QFrame)
from core.kui.ux.widgets.coin_dropdown import _coin_dropdown
from core.kcl.models.wallet import MWallet


class Ui_restore_wallet_dlg(QObject):
    def setupUi(self, restore_wallet_dialog: QDialog):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        self.verticalLayout = QVBoxLayout(restore_wallet_dialog)
        self.label_1 = QLabel(restore_wallet_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_4 = QLabel(restore_wallet_dialog)
        self.lineEdit_2 = QLineEdit(restore_wallet_dialog)
        self.horizontalLayout = QHBoxLayout()
        self.label_5 = QLabel(restore_wallet_dialog)
        self.comboBox1 = QComboBox(restore_wallet_dialog)
        self.label = QLabel(restore_wallet_dialog)
        self.comboBox = _coin_dropdown(restore_wallet_dialog)
        self.horizontalLayout_2 = QHBoxLayout()
        self.plainTextEdit = QPlainTextEdit(restore_wallet_dialog)
        self._ppic = QtGui.QPixmap(os.path.join(__path, '../assets/plus.png'))
        self._mpic = QtGui.QPixmap(os.path.join(__path, '../assets/minus.png'))
        self.adv_hl = QHBoxLayout()
        self.adv_label = QLabel(restore_wallet_dialog)
        self.adv_label_p = QLabel(restore_wallet_dialog)
        self.adv_f = QFrame(restore_wallet_dialog)
        self.adv_f_vl = QVBoxLayout(self.adv_f)
        self.label_2 = QLabel(restore_wallet_dialog)
        self.lineEdit = QLineEdit(restore_wallet_dialog)
        self.buttonBox = QDialogButtonBox(restore_wallet_dialog)
        self.label_3 = QLabel(restore_wallet_dialog)

        restore_wallet_dialog.setObjectName('restore_dlg')
        restore_wallet_dialog.resize(400, 400)
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.label_5.setVisible(False)
        self.comboBox1.addItem('-')
        self.comboBox1.addItem('bip32')
        # self.comboBox1.addItem('bip44')
        self.comboBox1.addItem('bip49')
        self.comboBox1.setVisible(False)
        self.label.setVisible(False)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.adv_label_p.setPixmap(self._ppic)
        self.adv_label_p.setVisible(False)
        self.adv_label.setVisible(False)
        self.adv_f.setVisible(False)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(self.label_1)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addWidget(self.label_5)
        self.horizontalLayout.addWidget(self.comboBox1)
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.adv_hl.addWidget(self.adv_label)
        self.adv_hl.addWidget(self.adv_label_p)
        self.adv_hl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.adv_hl)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.adv_f_vl.addLayout(self.horizontalLayout_2)
        self.adv_f_vl.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.adv_f)
        self.verticalLayout.addWidget(self.buttonBox)

        self._init_wallet()
        self.retranslateUi(restore_wallet_dialog)
        self.buttonBox.accepted.connect(restore_wallet_dialog.accept)
        self.buttonBox.rejected.connect(restore_wallet_dialog.reject)
        self.lineEdit_2.textChanged.connect(self._set_name)
        self.plainTextEdit.textChanged.connect(self._set_mnemonic)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.adv_label_p.mousePressEvent = self._display_advanced

    def retranslateUi(self, restore_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        restore_dlg.setWindowTitle(_translate('restore_dlg',
                                              'Narwhallet - Restore Wallet'))
        self.label_4.setText(_translate('restore_dlg', 'Name:'))
        self.label.setText(_translate('restore_dlg', 'Coin:'))
        self.label_5.setText(_translate('restore_dlg', 'Type:'))
        self.adv_label.setText(_translate('restore_dlg', 'Advanced'))
        self.label_2.setText(_translate('restore_dlg', '*Password:'))
        self.label_3.setText(_translate('restore_dlg',
                                        '* = Optional Mnemonic Seed Password'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._w = MWallet()

    def _display_advanced(self, event):
        if self.adv_f.isVisible() is True:
            self.adv_f.setVisible(False)
            self.adv_label_p.setPixmap(self._ppic)
        else:
            self.adv_f.setVisible(True)
            self.adv_label_p.setPixmap(self._mpic)

    def ret_wallet(self):
        self._w.set_coin(self.comboBox.currentText().upper())
        if self._w.bip == 'bip49' and self._w.mnemonic is not None:
            self._w.generate_seed(self.lineEdit.text())

        return self._w

    def _set_mnemonic(self):
        _b_ok = QDialogButtonBox.Ok

        if self.plainTextEdit.toPlainText().startswith('xprv'):
            self._w.set_bip('bip32')
            self._w.set_extended_prv(self.plainTextEdit.toPlainText())
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()
        elif self.plainTextEdit.toPlainText().startswith('xpub'):
            self._w.set_bip('bip32')
            self._w.set_extended_pub(self.plainTextEdit.toPlainText())
            if self._w.extended_pub is not None:
                self.buttonBox.button(_b_ok).setEnabled(True)
                self._set_name()
        elif self.plainTextEdit.toPlainText().startswith('ypub'):
            self._w.set_bip('bip49')
            self._w.set_kind(1)
            self._w.set_extended_pub(self.plainTextEdit.toPlainText())
            if self._w.extended_pub is not None:
                self.buttonBox.button(_b_ok).setEnabled(True)
                self._set_name()
        elif self.plainTextEdit.toPlainText().strip() == '':
            self.buttonBox.button(_b_ok).setEnabled(False)
        elif len(self.plainTextEdit.toPlainText()
                 .strip().replace('\n', ' ').split(' ')) == 24:
            self._w.set_bip('bip49')
            _mn = self.plainTextEdit.toPlainText().replace('\n', ' ')
            self._w.set_mnemonic(_mn)
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)

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
