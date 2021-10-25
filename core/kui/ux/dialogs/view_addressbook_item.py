import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QFrame,
                             QHBoxLayout, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit, QDialog)

from core.kui.ux.widgets.qr_widget import QRImage
from core.kui.ux.widgets.coin_dropdown import _coin_dropdown


class Ui_v_ab_item_dlg(QObject):
    def setupUi(self, view_addressbook_item_dialog: QDialog):

        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        _al_center = QtCore.Qt.AlignCenter
        _wt_flh = QtCore.Qt.FramelessWindowHint

        self.verticalLayout = QVBoxLayout(view_addressbook_item_dialog)
        self.label_1 = QLabel(view_addressbook_item_dialog)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(view_addressbook_item_dialog)
        self.comboBox = _coin_dropdown(view_addressbook_item_dialog)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_2 = QLabel(view_addressbook_item_dialog)
        self.lineEdit = QLineEdit(view_addressbook_item_dialog)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_4 = QLabel(view_addressbook_item_dialog)
        self.lineEdit_3 = QPlainTextEdit(view_addressbook_item_dialog)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_3 = QLabel(view_addressbook_item_dialog)
        self.lineEdit_2 = QLineEdit(view_addressbook_item_dialog)
        self.qr_hl1 = QHBoxLayout()
        self.qr_d = QLabel(view_addressbook_item_dialog)
        self.qr_hl2 = QHBoxLayout()
        self.qr_label = QPlainTextEdit(view_addressbook_item_dialog)
        self.horizontalLayout5 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(view_addressbook_item_dialog)

        view_addressbook_item_dialog.setObjectName('view_ab_item_dlg')
        view_addressbook_item_dialog.setWindowFlag(_wt_flh)
        view_addressbook_item_dialog.setMinimumSize(QtCore.QSize(425, 225))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.label.setVisible(False)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setFrameStyle(QFrame.NoFrame)
        self.lineEdit_3.setMaximumHeight(26)
        self.qr_label.setMaximumHeight(26)
        self.qr_label.setReadOnly(True)
        self.qr_label.setFrameStyle(QFrame.NoFrame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

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
        self.qr_hl1.addWidget(self.qr_d)
        self.qr_hl2.addWidget(self.qr_label)
        self.verticalLayout.addLayout(self.qr_hl1)
        self.verticalLayout.addLayout(self.qr_hl2)
        self.horizontalLayout5.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout5)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(view_addressbook_item_dialog)

        self.buttonBox.accepted.connect(view_addressbook_item_dialog.accept)

    def retranslateUi(self, view_ab_dlg: QDialog):
        _translate = QtCore.QCoreApplication.translate
        view_ab_dlg.setWindowTitle(_translate('view_ab_item_dlg',
                                              'Narwhallet - Address Book'))
        self.label.setText(_translate('view_ab_item_dlg', 'Coin:'))
        self.label_2.setText(_translate('view_ab_item_dlg', 'Name:'))
        self.label_3.setText(_translate('view_ab_item_dlg', 'Label:'))
        self.label_4.setText(_translate('view_ab_item_dlg', 'Address:'))

    def set_qr(self, data: str):
        _data = 'kevacoin://' + data
        self.qr_d.setPixmap(QRImage.make(_data, image_factory=QRImage))

    def set_qr_uri(self, data: str):
        _data = 'kevacoin://' + data
        self.qr_label.setPlainText(_data)
