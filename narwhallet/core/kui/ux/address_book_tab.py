from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout,
                             QLabel, QSpacerItem, QSizePolicy, QPushButton)
from narwhallet.core.kui.ux.widgets import _address_book_table, _coin_dropdown


class Ui_AddressBookTab(QObject):
    def setupUi(self):
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum

        self.tabAddBook = QWidget()
        self.verticalLayout_1 = QVBoxLayout(self.tabAddBook)
        self.frame_1 = QFrame(self.tabAddBook)
        self.horizontalLayout_1 = QHBoxLayout(self.frame_1)
        self.label_1 = QLabel(self.frame_1)
        self.ab_tab_combo_coin = _coin_dropdown(self.frame_1)
        self.ab_tab_line_v_1 = QFrame(self.frame_1)
        self.frame_2 = QFrame(self.tabAddBook)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.btn_create = QPushButton(self.frame_2)
        self.tbl_addr = _address_book_table('ab_tab_tbl_addr', self.tabAddBook)

        self.tabAddBook.setObjectName('tabAddBook')
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_1.setVisible(False)
        self.label_1.setMaximumSize(QtCore.QSize(35, 16777215))
        self.ab_tab_combo_coin.setMaximumSize(QtCore.QSize(80, 100))
        self.ab_tab_line_v_1.setFrameShape(QFrame.Shape.VLine)
        self.ab_tab_line_v_1.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_1.addWidget(self.label_1)
        self.horizontalLayout_1.addWidget(self.ab_tab_combo_coin)
        self.horizontalLayout_1.addWidget(self.ab_tab_line_v_1)
        self.horizontalLayout_1.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.verticalLayout_1.addWidget(self.frame_1)
        self.horizontalLayout_2.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.horizontalLayout_2.addWidget(self.btn_create)
        self.verticalLayout_1.addWidget(self.frame_2)
        self.verticalLayout_1.addWidget(self.tbl_addr)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_1.setText(_translate('tabAddBook', 'Coin:'))
        self.btn_create.setText(_translate('tabAddBook', 'Add'))
