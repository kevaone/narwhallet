from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame,
                             QHBoxLayout, QLabel, QSpacerItem,
                             QSizePolicy, QPushButton, QLineEdit,
                             QCheckBox, QPlainTextEdit, QTabWidget)
from narwhallet.core.kui.ux.widgets import (_electrumx_peers_table,
                                            _ns_value_textedit)


class Ui_SettingsTab(QObject):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignmentFlag.AlignCenter
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum
        _sp_minexp = QSizePolicy.Policy.MinimumExpanding

        self.tabSettings = QWidget()
        self.verticalLayout_13 = QVBoxLayout(self.tabSettings)
        self.tabWidget_3 = QTabWidget()
        self.settings_tab_wallet = QWidget(self.tabSettings)
        self.verticalLayout_12 = QVBoxLayout(self.settings_tab_wallet)
        self.path_meta_hl = QHBoxLayout()
        self.path_meta_l = QLabel(self.settings_tab_wallet)
        self.path_meta_e = QPlainTextEdit(self.settings_tab_wallet)
        self.reset_cache = QPushButton(self.settings_tab_wallet)
        self.auto_lock_hl = QHBoxLayout()
        self.auto_lock_l = QLabel(self.settings_tab_wallet)
        self.auto_lock_e = QLineEdit(self.settings_tab_wallet)
        self.auto_lock_v = QIntValidator(self.auto_lock_e)
        self.show_change = QCheckBox(self.settings_tab_wallet)
        self.s_a_wallet = QCheckBox(self.settings_tab_wallet)
        self.s_timer_wallet_hl = QHBoxLayout()
        self.s_t_wallet_l = QCheckBox(self.settings_tab_wallet)
        self.s_t_wallet_e = QLineEdit(self.settings_tab_wallet)
        self.stwe_v = QIntValidator(self.s_t_wallet_e)
        self.settings_tab_about = QWidget(self.settings_tab_wallet)
        self.verticalLayout_9 = QVBoxLayout(self.settings_tab_about)
        self.horizontalLayout_11 = QHBoxLayout()
        self.settings_elxp_label = QLabel(self.settings_tab_wallet)
        self.elxp_btn_add = QPushButton(self.settings_tab_wallet)
        self.elxp_tbl = _electrumx_peers_table('selxp_table',
                                               self.settings_tab_wallet)
        self.settings_about_text = _ns_value_textedit('selxp_table_2',
                                                      self.settings_tab_about)
        self.line_1 = QFrame(self.settings_tab_wallet)

        self.tabSettings.setObjectName('tabSettings')
        self.path_meta_e.setReadOnly(True)
        self.path_meta_e.setMaximumHeight(28)
        self.path_meta_e.setFrameStyle(QFrame.Shape.NoFrame)
        self.auto_lock_e.setValidator(self.auto_lock_v)
        self.auto_lock_e.setMaximumWidth(50)
        self.auto_lock_e.setAlignment(_al_center)
        self.s_a_wallet.setChecked(True)
        self.s_t_wallet_e.setValidator(self.stwe_v)
        self.s_t_wallet_e.setMaximumWidth(50)
        self.s_t_wallet_e.setAlignment(_al_center)
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.path_meta_hl.addWidget(self.path_meta_l)
        self.path_meta_hl.addWidget(self.path_meta_e)
        self.path_meta_hl.addWidget(self.reset_cache)
        self.path_meta_hl.addItem(QSpacerItem(5, 25, _sp_min, _sp_min))
        self.verticalLayout_12.addLayout(self.path_meta_hl)
        self.auto_lock_hl.addWidget(self.auto_lock_l)
        self.auto_lock_hl.addWidget(self.auto_lock_e)
        self.auto_lock_hl.addItem(QSpacerItem(5, 35, _sp_minexp, _sp_min))
        self.verticalLayout_12.addLayout(self.auto_lock_hl)
        self.verticalLayout_12.addWidget(self.show_change)
        self.s_timer_wallet_hl.addWidget(self.s_a_wallet)
        self.s_timer_wallet_hl.addWidget(self.s_t_wallet_l)
        self.s_timer_wallet_hl.addWidget(self.s_t_wallet_e)
        self.s_timer_wallet_hl.addItem(QSpacerItem(5, 25,
                                       _sp_minexp, _sp_min))
        self.verticalLayout_12.addLayout(self.s_timer_wallet_hl)
        self.verticalLayout_12.addWidget(self.line_1)
        self.horizontalLayout_11.addWidget(self.settings_elxp_label)
        self.horizontalLayout_11.addItem(QSpacerItem(253, 20,
                                         _sp_exp, _sp_min))
        self.horizontalLayout_11.addWidget(self.elxp_btn_add)
        self.verticalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_12.addWidget(self.elxp_tbl)
        self.verticalLayout_9.addWidget(self.settings_about_text)
        self.verticalLayout_12.addItem(QSpacerItem(20, 20, _sp_min, _sp_exp))
        self.tabWidget_3.addTab(self.settings_tab_wallet, '')
        self.tabWidget_3.addTab(self.settings_tab_about, '')
        self.tabWidget_3.setCurrentIndex(0)
        self.verticalLayout_13.addWidget(self.tabWidget_3)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.path_meta_l.setText(_translate('tabSettings', 'Path:'))
        self.reset_cache.setText(_translate('tabSettings', 'Reset Cache'))
        (self.auto_lock_l
         .setText(_translate('tabSettings', 'Wallet Auto Lock Timer')))
        (self.show_change
         .setText(_translate('tabSettings', 'Show Change Addresses')))
        self.s_a_wallet.setText(_translate('tabSettings',
                                           'Sync wallets on startup,'))
        self.s_t_wallet_l.setText(_translate('tabSettings', 'on timer'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.settings_tab_wallet),
                                    _translate('tabSettings', 'General'))
        self.settings_elxp_label.setText(_translate('tabSettings',
                                         'ElectrumX Peers -'))
        self.elxp_btn_add.setText(_translate('tabSettings', 'Add'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.settings_tab_about),
                                    _translate('tabSettings', 'About'))
