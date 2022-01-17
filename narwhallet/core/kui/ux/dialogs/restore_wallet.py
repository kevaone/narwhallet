from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QComboBox,
                             QPlainTextEdit, QLineEdit,
                             QSpacerItem, QSizePolicy, QDialogButtonBox)
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_restore_wallet_dlg(QDialog):
    def setupUi(self):
        # FIXME Add in more recovery support, ie attempt to detect input.
        # Assuming Kevacoin
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.coin = HLSection('Coin:', QComboBox(self))
        self.wallet_name = HLSection('Name:', QLineEdit(self))
        self.mnemonic_label = HLSection('Mnemonic:', None)
        self.mnemonic = QPlainTextEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('restore_dlg')
        self.resize(400, 400)
        self.coin.widgets[0].addItem('Kevacoin', 'KEVACOIN')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.wallet_name)
        self.verticalLayout.addLayout(self.mnemonic_label)
        self.verticalLayout.addWidget(self.mnemonic)
        self.verticalLayout.addWidget(self.buttonBox)

        self._init_wallet()
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.wallet_name.widgets[0].textChanged.connect(self._set_name)
        self.mnemonic.textChanged.connect(self._set_mnemonic)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('restore_dlg',
                                       'Narwhallet - Restore Wallet'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._w = MWallet()

    # def _display_advanced(self, _event):
    #     if self.adv_f.isVisible() is True:
    #         self.adv_f.setVisible(False)
    #         self.adv_label_p.setIcon(QIcon(self._ppic))
    #     else:
    #         self.adv_f.setVisible(True)
    #         self.adv_label_p.setIcon(QIcon(self._mpic))

    def ret_wallet(self):
        self._w.set_coin(self.coin.widgets[0].currentData())
        if self._w.bip == 'bip49' and self._w.mnemonic is not None:
            # TODO Pass password if advanced enabled
            self._w.generate_seed('')

        return self._w

    def _set_mnemonic(self):
        _b_ok = QDialogButtonBox.Ok

        if self.mnemonic.toPlainText().startswith('xprv'):
            self._w.set_bip('bip32')
            self._w.set_extended_prv(self.mnemonic.toPlainText())
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()
        elif self.mnemonic.toPlainText().startswith('xpub'):
            self._w.set_bip('bip32')
            self._w.set_extended_pub(self.mnemonic.toPlainText())
            if self._w.extended_pub is not None:
                self.buttonBox.button(_b_ok).setEnabled(True)
                self._set_name()
        elif self.mnemonic.toPlainText().startswith('ypub'):
            self._w.set_bip('bip49')
            self._w.set_kind(1)
            self._w.set_extended_pub(self.mnemonic.toPlainText())
            if self._w.extended_pub is not None:
                self.buttonBox.button(_b_ok).setEnabled(True)
                self._set_name()
        elif self.mnemonic.toPlainText().strip() == '':
            self.buttonBox.button(_b_ok).setEnabled(False)
        elif len(self.mnemonic.toPlainText()
                 .strip().replace('\n', ' ').split(' ')) == 24:
            self._w.set_bip('bip49')
            _mn = self.mnemonic.toPlainText().replace('\n', ' ')
            self._w.set_mnemonic(_mn)
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)

    def _set_name(self):
        _b_ok = QDialogButtonBox.Ok

        _name = self.wallet_name.widgets[0].text().strip()
        _filters = ['\\', '/', '\'', '"', ',', '*',
                    '?', '<', '>', ':', ';', '|']
        for _filter in _filters:
            if _filter in _name:
                self.buttonBox.button(_b_ok).setEnabled(False)
                return

        if _name != '' and self.mnemonic.toPlainText().strip() != '':
            self._w.set_name(_name)
            self.buttonBox.button(_b_ok).setEnabled(True)
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)
