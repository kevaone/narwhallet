from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QDialogButtonBox,
                             QPlainTextEdit, QDialog)
from narwhallet.core.kui.ux.widgets.generator import HLSection
from narwhallet.control.shared import MShared


class Ui_warning_dlg(QDialog):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignCenter
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.message_pic = HLSection('', None)

        self.horizontalLayout_2 = QHBoxLayout()
        self._pic = QPixmap(MShared.get_resource_path('warning.png'))
        self.error_pic = QPixmap(MShared.get_resource_path('exclamation.png'))
        self.success_pic = QPixmap(MShared.get_resource_path('narwhal.png'))
        self.message_text = QPlainTextEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('warning_dlg')
        self.message_pic.label.setAlignment(_al_center)
        self.message_pic.label.setContentsMargins(0, 0, 0, 0)
        self.message_pic.label.setPixmap(self._pic)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())

        self.verticalLayout.addLayout(self.message_pic)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.horizontalLayout_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.horizontalLayout_2.addWidget(self.message_text)
        self.horizontalLayout_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addItem(QSpacerItem(5, 20, _sp_exp, _sp_min))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('warning_dlg', 'Narwhallet - Warning'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def set_message(self, message):
        _translate = QtCore.QCoreApplication.translate
        self.message_text.setPlainText(_translate('warning_dlg', message))
