from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout,
                             QLabel, QSpacerItem, QSizePolicy, QPushButton,
                             QLineEdit, QCheckBox, QPlainTextEdit, QTabWidget)

from core.kui.ux.widgets.widgets import _ns_value_textedit
from core.kui.ux.widgets.electrumx_peers_table import _electrumx_peers_table
from core.kui.ux.widgets.ipfs_gateways_table import _ipfs_gateways_table


class Ui_SettingsTab(QObject):
    def setupUi(self):
        _al_center = QtCore.Qt.AlignmentFlag.AlignCenter
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum
        _sp_minExp = QSizePolicy.Policy.MinimumExpanding

        self.tabSettings = QWidget()
        self.verticalLayout_13 = QVBoxLayout(self.tabSettings)
        self.tabWidget_3 = QTabWidget()
        self.settings_tab_wallet = QWidget(self.tabSettings)
        self.verticalLayout_12 = QVBoxLayout(self.settings_tab_wallet)
        self.path_meta_hl = QHBoxLayout()
        self.path_meta_l = QLabel(self.tabSettings)
        self.path_meta_e = QPlainTextEdit(self.settings_tab_wallet)
        self.syncBox = QLabel(self.settings_tab_wallet)
        self.s_a_wallet = QCheckBox(self.settings_tab_wallet)
        self.s_timer_wallet_hl = QHBoxLayout()
        self.s_t_wallet_l = QCheckBox(self.settings_tab_wallet)
        self.s_t_wallet_e = QLineEdit(self.settings_tab_wallet)
        self.stwe_v = QIntValidator(self.s_t_wallet_e)
        self.s_a_df = QCheckBox(self.settings_tab_wallet)
        self.s_timer_df_hl = QHBoxLayout()
        self.s_t_df_l = QCheckBox(self.settings_tab_wallet)
        self.s_t_df_e = QLineEdit(self.settings_tab_wallet)
        self.stde_v = QIntValidator(self.s_t_df_e)
        self.s_a_fav = QCheckBox(self.settings_tab_wallet)
        self.s_timer_favorites_hl = QHBoxLayout()
        self.s_t_fav_l = QCheckBox(self.settings_tab_wallet)
        self.s_t_fav_e = QLineEdit(self.settings_tab_wallet)
        self.stfe_v = QIntValidator(self.s_t_fav_e)
        self.datafeedBox = QHBoxLayout()
        self.label_3 = QLabel(self.settings_tab_wallet)
        self.lineEdit_2 = QLineEdit(self.settings_tab_wallet)
        self.settings_tab_debug = QWidget(self.settings_tab_wallet)
        self.verticalLayout_9 = QVBoxLayout(self.settings_tab_debug)
        self.horizontalLayout_11 = QHBoxLayout()
        self.settings_elxp_label = QLabel(self.settings_tab_wallet)
        self.elxp_btn_add = QPushButton(self.settings_tab_wallet)
        self.elxp_tbl = _electrumx_peers_table('selxp_table',
                                               self.settings_tab_wallet)
        self.settings_debug_text = _ns_value_textedit('selxp_table_2',
                                                      self.settings_tab_debug)
        self.horizontalLayout_12 = QHBoxLayout()
        self.label = QLabel(self.settings_tab_wallet)
        self.line_0 = QFrame(self.settings_tab_wallet)
        self.line_1 = QFrame(self.settings_tab_wallet)
        self.line_2 = QFrame(self.settings_tab_wallet)
        self.horizontalLayout_13 = QHBoxLayout()
        self.settings_ipfs_button_add = QPushButton(self.settings_tab_wallet)
        self.ipfs_tbl = _ipfs_gateways_table('ipfs_tbl',
                                             self.settings_tab_wallet)
        self.settings_tab_datafeeds = QWidget(self.settings_tab_wallet)
        self.settings_tab_df_vl = QVBoxLayout(self.settings_tab_datafeeds)

        self.tabSettings.setObjectName('tabSettings')
        self.path_meta_e.setReadOnly(True)
        self.path_meta_e.setMaximumHeight(26)
        self.path_meta_e.setFrameStyle(QFrame.Shape.NoFrame)
        self.s_a_wallet.setChecked(True)
        self.s_t_wallet_e.setValidator(self.stwe_v)
        self.s_t_wallet_e.setMaximumWidth(50)
        self.s_t_wallet_e.setAlignment(_al_center)
        self.s_a_df.setChecked(True)
        self.s_t_df_e.setValidator(self.stde_v)
        self.s_t_df_e.setMaximumWidth(50)
        self.s_t_df_e.setAlignment(_al_center)
        self.s_a_fav.setChecked(True)
        self.s_t_fav_e.setValidator(self.stfe_v)
        self.s_t_fav_e.setMaximumWidth(50)
        self.s_t_fav_e.setAlignment(_al_center)
        self.line_0.setFrameShape(QFrame.Shape.HLine)
        self.line_0.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.path_meta_hl.addWidget(self.path_meta_l)
        self.path_meta_hl.addWidget(self.path_meta_e)
        self.verticalLayout_12.addLayout(self.path_meta_hl)
        self.verticalLayout_12.addWidget(self.syncBox)
        self.s_timer_wallet_hl.addWidget(self.s_a_wallet)
        self.s_timer_wallet_hl.addWidget(self.s_t_wallet_l)
        self.s_timer_wallet_hl.addWidget(self.s_t_wallet_e)
        self.s_timer_wallet_hl.addItem(QSpacerItem(5, 5,
                                       _sp_minExp, _sp_minExp))
        self.verticalLayout_12.addLayout(self.s_timer_wallet_hl)
        self.s_timer_df_hl.addWidget(self.s_a_df)
        self.s_timer_df_hl.addWidget(self.s_t_df_l)
        self.s_timer_df_hl.addWidget(self.s_t_df_e)
        self.s_timer_df_hl.addItem(QSpacerItem(5, 5,
                                   _sp_minExp, _sp_minExp))
        self.verticalLayout_12.addLayout(self.s_timer_df_hl)
        self.s_timer_favorites_hl.addWidget(self.s_a_fav)
        self.s_timer_favorites_hl.addWidget(self.s_t_fav_l)
        self.s_timer_favorites_hl.addWidget(self.s_t_fav_e)
        self.s_timer_favorites_hl.addItem(QSpacerItem(5, 5,
                                          _sp_minExp, _sp_minExp))
        self.verticalLayout_12.addLayout(self.s_timer_favorites_hl)
        self.verticalLayout_12.addWidget(self.line_0)
        self.verticalLayout_12.addLayout(self.datafeedBox)
        self.verticalLayout_12.addWidget(self.line_1)
        self.datafeedBox.addWidget(self.label_3)
        self.datafeedBox.addWidget(self.lineEdit_2)
        self.horizontalLayout_11.addWidget(self.settings_elxp_label)
        self.horizontalLayout_11.addItem(QSpacerItem(253, 20,
                                         _sp_exp, _sp_min))
        self.horizontalLayout_11.addWidget(self.elxp_btn_add)
        self.verticalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_12.addWidget(self.elxp_tbl)
        self.verticalLayout_9.addWidget(self.settings_debug_text)
        self.horizontalLayout_13.addWidget(self.label)
        self.verticalLayout_12.addWidget(self.line_2)
        self.horizontalLayout_13.addItem(QSpacerItem(253, 20,
                                         _sp_exp, _sp_min))
        self.horizontalLayout_13.addWidget(self.settings_ipfs_button_add)
        self.verticalLayout_12.addLayout(self.horizontalLayout_13)
        self.verticalLayout_12.addWidget(self.ipfs_tbl)
        self.verticalLayout_12.addItem(QSpacerItem(20, 20, _sp_min, _sp_exp))
        self.tabWidget_3.addTab(self.settings_tab_wallet, '')
        self.tabWidget_3.addTab(self.settings_tab_debug, '')
        self.tabWidget_3.setCurrentIndex(0)
        self.verticalLayout_13.addWidget(self.tabWidget_3)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.path_meta_l.setText(_translate('tabSettings', 'Path:'))
        self.syncBox.setText(_translate('tabSettings', 'Sync Options:'))
        self.s_a_wallet.setText(_translate('tabSettings',
                                           'Sync wallets on startup,'))
        self.s_a_df.setText(_translate('tabSettings',
                                       'Sync data feeds on startup,'))
        self.s_a_fav.setText(_translate('tabSettings',
                                        'Sync favorites on startup,'))
        self.s_t_wallet_l.setText(_translate('tabSettings', 'on timer'))
        self.s_t_df_l.setText(_translate('tabSettings', 'on timer'))
        self.s_t_fav_l.setText(_translate('tabSettings', 'on timer'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.settings_tab_wallet),
                                    _translate('tabSettings', 'General'))
        self.settings_elxp_label.setText(_translate('tabSettings',
                                         'ElectrumX Peers'))
        self.elxp_btn_add.setText(_translate('tabSettings', 'Add'))
        self.tabWidget_3.setTabText(self.tabWidget_3
                                    .indexOf(self.settings_tab_debug),
                                    _translate('tabSettings', 'Debug'))
        self.label.setText(_translate('tabSettings', 'IPFS Gateways'))
        self.settings_ipfs_button_add.setText(_translate('tabSettings', 'Add'))
        self.label_3.setText(_translate('tabSettings', 'NFT Market Data'))
