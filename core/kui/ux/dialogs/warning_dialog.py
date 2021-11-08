import os
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox)


class Ui_warning_dlg(QObject):
    def setupUi(self, warning_dialog: QDialog):
        _al_center = QtCore.Qt.AlignCenter
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(warning_dialog)
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_1 = QLabel(warning_dialog)
        __path = os.path.dirname(__file__)
        self._pic = QPixmap(os.path.join(__path, '../assets/warning.png'))
        self.error_pic = QPixmap(os.path.join(__path,
                                               '../assets/exclamation.png'))
        self.success_pic = QPixmap(os.path.join(__path,
                                                 '../assets/narwhal.png'))
        self.label_2 = QLabel(warning_dialog)
        self.buttonBox = QDialogButtonBox(warning_dialog)

        warning_dialog.setObjectName('warning_dlg')
        self.label_1.setAlignment(_al_center)
        self.label_1.setContentsMargins(0, 0, 0, 0)
        self.label_1.setPixmap(self._pic)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.horizontalLayout_1.addWidget(self.label_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(warning_dialog)
        self.buttonBox.accepted.connect(warning_dialog.accept)
        self.buttonBox.rejected.connect(warning_dialog.reject)

    def retranslateUi(self, warning_dialog: QDialog):
        _translate = QtCore.QCoreApplication.translate
        warning_dialog.setWindowTitle(_translate('warning_dlg',
                                                 'Narwhallet - Warning'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def set_message(self, message):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate('warning_dlg', message))
