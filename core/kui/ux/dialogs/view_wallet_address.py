import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog, QFrame
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit)

from core.kui.ux.widgets.qr_widget import QRImage


class Ui_v_addr_dlg(QObject):
    def setupUi(self, view_wallet_address_dialog: QDialog):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        _transm_st = QtCore.Qt.SmoothTransformation
        __path = os.path.dirname(__file__)
        self._ppic = QtGui.QPixmap(os.path.join(__path, '../assets/plus.png'))
        self._mpic = QtGui.QPixmap(os.path.join(__path, '../assets/minus.png'))
        self.verticalLayout = QVBoxLayout(view_wallet_address_dialog)
        self.label_hl = QHBoxLayout()
        self.label_label = QLabel(view_wallet_address_dialog)
        self.label_d = QLineEdit(view_wallet_address_dialog)
        self.address_hl = QHBoxLayout()
        self.address_label = QLabel(view_wallet_address_dialog)
        self.address_d = QPlainTextEdit(view_wallet_address_dialog)
        self.details_show = QHBoxLayout()
        self.details_show_label = QLabel(view_wallet_address_dialog)
        self.details_show_img = QLabel(view_wallet_address_dialog)
        self.details = QFrame(view_wallet_address_dialog)
        self.details_verticalLayout = QVBoxLayout(self.details)
        self.details_horizontalLayout5 = QHBoxLayout()
        self.details_balance = QLabel(self.details)
        self.details_balance_d = QLabel(self.details)
        self.details_horizontalLayout1 = QHBoxLayout()
        self.details_received = QLabel(self.details)
        self.details_received_d = QLabel(self.details)
        self.details_horizontalLayout2 = QHBoxLayout()
        self.details_sent = QLabel(self.details)
        self.details_sent_d = QLabel(self.details)
        self.details_horizontalLayout3 = QHBoxLayout()
        self.details_locked = QLabel(self.details)
        self.details_locked_d = QLabel(self.details)
        self.qr_hl1 = QHBoxLayout()
        self.qr_d = QLabel(view_wallet_address_dialog)
        self.qr_hl2 = QHBoxLayout()
        self.qr_label = QPlainTextEdit(view_wallet_address_dialog)
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(view_wallet_address_dialog)

        view_wallet_address_dialog.setObjectName('waddress_dlg')
        view_wallet_address_dialog.resize(430, 425)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.address_d.setMaximumHeight(26)
        self.address_d.setReadOnly(True)
        self.address_d.setFrameStyle(QFrame.NoFrame)
        self.details_show_img.setPixmap(self._ppic)
        self.details.setVisible(False)
        self.details.setFrameShape(QFrame.StyledPanel)
        self.details.setFrameShadow(QFrame.Raised)
        self.qr_label.setMaximumHeight(26)
        self.qr_label.setReadOnly(True)
        self.qr_label.setFrameStyle(QFrame.NoFrame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

        self.label_hl.addWidget(self.label_label)
        self.label_hl.addWidget(self.label_d)
        self.verticalLayout.addLayout(self.label_hl)
        self.address_hl.addWidget(self.address_label)
        self.address_hl.addWidget(self.address_d)
        self.verticalLayout.addLayout(self.address_hl)
        self.details_show.addWidget(self.details_show_label)
        self.details_show.addWidget(self.details_show_img)
        self.verticalLayout.addLayout(self.details_show)
        self.details_horizontalLayout5.addWidget(self.details_balance)
        self.details_horizontalLayout5.addWidget(self.details_balance_d)
        self.details_horizontalLayout1.addWidget(self.details_received)
        self.details_horizontalLayout1.addWidget(self.details_received_d)
        self.details_horizontalLayout2.addWidget(self.details_sent)
        self.details_horizontalLayout2.addWidget(self.details_sent_d)
        self.details_horizontalLayout3.addWidget(self.details_locked)
        self.details_horizontalLayout3.addWidget(self.details_locked_d)
        self.details_verticalLayout.addLayout(self.details_horizontalLayout5)
        self.details_verticalLayout.addLayout(self.details_horizontalLayout1)
        self.details_verticalLayout.addLayout(self.details_horizontalLayout2)
        self.details_verticalLayout.addLayout(self.details_horizontalLayout3)
        self.verticalLayout.addWidget(self.details)
        self.qr_hl1.addWidget(self.qr_d)
        self.qr_hl2.addWidget(self.qr_label)
        self.verticalLayout.addLayout(self.qr_hl1)
        self.verticalLayout.addLayout(self.qr_hl2)
        self.horizontalLayout.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(view_wallet_address_dialog)
        self.buttonBox.accepted.connect(view_wallet_address_dialog.accept)

        self.details_show_img.mousePressEvent = self._display_details

    def retranslateUi(self, view_waddr_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        view_waddr_dlg.setWindowTitle(_translate('waddress_dlg',
                                                 'Narwhallet - Address'))
        self.label_label.setText(_translate('waddress_dlg', 'Label:'))
        self.address_label.setText(_translate('waddress_dlg', 'Address:'))
        self.details_show_label.setText(_translate('waddress_dlg', 'Details'))
        self.details_balance.setText(_translate('waddress_dlg', 'Balance:'))
        self.details_received.setText(_translate('waddress_dlg', 'Received:'))
        self.details_received_d.setText(_translate('waddress_dlg', '0.0'))
        self.details_sent.setText(_translate('waddress_dlg', 'Sent:'))
        self.details_sent_d.setText(_translate('waddress_dlg', '0.0'))
        self.details_locked.setText(_translate('waddress_dlg', 'Locked:'))
        self.details_locked_d.setText(_translate('waddress_dlg', '0.0'))

    def set_qr(self, data: str):
        _data = 'kevacoin://' + data
        self.qr_d.setPixmap(QRImage.make(_data, image_factory=QRImage))

    def set_qr_uri(self, data: str):
        _data = 'kevacoin://' + data
        self.qr_label.setPlainText(_data)

    def _display_details(self, event):
        if self.details.isVisible() is True:
            self.details.setVisible(False)
            self.details_show_img.setPixmap(self._ppic)
        else:
            self.details.setVisible(True)
            self.details_show_img.setPixmap(self._mpic)
