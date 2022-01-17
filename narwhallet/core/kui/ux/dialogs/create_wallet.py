from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QComboBox, QPlainTextEdit, QDialog,
                             QPushButton, QLineEdit, QSpacerItem, QFrame,
                             QSizePolicy, QDialogButtonBox, QRadioButton)
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_create_wallet_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _transm_st = QtCore.Qt.SmoothTransformation

        self.verticalLayout = QVBoxLayout(self)
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.wallet_name = HLSection('Name:', QLineEdit(self))
        self.options_label = HLSection('Options -', QPushButton(self))
        self.options = QFrame(self)
        self.options_verticalLayout = QVBoxLayout(self.options)
        self.coin = HLSection('Coin:', QComboBox(self))
        self.coin.widgets[0].addItem('Kevacoin', 'KEVACOIN')
        self.coin_network_label = HLSection('Network:', None)
        self.coin_network = HLSection('', [QRadioButton(self),
                                      QRadioButton(self), QRadioButton(self),
                                      QRadioButton(self)])
        self.wallet_bip = HLSection('Bip:', QComboBox(self))
        self.mnemonic_language = HLSection('Language:', QComboBox(self))
        self.mnemonic_language.widgets[0].addItem('English', 'ENGLISH')
        self.mnemonic_language.widgets[0].addItem('Italian', 'ITALIAN')
        self.mnemonic_language.widgets[0].addItem('French', 'FRENCH')
        self.mnemonic_language.widgets[0].addItem('Spanish', 'SPANISH')
        self.mnemonic_language.widgets[0].addItem('Portuguese', 'PORTUGUESE')
        self.mnemonic_language.widgets[0].addItem('Czech', 'CZECH')
        self.mnemonic_language.widgets[0].addItem('Chinese Simplified',
                                                  'CHINESE_SIMPLIFIED')
        self.mnemonic_language.widgets[0].addItem('Chinese Traditional',
                                                  'CHINESE_TRADITIONAL')
        self.mnemonic_language.widgets[0].addItem('Korean', 'KOREAN')
        self.mnemonic_words = HLSection('Words:', QComboBox(self))
        self.mnemonic_words.widgets[0].addItem('12', 12)
        self.mnemonic_words.widgets[0].addItem('15', 15)
        self.mnemonic_words.widgets[0].addItem('18', 18)
        self.mnemonic_words.widgets[0].addItem('21', 21)
        self.mnemonic_words.widgets[0].addItem('24', 24)
        self.mnemonic_words.widgets[0].setCurrentIndex(4)
        self.mnemonic_passphrase = HLSection('Passphrase:', QLineEdit(self))
        self.mnemonic_passphrase_confirm = HLSection('Confirm:',
                                                     QLineEdit(self))
        self.options_verticalLayout.addLayout(self.coin_network_label)
        self.options_verticalLayout.addLayout(self.coin_network)
        self.options_verticalLayout.addLayout(self.wallet_bip)
        self.options_verticalLayout.addLayout(self.mnemonic_language)
        self.options_verticalLayout.addLayout(self.mnemonic_words)
        self.options_verticalLayout.addLayout(self.mnemonic_passphrase)
        self.options_verticalLayout.addLayout(self.mnemonic_passphrase_confirm)
        self.generate_mnemonic = HLSection('', QPushButton(self))
        self.generate_mnemonic.widgets[0].setText('Generate Mnemonic')
        self.mnemonic_label = HLSection('Mnemonic:', None)
        self.mnemonic = QPlainTextEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('create_dlg')
        self.resize(400, 475)

        self.coin_network.widgets[0].setText('mainnet')
        self.coin_network.widgets[0].setChecked(True)
        self.coin_network.widgets[1].setText('testnet')
        self.coin_network.widgets[2].setText('signet')
        self.coin_network.widgets[3].setText('regtest')
        self.coin_network.widgets[1].setEnabled(False)
        self.coin_network.widgets[2].setEnabled(False)
        self.coin_network.widgets[3].setEnabled(False)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.options_label.widgets[0].setIcon(QIcon(self._ppic))
        self.options_label.widgets[0].setFlat(True)
        self.options_label.widgets[0].setEnabled(False)
        self.options.setVisible(False)
        self.mnemonic_passphrase.widgets[0].setEchoMode(QLineEdit.Password)
        (self.mnemonic_passphrase_confirm.widgets[0]
         .setEchoMode(QLineEdit.Password))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.wallet_name)
        self.verticalLayout.addLayout(self.options_label)
        self.verticalLayout.addWidget(self.options)
        self.verticalLayout.addLayout(self.generate_mnemonic)
        self.verticalLayout.addLayout(self.mnemonic_label)
        self.verticalLayout.addWidget(self.mnemonic)
        self.verticalLayout.addWidget(self.buttonBox)

        self._init_wallet()
        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        (self.generate_mnemonic.widgets[0]
         .clicked.connect(self._generate_mnemonic))
        self.wallet_name.widgets[0].textChanged.connect(self._set_name)
        self.mnemonic.textChanged.connect(self._mnemonic_changed)
        (self.mnemonic_passphrase.widgets[0]
         .textChanged.connect(self._test_password_match))
        (self.mnemonic_passphrase_confirm.widgets[0]
         .textChanged.connect(self._test_password_match))
        self.coin.widgets[0].currentTextChanged.connect(self._set_coin)
        (self.wallet_bip.widgets[0]
         .currentTextChanged.connect(self.set_wallet_bip))
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.options_label.widgets[0].clicked.connect(self._display_advanced)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('create_dlg',
                                       'Narwhallet - Create Wallet'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _init_wallet(self):
        self._w = MWallet()

    def _display_advanced(self, _event):
        if self.options.isVisible() is True:
            self.options.setVisible(False)
            self.options_label.widgets[0].setIcon(QIcon(self._ppic))
        else:
            self.options.setVisible(True)
            self.options_label.widgets[0].setIcon(QIcon(self._mpic))

    def ret_wallet(self) -> MWallet:
        self._w.set_coin(self.coin.widgets[0].currentData())
        self._w.set_bip('bip49')

        if (self._w.mnemonic is None
           and self.mnemonic.toPlainText() != ''):

            _m = self.mnemonic.toPlainText().replace('\n', ' ')
            self._w.set_mnemonic(_m)

        self._w.generate_seed(self.mnemonic_passphrase.widgets[0].text())
        return self._w

    def _test_password_match(self):
        _b_ok = QDialogButtonBox.Ok

        if (self.mnemonic_passphrase.widgets[0].text() !=
                self.mnemonic_passphrase_confirm.widgets[0].text()):
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)

    def _generate_mnemonic(self):
        self._w.generate_mnemonic()
        self.mnemonic.setPlainText(self._w.mnemonic)

    def _mnemonic_changed(self):
        _b_ok = QDialogButtonBox.Ok

        if len(self.mnemonic.toPlainText().strip().split(' ')) != 24:
            self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(True)
            self._set_name()

    def _set_coin(self):
        self._w.set_coin(self.coin.widgets[0].currentText().upper())

    def set_wallet_bip(self):
        self._w.set_bip(self.wallet_bip.widgets[0].currentText())

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
