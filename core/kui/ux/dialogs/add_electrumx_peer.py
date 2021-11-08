import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QCheckBox, QPushButton,
                             QHBoxLayout, QLineEdit, QSpacerItem,
                             QSizePolicy, QDialogButtonBox)
from PyQt5.QtWidgets import QDialog

from core.kui.ux.widgets.coin_dropdown import _coin_dropdown


class Ui_add_electrumx_peer_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _al_center = QtCore.Qt.AlignCenter

        self.verticalLayout = QVBoxLayout(self)
        self.label_1 = QLabel(self)
        __path = os.path.dirname(__file__)
        _pic = QtGui.QPixmap(os.path.join(__path, '../assets/narwhal.png'))
        self.horizontalLayout = QHBoxLayout()
        self.comboBox = _coin_dropdown(self)
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_2 = QLabel(self)
        self.lineEdit = QLineEdit(self)
        self.label_3 = QLabel(self)
        self.lineEdit_2 = QLineEdit(self)
        self.port_v = QtGui.QIntValidator(self.lineEdit_2)
        self.checkBox = QCheckBox(self)
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_4 = QLabel(self)
        self.pushButton = QPushButton(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('create_electrumx_peer_dlg')
        self.resize(447, 175)
        self.setMaximumSize(QtCore.QSize(500, 175))
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(_pic)
        self.comboBox.setCurrentText('Kevacoin')
        self.comboBox.setVisible(False)
        self.lineEdit_2.setValidator(self.port_v)
        self.label_4.setMinimumSize(QtCore.QSize(325, 0))
        self.label_4.setText('')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(self.label_1)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_3.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('create_electrumx_peer_dlg',
                            'Narwhallet - Add ElectrumX Peer'))
        # self.label.setText(_translate('create_electrumx_peer_dlg', 'Coin:'))
        self.label_2.setText(_translate('create_electrumx_peer_dlg', 'Host:'))
        self.label_3.setText(_translate('create_electrumx_peer_dlg', 'Port:'))
        self.checkBox.setText(_translate('create_electrumx_peer_dlg', 'TLS'))
        self.pushButton.setText(_translate('create_electrumx_peer_dlg',
                                           'Test'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel
