from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QSpacerItem, QSizePolicy,
                             QPushButton, QLineEdit, QFileDialog, QCheckBox,
                             QPlainTextEdit, QRadioButton, QTabWidget)
from narwhallet.core.kui.ux.widgets import AddressComboBox, WalletComboBox


class Ui_UtilsTab(QObject):
    def setupUi(self):
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum

        self.tabUtils = QWidget()
        self.verticalLayout_0 = QVBoxLayout(self.tabUtils)
        self.tabWidget_3 = QTabWidget(self.tabUtils)
        self.sign_tab = QWidget(self.tabWidget_3)
        self.verticalLayout_1 = QVBoxLayout(self.sign_tab)
        self.hl = QHBoxLayout()
        self.wallet_combo = WalletComboBox()
        self.hl_0 = QHBoxLayout()
        self.address_combo = AddressComboBox()
        self.thl_bcpl = QLabel(self.sign_tab)
        self.thl_bcp = QLineEdit(self.sign_tab)
        self.thl_a = QHBoxLayout()
        self.thl_ac = QRadioButton(self.tabUtils)
        self.hl_1a = QHBoxLayout()
        self.sm_e = QPlainTextEdit(self.sign_tab)
        self.thl_b = QHBoxLayout()
        self.thl_bc = QRadioButton(self.tabUtils)
        self.thl_b1 = QHBoxLayout()
        self.thl_bcl = QLineEdit(self.tabUtils)
        self.thl_bcb = QPushButton(self.tabUtils)
        self.hl_2 = QHBoxLayout()
        self.ss_label = QLabel(self.sign_tab)
        self.ss_e = QPlainTextEdit(self.sign_tab)
        self.hl_sb = QHBoxLayout()
        self.sbutton = QPushButton(self.sign_tab)
        self.verify_tab = QWidget(self.tabWidget_3)
        self.verticalLayout_2 = QVBoxLayout(self.verify_tab)
        self.hl_3 = QHBoxLayout()
        self.va_label = QLabel(self.verify_tab)
        self.va_e = QLineEdit(self.verify_tab)
        self.vthl_a = QHBoxLayout()
        self.vthl_ac = QRadioButton(self.tabUtils)
        self.hl_4a = QHBoxLayout()
        self.vm_e = QPlainTextEdit(self.verify_tab)
        self.vthl_b = QHBoxLayout()
        self.vthl_bc = QRadioButton(self.tabUtils)
        self.vthl_b1 = QHBoxLayout()
        self.vthl_bcl = QLineEdit(self.tabUtils)
        self.vthl_bcb = QPushButton(self.tabUtils)
        self.hl_5 = QHBoxLayout()
        self.vs_label = QLabel(self.verify_tab)
        self.vs_e = QPlainTextEdit(self.verify_tab)
        self.hl_vb = QHBoxLayout()
        self.vbutton = QPushButton(self.verify_tab)
        self.hl_6 = QHBoxLayout()
        self.success_label = QLabel(self.verify_tab)
        self.misc_tab = QWidget(self.tabWidget_3)
        self.verticalLayout_3 = QVBoxLayout(self.misc_tab)
        self.mhl = QHBoxLayout()
        self.m_select_label = QLabel(self.misc_tab)
        self.m_select = QComboBox(self.misc_tab)
        self.mhl_0 = QHBoxLayout()
        self.msa_label = QLabel(self.misc_tab)
        self.mishex = QCheckBox(self.misc_tab)
        self.msa_e = QPlainTextEdit(self.misc_tab)
        self.mvthl_b1 = QHBoxLayout()
        self.mv_submit = QPushButton(self.misc_tab)
        self.mhl_5 = QHBoxLayout()
        self.mvs_label = QLabel(self.misc_tab)
        self.mvs_result = QPlainTextEdit(self.misc_tab)

        self.tabUtils.setObjectName('tabUtils')
        self.thl_bcp.setReadOnly(True)
        self.thl_bcl.setEnabled(False)
        self.thl_bcb.setEnabled(False)
        self.thl_bcb.setText('browse')
        self.ss_e.setReadOnly(True)
        self.ss_e.setMaximumHeight(65)
        self.vthl_bcl.setEnabled(False)
        self.vthl_bcb.setEnabled(False)
        self.vthl_bcb.setText('browse')
        self.vs_e.setMaximumHeight(65)
        self.m_select.addItem('Sha256', 'Sha256')
        self.m_select.addItem('dSha256', 'dSha256')
        self.m_select.addItem('Hash160', 'Hash160')
        self.m_select.addItem('int4byte', 'int4byte')
        self.m_select.addItem('int8byte', 'int8byte')
        self.m_select.addItem('Reverse', 'Reverse')

        self.wallet_combo.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_1.addLayout(self.wallet_combo)
        self.address_combo.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_1.addLayout(self.address_combo)
        self.verticalLayout_1.addWidget(self.thl_bcpl)
        self.verticalLayout_1.addWidget(self.thl_bcp)
        self.thl_a.addWidget(self.thl_ac)
        self.verticalLayout_1.addLayout(self.thl_a)
        self.hl_1a.addWidget(self.sm_e)
        self.verticalLayout_1.addLayout(self.hl_1a)
        self.thl_b.addWidget(self.thl_bc)
        self.verticalLayout_1.addLayout(self.thl_b)
        self.thl_b1.addWidget(self.thl_bcl)
        self.thl_b1.addWidget(self.thl_bcb)
        self.verticalLayout_1.addLayout(self.thl_b1)
        self.hl_2.addWidget(self.ss_label)
        self.hl_2.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_1.addLayout(self.hl_2)
        self.verticalLayout_1.addWidget(self.ss_e)
        self.hl_sb.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.hl_sb.addWidget(self.sbutton)
        self.verticalLayout_1.addLayout(self.hl_sb)
        self.verticalLayout_1.addItem(QSpacerItem(5, 5, _sp_min, _sp_exp))
        self.tabWidget_3.addTab(self.sign_tab, '')
        self.hl_3.addWidget(self.va_label)
        self.verticalLayout_2.addLayout(self.hl_3)
        self.verticalLayout_2.addWidget(self.va_e)
        self.vthl_a.addWidget(self.vthl_ac)
        self.verticalLayout_2.addLayout(self.vthl_a)
        self.hl_4a.addWidget(self.vm_e)
        self.verticalLayout_2.addLayout(self.hl_4a)
        self.vthl_b.addWidget(self.vthl_bc)
        self.verticalLayout_2.addLayout(self.vthl_b)
        self.vthl_b1.addWidget(self.vthl_bcl)
        self.vthl_b1.addWidget(self.vthl_bcb)
        self.verticalLayout_2.addLayout(self.vthl_b1)
        self.hl_5.addWidget(self.vs_label)
        self.hl_5.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_2.addLayout(self.hl_5)
        self.verticalLayout_2.addWidget(self.vs_e)
        self.hl_vb.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.hl_vb.addWidget(self.vbutton)
        self.verticalLayout_2.addLayout(self.hl_vb)
        self.hl_6.addWidget(self.success_label)
        self.verticalLayout_2.addLayout(self.hl_6)
        self.verticalLayout_2.addItem(QSpacerItem(5, 5, _sp_min, _sp_exp))
        self.tabWidget_3.addTab(self.verify_tab, '')
        self.mhl.addWidget(self.m_select_label)
        self.mhl.addWidget(self.m_select)
        self.mhl.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_3.addLayout(self.mhl)
        self.mhl_0.addWidget(self.msa_label)
        self.mhl_0.addWidget(self.mishex)
        self.mhl_0.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_3.addLayout(self.mhl_0)
        self.verticalLayout_3.addWidget(self.msa_e)
        self.mvthl_b1.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.mvthl_b1.addWidget(self.mv_submit)
        self.verticalLayout_3.addLayout(self.mvthl_b1)
        self.mhl_5.addWidget(self.mvs_label)
        self.mhl_5.addItem(QSpacerItem(5, 5, _sp_exp, _sp_min))
        self.verticalLayout_3.addLayout(self.mhl_5)
        self.verticalLayout_3.addWidget(self.mvs_result)
        self.tabWidget_3.addTab(self.misc_tab, '')
        self.verticalLayout_0.addWidget(self.tabWidget_3)

        self.thl_ac.setChecked(True)
        self.vthl_ac.setChecked(True)
        self.tabWidget_3.setTabVisible(2, False)

        self.tabWidget_3.setCurrentIndex(0)
        self.thl_ac.clicked.connect(self.sign_radio_clicked)
        self.thl_bc.clicked.connect(self.sign_radio_clicked)
        self.vthl_ac.clicked.connect(self.verify_radio_clicked)
        self.vthl_bc.clicked.connect(self.verify_radio_clicked)
        self.thl_bcb.clicked.connect(self.sign_file_browse)
        self.vthl_bcb.clicked.connect(self.verify_file_browse)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.thl_bcpl.setText(_translate('tabUtils', 'Public Key:'))
        self.thl_ac.setText(_translate('tabUtils', 'Message:'))
        self.thl_bc.setText(_translate('tabUtils', 'File:'))
        self.ss_label.setText(_translate('tabUtils', 'Signature:'))
        self.sbutton.setText(_translate('tabUtils', 'Sign'))
        self.va_label.setText(_translate('tabUtils', 'Public Key:'))
        self.vthl_ac.setText(_translate('tabUtils', 'Message:'))
        self.vthl_bc.setText(_translate('tabUtils', 'File:'))
        self.vs_label.setText(_translate('tabUtils', 'Signature:'))
        self.vbutton.setText(_translate('tabUtils', 'Verify'))
        self.m_select_label.setText(_translate('tabUtils', 'Function:'))
        self.msa_label.setText(_translate('tabUtils', 'Input:'))
        self.mishex.setText(_translate('tabUtils', 'isHex'))
        self.mv_submit.setText(_translate('tabUtils', 'Submit'))
        self.mvs_label.setText(_translate('tabUtils', 'Result:'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.sign_tab),
                                    _translate('tabUtils', 'Sign'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.verify_tab),
                                    _translate('tabUtils', 'Verify'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.misc_tab),
                                    _translate('tabUtils', 'Misc'))

    def sign_file_browse(self):
        self.thl_bcl.setText(self._file_browse()[0])

    def verify_file_browse(self):
        self.vthl_bcl.setText(self._file_browse()[0])

    def _file_browse(self):
        return QFileDialog.getOpenFileName()

    def sign_radio_clicked(self, _checked):
        if self.thl_ac.isChecked() is True:
            self.sm_e.setEnabled(True)
            self.thl_bcl.setEnabled(False)
            self.thl_bcb.setEnabled(False)
        elif self.thl_bc.isChecked() is True:
            self.sm_e.setEnabled(False)
            self.thl_bcl.setEnabled(True)
            self.thl_bcb.setEnabled(True)

    def verify_radio_clicked(self, _checked):
        if self.vthl_ac.isChecked() is True:
            self.vm_e.setEnabled(True)
            self.vthl_bcl.setEnabled(False)
            self.vthl_bcb.setEnabled(False)
        elif self.vthl_bc.isChecked() is True:
            self.vm_e.setEnabled(False)
            self.vthl_bcl.setEnabled(True)
            self.vthl_bcb.setEnabled(True)
