from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QLabel,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit,
                             QDialog, QFrame, QPushButton)
from narwhallet.core.kui.ux.widgets.qr_widget import QRImage
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import HLSection


class Ui_v_addr_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        _transm_st = QtCore.Qt.SmoothTransformation
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.verticalLayout = QVBoxLayout(self)
        # TODO Add coin display on address details
        # self.coin = HLSection('Coin:', QLineEdit(self))
        self.address = HLSection('Address:', QPlainTextEdit(self))
        self.label = HLSection('Label:', QLineEdit(self))
        self.details_show = HLSection('Details:', QPushButton(self))
        self.details = QFrame(self)
        self.details_verticalLayout = QVBoxLayout(self.details)
        self.balance = HLSection('Balance:', QLabel(self))
        self.recevied = HLSection('Received:', QLabel(self))
        self.sent = HLSection('Sent:', QLabel(self))
        self.locked = HLSection('Locked:', QLabel(self))
        self.qr_code = HLSection('', None)
        self.qr_data = HLSection('QR Data:', QLineEdit(self))
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('waddress_dlg')
        self.resize(425, 425)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.address.widgets[0].setMaximumHeight(28)
        self.address.widgets[0].setReadOnly(True)
        self.address.widgets[0].setFrameStyle(QFrame.NoFrame)
        self.details_show.widgets[0].setIcon(QIcon(self._ppic))
        self.details_show.widgets[0].setFlat(True)
        self.details.setVisible(False)
        self.details.setFrameShape(QFrame.StyledPanel)
        self.details.setFrameShadow(QFrame.Raised)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

        self.verticalLayout.addLayout(self.label)
        self.verticalLayout.addLayout(self.address)
        self.verticalLayout.addLayout(self.details_show)
        self.details_verticalLayout.addLayout(self.balance)
        self.details_verticalLayout.addLayout(self.recevied)
        self.details_verticalLayout.addLayout(self.sent)
        self.details_verticalLayout.addLayout(self.locked)
        self.verticalLayout.addWidget(self.details)
        self.verticalLayout.addLayout(self.qr_code)
        self.verticalLayout.addLayout(self.qr_data)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)

        self.details_show.widgets[0].clicked.connect(self._display_details)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('waddress_dlg',
                                       'Narwhallet - Address'))

    def set_qr(self, data: str):
        self.qr_code.label.setPixmap(QRImage.make(data, image_factory=QRImage))
        self.qr_data.widgets[0].setText(data)

    def _display_details(self, _event):
        if self.details.isVisible() is True:
            self.details.setVisible(False)
            self.details_show.widgets[0].setIcon(QIcon(self._ppic))
        else:
            self.details.setVisible(True)
            self.details_show.widgets[0].setIcon(QIcon(self._mpic))
