from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QCheckBox,
                             QComboBox, QLineEdit, QSpacerItem,
                             QSizePolicy, QDialogButtonBox)
from PyQt5.QtWidgets import QDialog
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_add_electrumx_peer_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.coin = HLSection('Coin:', QComboBox(self))
        self.host = HLSection('Host:', [QLineEdit(self), QLabel(self),
                                        QLineEdit(self), QCheckBox(self)])
        self.port_v = QtGui.QIntValidator(self.host.widgets[2])
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('create_electrumx_peer_dlg')
        self.resize(447, 175)
        self.setMaximumSize(QtCore.QSize(500, 175))
        self.coin.widgets[0].addItem('Kevacoin', 'KEVACOIN')
        self.host.widgets[1].setText('Port:')
        self.host.widgets[2].setValidator(self.port_v)
        self.host.widgets[3].setText('TLS')
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.coin)
        self.verticalLayout.addLayout(self.host)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('create_electrumx_peer_dlg',
                            'Narwhallet - Add ElectrumX Peer'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel
