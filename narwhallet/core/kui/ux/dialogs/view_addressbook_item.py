from PyQt5 import QtCore
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QFrame,
                             QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit)
from narwhallet.core.kui.ux.widgets.qr_widget import QRImage
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_v_ab_item_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok

        self.verticalLayout = QVBoxLayout(self)
        # TODO Add coin display on address details
        # self.coin = HLSection('Coin:', QLineEdit(self))
        self.name = HLSection('Name:', QLineEdit(self))
        self.label = HLSection('Label:', QLineEdit(self))
        self.address = HLSection('Address:', QPlainTextEdit(self))
        # TODO Fix centering
        self.qr_code = HLSection('', None)
        self.qr_data = HLSection('QR Data:', QLineEdit(self))
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('view_ab_item_dlg')
        self.setMinimumSize(QtCore.QSize(425, 225))
        # self.coin.widgets[0].setReadOnly(True)
        self.address.widgets[0].setReadOnly(True)
        self.address.widgets[0].setFrameStyle(QFrame.NoFrame)
        self.address.widgets[0].setMaximumHeight(28)
        self.qr_data.widgets[0].setReadOnly(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        # self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.name)
        self.verticalLayout.addLayout(self.label)
        self.verticalLayout.addLayout(self.address)
        # self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.qr_code)
        # self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.qr_data)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        self.buttonBox.accepted.connect(self.accept)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('view_ab_item_dlg',
                                       'Narwhallet - Address Book'))

    def set_qr(self, data: str):
        self.qr_code.label.setPixmap(QRImage.make(data, image_factory=QRImage))
        self.qr_data.widgets[0].setText(data)
