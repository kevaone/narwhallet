from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QVBoxLayout, QLineEdit, QLabel, QFrame,
                             QHBoxLayout, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QPlainTextEdit, QDialog)

from narwhallet.core.kui.ux.widgets.qr_widget import QRImage
from narwhallet.core.kui.ux.widgets.coin_dropdown import _coin_dropdown
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets.generator import UShared


class Ui_v_ab_item_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _b_ok = QDialogButtonBox.Ok
        # _al_center = QtCore.Qt.AlignCenter

        self.verticalLayout = QVBoxLayout(self)
        # self.label_1 = QLabel(self)
        # _pic = QtGui.QPixmap(MShared.get_resource_path('narwhal.png'))
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.comboBox = _coin_dropdown(self)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.lineEdit = QLineEdit(self)
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_4 = QLabel(self)
        self.lineEdit_3 = QPlainTextEdit(self)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_3 = QLabel(self)
        self.lineEdit_2 = QLineEdit(self)
        self.qr_hl1 = QHBoxLayout()
        self.qr_d = QLabel(self)
        self.qr_hl2 = QHBoxLayout()
        self.horizontalLayout5 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('view_ab_item_dlg')
        self.setMinimumSize(QtCore.QSize(425, 225))
        # self.label_1.setAlignment(_al_center)
        # self.label_1.setContentsMargins(0, 0, 0, 0)
        # self.label_1.setPixmap(_pic)
        self.label.setVisible(False)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setFrameStyle(QFrame.NoFrame)
        self.lineEdit_3.setMaximumHeight(26)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
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
        self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.qr_hl1.addWidget(self.qr_d)
        self.qr_hl1.addItem(QSpacerItem(10, 10, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.qr_hl1)
        self.verticalLayout.addLayout(self.qr_hl2)
        self.horizontalLayout5.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout5)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()

        self.buttonBox.accepted.connect(self.accept)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('view_ab_item_dlg',
                                       'Narwhallet - Address Book'))
        self.label.setText(_translate('view_ab_item_dlg', 'Coin:'))
        self.label_2.setText(_translate('view_ab_item_dlg', 'Name:'))
        self.label_3.setText(_translate('view_ab_item_dlg', 'Label:'))
        self.label_4.setText(_translate('view_ab_item_dlg', 'Address:'))

    def set_qr(self, data: str):
        self.qr_d.setPixmap(QRImage.make(data, image_factory=QRImage))
