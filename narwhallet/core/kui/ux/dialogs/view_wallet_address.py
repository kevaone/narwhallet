from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit,
                             QDialog, QFrame, QPushButton)

from narwhallet.core.kui.ux.widgets.qr_widget import QRImage
from narwhallet.control.shared import MShared


class Ui_v_addr_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        _transm_st = QtCore.Qt.SmoothTransformation
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.verticalLayout = QVBoxLayout(self)
        self.label_hl = QHBoxLayout()
        self.label_label = QLabel(self)
        self.label_d = QLineEdit(self)
        self.address_hl = QHBoxLayout()
        self.address_label = QLabel(self)
        self.address_d = QPlainTextEdit(self)
        self.details_show = QHBoxLayout()
        self.details_show_label = QLabel(self)
        self.details_show_img = QPushButton(self)
        self.details = QFrame(self)
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
        self.qr_d = QLabel(self)
        self.qr_hl2 = QHBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('waddress_dlg')
        self.resize(425, 425)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.address_d.setMaximumHeight(26)
        self.address_d.setReadOnly(True)
        self.address_d.setFrameStyle(QFrame.NoFrame)
        self.details_show_img.setIcon(QIcon(self._ppic))
        self.details_show_img.setFlat(True)
        self.details.setVisible(False)
        self.details.setFrameShape(QFrame.StyledPanel)
        self.details.setFrameShadow(QFrame.Raised)
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
        self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.qr_hl1.addWidget(self.qr_d)
        self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.qr_hl1)
        self.verticalLayout.addLayout(self.qr_hl2)
        self.horizontalLayout.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)

        self.details_show_img.clicked.connect(self._display_details)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('waddress_dlg',
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
        self.qr_d.setPixmap(QRImage.make(data, image_factory=QRImage))

    def _display_details(self, event):
        if self.details.isVisible() is True:
            self.details.setVisible(False)
            self.details_show_img.setIcon(QIcon(self._ppic))
        else:
            self.details.setVisible(True)
            self.details_show_img.setIcon(QIcon(self._mpic))
