from PyQt5 import QtCore
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QSpacerItem, QSizePolicy,
                             QDialogButtonBox)
from narwhallet.core.kui.ux.widgets.generator import UShared, HLSection


class Ui_add_ns_fav_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self.verticalLayout = QVBoxLayout(self)
        self.name = HLSection('Coin:', QLineEdit(self))
        self.shortcode = HLSection('Shortcode:', QLineEdit(self))
        self.horizontalLayout_1 = QHBoxLayout()
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('add_ns_fav_dlg')
        self.resize(430, 225)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(self.set_buttons())
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.horizontalLayout_1.addWidget(UShared.dialog_header_graphic())
        self.verticalLayout.addLayout(self.name)
        self.verticalLayout.addLayout(self.shortcode)
        self.verticalLayout.addItem(QSpacerItem(10, 10, _sp_min, _sp_exp))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.shortcode.widgets[0].textChanged.connect(self._test_name)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('add_ns_fav_dlg',
                                       'Narwhallet - Add Favorite'))

    @staticmethod
    def set_buttons():
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def _test_name(self):
        # TODO Add Shortcode test, extend to allow NS id as well as TX id
        _b_ok = QDialogButtonBox.Ok

        if self.shortcode.widgets[0].text() != '':
            try:
                int(self.shortcode.widgets[0].text())
                self.buttonBox.button(_b_ok).setEnabled(True)
            except Exception:
                self.buttonBox.button(_b_ok).setEnabled(False)
        else:
            self.buttonBox.button(_b_ok).setEnabled(False)
