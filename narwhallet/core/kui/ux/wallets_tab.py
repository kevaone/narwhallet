from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout,
                             QLabel, QSpacerItem, QSizePolicy, QPushButton,
                             QPlainTextEdit, QScrollArea, QSplitter,
                             QTabWidget)
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.widgets import (_transaction_table,
                                            _wallets_addr_tbl,
                                            _wallets_table)
from narwhallet.core.kcl.wallet.wallet import MWallet


class Ui_WalletTab(QObject):
    def setupUi(self):
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum
        _sp_minexp = QSizePolicy.Policy.MinimumExpanding
        _transm_st = QtCore.Qt.TransformationMode.SmoothTransformation

        self.tabWallets = QWidget()
        self.verticalLayout_3 = QVBoxLayout(self.tabWallets)
        self.frame_3 = QFrame(self.tabWallets)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.btn_send = QPushButton(self.frame_3)
        self.btn_create = QPushButton(self.frame_3)
        self.btn_restore = QPushButton(self.frame_3)
        self.btn_watch = QPushButton(self.frame_3)
        self.tbl_w = _wallets_table('tbl_w', self.tabWallets)
        self.tabWidget_2 = QTabWidget(self.tabWallets)
        self.tabTransactions = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.tabTransactions)
        self.tbl_tx = _transaction_table('tbl_tx', self.tabTransactions)
        self.tabAddresses = QWidget()
        self.verticalLayout_5 = QVBoxLayout(self.tabAddresses)
        self.frame_4 = QFrame(self.tabAddresses)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.btn_watch_addr = QPushButton(self.frame_4)
        self.btn_addr = QPushButton(self.frame_4)
        self.tbl_addr = _wallets_addr_tbl('tbl_addr', self.tabAddresses)
        self.tabIntAddresses = QWidget()
        self.verticalLayout_7 = QVBoxLayout(self.tabIntAddresses)
        self.frame_7 = QFrame(self.tabIntAddresses)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_7)
        self.btn_addr2 = QPushButton(self.frame_7)
        self.tbl_addr2 = _wallets_addr_tbl('tbl_addr',
                                           self.tabIntAddresses)
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self._bpic = QPixmap(MShared.get_resource_path('clipboard.png'))
        self._bpic = self._bpic.scaledToWidth(20, _transm_st)
        self.tabWalletSettings = QWidget()
        self.root_vl = QVBoxLayout(self.tabWalletSettings)
        self.frame_info = QFrame(self.tabWalletSettings)
        self.frame_vl = QVBoxLayout(self.frame_info)
        self.hl0 = QHBoxLayout()
        self.lwname = QLabel(self.frame_info)
        self.wname = QLabel(self.frame_info)
        self.hl1 = QHBoxLayout()
        self.hl1a = QHBoxLayout()
        self.lwmnemonic = QLabel(self.frame_info)
        self.llwmnemonic = QPushButton(self.frame_info)
        self.cpmnemonic = QPushButton(self.frame_info)
        self.wmnemonic = QPlainTextEdit(self.frame_info)
        self.hl2 = QHBoxLayout()
        self.hl2a = QHBoxLayout()
        self.lwseed = QLabel(self.frame_info)
        self.llwseed = QPushButton(self.frame_info)
        self.cpseed = QPushButton(self.frame_info)
        self.wseed = QPlainTextEdit(self.frame_info)
        self.hl14 = QHBoxLayout()
        self.hl14a = QHBoxLayout()
        self.lxprv = QLabel(self.frame_info)
        self.llxprv = QPushButton(self.frame_info)
        self.cpxprv = QPushButton(self.frame_info)
        self.wxprv = QPlainTextEdit(self.frame_info)
        self.hl15 = QHBoxLayout()
        self.hl15a = QHBoxLayout()
        self.lxpub = QLabel(self.frame_info)
        self.llxpub = QPushButton(self.frame_info)
        self.cpxpub = QPushButton(self.frame_info)
        self.wxpub = QPlainTextEdit(self.frame_info)
        self.hl3 = QHBoxLayout()
        self.lwcoin = QLabel(self.frame_info)
        self.wcoin = QLabel(self.frame_info)
        # self.hl4 = QHBoxLayout()
        # self.lwbip = QLabel(self.frame_info)
        # self.wbip = QLabel(self.frame_info)
        self.hl5 = QHBoxLayout()
        self.lwkind = QLabel(self.frame_info)
        self.wkind = QLabel(self.frame_info)
        self.hl6 = QHBoxLayout()
        self.lwaccount_index = QLabel(self.frame_info)
        self.waccount_index = QLabel(self.frame_info)
        self.hl7 = QHBoxLayout()
        self.lwchange_index = QLabel(self.frame_info)
        self.wchange_index = QLabel(self.frame_info)
        self.hl8 = QHBoxLayout()
        self.lwbalance = QLabel(self.frame_info)
        self.wbalance = QLabel(self.frame_info)
        self.hl9 = QHBoxLayout()
        self.lwlocked = QLabel(self.frame_info)
        self.wlocked = QLabel(self.frame_info)
        self.hl10 = QHBoxLayout()
        self.lwlast_updated = QLabel(self.frame_info)
        self.wlast_updated = QLabel(self.frame_info)
        self.info_scroll = QScrollArea(self.tabWalletSettings)
        splitter_main = QSplitter(QtCore.Qt.Orientation.Vertical)

        self.tabWallets.setObjectName('tabWallets')
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.btn_watch_addr.setVisible(False)
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.frame_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Shadow.Raised)
        self.wmnemonic.setMaximumHeight(65)
        self.wmnemonic.setVisible(False)
        self.wmnemonic.setReadOnly(True)
        self.cpmnemonic.setVisible(False)
        self.cpmnemonic.setIcon(QIcon(self._bpic))
        self.cpmnemonic.setFlat(True)
        self.cpmnemonic.setToolTip('Copy Mnemonic to Clipboard')
        self.llwmnemonic.setIcon(QIcon(self._ppic))
        self.llwmnemonic.setFlat(True)
        self.llwmnemonic.setToolTip('Show Mnemonic')
        self.wseed.setMaximumHeight(65)
        self.wseed.setVisible(False)
        self.wseed.setReadOnly(True)
        self.cpseed.setVisible(False)
        self.cpseed.setIcon(QIcon(self._bpic))
        self.cpseed.setFlat(True)
        self.cpseed.setToolTip('Copy Seed to Clipboard')
        self.llwseed.setIcon(QIcon(self._ppic))
        self.llwseed.setFlat(True)
        self.llwseed.setToolTip('Show Seed')
        self.wxprv.setMaximumHeight(65)
        self.wxprv.setVisible(False)
        self.wxprv.setReadOnly(True)
        self.cpxprv.setVisible(False)
        self.cpxprv.setIcon(QIcon(self._bpic))
        self.cpxprv.setFlat(True)
        self.cpxprv.setToolTip('Copy xprv to Clipboard')
        self.llxprv.setIcon(QIcon(self._ppic))
        self.llxprv.setFlat(True)
        self.llxprv.setToolTip('Show xprv')
        self.wxpub.setMaximumHeight(65)
        self.wxpub.setVisible(False)
        self.wxpub.setReadOnly(True)
        self.cpxpub.setVisible(False)
        self.cpxpub.setIcon(QIcon(self._bpic))
        self.cpxpub.setFlat(True)
        self.cpxprv.setToolTip('Copy xpub to Clipboard')
        self.llxpub.setIcon(QIcon(self._ppic))
        self.llxpub.setFlat(True)
        self.llxpub.setToolTip('Show xpub')
        self.info_scroll.setWidget(self.frame_info)
        self.info_scroll.setWidgetResizable(True)
        splitter_main.setStretchFactor(1, 1)

        self.horizontalLayout_3.addWidget(self.btn_send)
        self.horizontalLayout_3.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.horizontalLayout_3.addWidget(self.btn_create)
        self.horizontalLayout_3.addWidget(self.btn_restore)
        self.horizontalLayout_3.addWidget(self.btn_watch)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.verticalLayout_4.addWidget(self.tbl_tx)
        self.tabWidget_2.addTab(self.tabTransactions, '')
        self.horizontalLayout_4.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.horizontalLayout_4.addWidget(self.btn_watch_addr)
        self.horizontalLayout_4.addWidget(self.btn_addr)
        self.verticalLayout_5.addWidget(self.tbl_addr)
        self.verticalLayout_5.addWidget(self.frame_4)
        self.tabWidget_2.addTab(self.tabAddresses, '')
        self.horizontalLayout_7.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.horizontalLayout_7.addWidget(self.btn_addr2)
        self.verticalLayout_7.addWidget(self.tbl_addr2)
        self.verticalLayout_7.addWidget(self.frame_7)
        self.tabWidget_2.addTab(self.tabIntAddresses, '')
        self.tabWidget_2.addTab(self.tabWalletSettings, '')
        self.hl0.addWidget(self.lwname)
        self.hl0.addWidget(self.wname)
        self.hl0.addItem(QSpacerItem(0, 0, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl0)
        self.hl1.addWidget(self.lwmnemonic)
        self.hl1.addWidget(self.llwmnemonic)
        self.hl1.addItem(QSpacerItem(0, 0, _sp_minexp, _sp_min))
        self.frame_vl.addLayout(self.hl1)
        self.hl1a.addWidget(self.cpmnemonic)
        self.hl1a.addWidget(self.wmnemonic)
        self.frame_vl.addLayout(self.hl1a)
        self.hl2.addWidget(self.lwseed)
        self.hl2.addWidget(self.llwseed)
        self.hl2.addItem(QSpacerItem(0, 0, _sp_minexp, _sp_min))
        self.frame_vl.addLayout(self.hl2)
        self.hl2a.addWidget(self.cpseed)
        self.hl2a.addWidget(self.wseed)
        self.frame_vl.addLayout(self.hl2a)

        self.hl14.addWidget(self.lxprv)
        self.hl14.addWidget(self.llxprv)
        self.hl14.addItem(QSpacerItem(0, 0, _sp_minexp, _sp_min))
        self.frame_vl.addLayout(self.hl14)
        self.hl14a.addWidget(self.cpxprv)
        self.hl14a.addWidget(self.wxprv)
        self.frame_vl.addLayout(self.hl14a)
        self.hl15.addWidget(self.lxpub)
        self.hl15.addWidget(self.llxpub)
        self.hl15.addItem(QSpacerItem(0, 0, _sp_minexp, _sp_min))
        self.frame_vl.addLayout(self.hl15)
        self.hl15a.addWidget(self.cpxpub)
        self.hl15a.addWidget(self.wxpub)
        self.frame_vl.addLayout(self.hl15a)
        self.hl3.addWidget(self.lwcoin)
        self.hl3.addWidget(self.wcoin)
        self.hl3.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl3)
        # self.hl4.addWidget(self.lwbip)
        # self.hl4.addWidget(self.wbip)
        # self.hl4.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        # self.frame_vl.addLayout(self.hl4)
        self.hl5.addWidget(self.lwkind)
        self.hl5.addWidget(self.wkind)
        self.hl5.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl5)
        self.hl6.addWidget(self.lwaccount_index)
        self.hl6.addWidget(self.waccount_index)
        self.hl6.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl6)
        self.hl7.addWidget(self.lwchange_index)
        self.hl7.addWidget(self.wchange_index)
        self.hl7.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl7)
        self.hl8.addWidget(self.lwbalance)
        self.hl8.addWidget(self.wbalance)
        self.hl8.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl8)
        self.hl9.addWidget(self.lwlocked)
        self.hl9.addWidget(self.wlocked)
        self.hl9.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl9)
        self.hl10.addWidget(self.lwlast_updated)
        self.hl10.addWidget(self.wlast_updated)
        self.hl10.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.frame_vl.addLayout(self.hl10)
        self.frame_vl.addItem(QSpacerItem(5, 5, _sp_min, _sp_exp))

        self.root_vl.addWidget(self.info_scroll)
        splitter_main.addWidget(self.tbl_w)
        splitter_main.addWidget(self.tabWidget_2)
        splitter_main.setSizes([250, 350])
        self.verticalLayout_3.addWidget(splitter_main)

        self.tabWidget_2.setCurrentIndex(0)
        self.llwmnemonic.clicked.connect(self._display_mnemonic)
        self.llwseed.clicked.connect(self._display_seed)
        self.llxprv.clicked.connect(self._display_xprv)
        self.llxpub.clicked.connect(self._display_xpub)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.btn_send.setText(_translate('tabWallets', 'Send'))
        self.btn_create.setText(_translate('tabWallets',
                                           'Create'))
        self.btn_restore.setText(_translate('tabWallets',
                                            'Restore'))
        self.btn_watch.setText(_translate('tabWallets', 'W/O'))
        self.tabWidget_2.setTabText(self.tabWidget_2
                                    .indexOf(self.tabTransactions),
                                    _translate('tabWallets', 'Transactions'))
        self.btn_watch_addr.setText(_translate('tabWallets',
                                               'Add Address'))
        self.btn_addr.setText(_translate('tabWallets',
                                         'Increase Pool'))
        self.btn_addr2.setText(_translate('tabWallets',
                                          'Increase Pool'))
        self.tabWidget_2.setTabText(self.tabWidget_2
                                    .indexOf(self.tabIntAddresses),
                                    _translate('tabWallets', 'Change'))
        self.tabWidget_2.setTabText(self.tabWidget_2
                                    .indexOf(self.tabAddresses),
                                    _translate('tabWallets', 'Addresses'))
        self.tabWidget_2.setTabText(self.tabWidget_2
                                    .indexOf(self.tabWalletSettings),
                                    _translate('tabWallets', 'Info'))
        self.lwname.setText(_translate('tabWallets', 'Name:'))
        self.lwmnemonic.setText(_translate('tabWallets', 'Mnemonic:'))
        self.lwseed.setText(_translate('tabWallets', 'Seed:'))
        self.lxprv.setText(_translate('tabWallets', 'xprv:'))
        self.lxpub.setText(_translate('tabWallets', 'xpub:'))
        self.lwcoin.setText(_translate('tabWallets', 'Coin:'))
        self.lwkind.setText(_translate('tabWallets', 'Kind:'))
        # self.lwbip.setText(_translate('tabWallets', 'BIP:'))
        self.lwaccount_index.setText(_translate('tabWallets',
                                     'Account Index:'))
        self.lwchange_index.setText(_translate('tabWallets', 'Change Index:'))
        self.lwbalance.setText(_translate('tabWallets', 'Balance:'))
        self.lwlocked.setText(_translate('tabWallets', 'Locked:'))
        self.lwlast_updated.setText(_translate('tabWallets', 'Last Updated:'))

    def _display_mnemonic(self, _event):
        if self.wmnemonic.isVisible() is True:
            self.wmnemonic.setVisible(False)
            self.cpmnemonic.setVisible(False)
            self.llwmnemonic.setIcon(QIcon(self._ppic))
            self.llwmnemonic.setToolTip('Show Mnemonic')
        else:
            self.wmnemonic.setVisible(True)
            self.cpmnemonic.setVisible(True)
            self.llwmnemonic.setIcon(QIcon(self._mpic))
            self.llwmnemonic.setToolTip('Hide Mnemonic')

    def _display_seed(self, _event):
        if self.wseed.isVisible() is True:
            self.wseed.setVisible(False)
            self.cpseed.setVisible(False)
            self.llwseed.setIcon(QIcon(self._ppic))
            self.llwseed.setToolTip('Show Seed')
        else:
            self.wseed.setVisible(True)
            self.cpseed.setVisible(True)
            self.llwseed.setIcon(QIcon(self._mpic))
            self.llwseed.setToolTip('Hide Seed')

    def _display_xprv(self, _event):
        if self.wxprv.isVisible() is True:
            self.wxprv.setVisible(False)
            self.cpxprv.setVisible(False)
            self.llxprv.setIcon(QIcon(self._ppic))
            self.llxprv.setToolTip('Show xprv')
        else:
            self.wxprv.setVisible(True)
            self.cpxprv.setVisible(True)
            self.llxprv.setIcon(QIcon(self._mpic))
            self.llxprv.setToolTip('Hide xrpv')

    def _display_xpub(self, _event):
        if self.wxpub.isVisible() is True:
            self.wxpub.setVisible(False)
            self.cpxpub.setVisible(False)
            self.llxpub.setIcon(QIcon(self._ppic))
            (self.llxpub
             .setToolTip(self.llxpub.toolTip().replace('Hide', 'Show')))
        else:
            self.wxpub.setVisible(True)
            self.cpxpub.setVisible(True)
            self.llxpub.setIcon(QIcon(self._mpic))
            (self.llxpub
             .setToolTip(self.llxpub.toolTip().replace('Show', 'Hide')))

    def set_info_values(self, wallet: MWallet):
        self.wname.setText(wallet.name)
        if wallet.mnemonic == '':
            self.lwmnemonic.setVisible(False)
            self.llwmnemonic.setVisible(False)
            self.wmnemonic.setVisible(False)
            self.cpmnemonic.setVisible(False)
            self.wmnemonic.setPlainText('')
        else:
            self.lwmnemonic.setVisible(True)
            self.llwmnemonic.setVisible(True)
            self.wmnemonic.setVisible(False)
            self.cpmnemonic.setVisible(False)
            self.llwmnemonic.setIcon(QIcon(self._ppic))
            self.wmnemonic.setPlainText(wallet.mnemonic)

        if wallet.seed == '':
            self.llwseed.setVisible(False)
            self.lwseed.setVisible(False)
            self.wseed.setVisible(False)
            self.cpseed.setVisible(False)
            self.wseed.setPlainText('')
        else:
            self.llwseed.setVisible(True)
            self.lwseed.setVisible(True)
            self.wseed.setVisible(False)
            self.cpseed.setVisible(False)
            self.llwseed.setIcon(QIcon(self._ppic))
            self.wseed.setPlainText(wallet.seed)

        wallet.generate_extended_prv()
        if wallet.extended_prv == '':
            self.llxprv.setVisible(False)
            self.lxprv.setVisible(False)
            self.wxprv.setVisible(False)
            self.cpxprv.setVisible(False)
            self.wxprv.setPlainText('')
        else:
            self.llxprv.setVisible(True)
            self.lxprv.setVisible(True)
            self.wxprv.setVisible(False)
            self.cpxprv.setVisible(False)
            self.llxprv.setIcon(QIcon(self._ppic))
            self.wxprv.setPlainText(wallet.extended_prv)

        wallet.generate_extended_pub()
        self.wxpub.setPlainText(wallet.extended_pub)
        if wallet.bip == 'bip49':
            self.lxpub.setText('ypub')
            self.cpxpub.setToolTip('Copy ypub to Clipboard')
            self.llxpub.setToolTip('Show ypub')

        self.wcoin.setText(wallet.coin)

        self.wkind.setText(wallet.kind.name)

        if wallet.kind == 3:
            self.btn_watch_addr.setVisible(True)
            self.btn_addr.setVisible(False)
            self.btn_addr2.setVisible(False)
            self.llxpub.setVisible(False)
            self.lxpub.setVisible(False)
            self.cpxpub.setVisible(False)
            self.wxpub.setVisible(False)
        else:
            self.llxpub.setIcon(QIcon(self._ppic))
            self.btn_watch_addr.setVisible(False)
            self.btn_addr.setVisible(True)
            self.btn_addr2.setVisible(True)
            self.llxpub.setVisible(True)
            self.lxpub.setVisible(True)
            self.cpxpub.setVisible(False)
            self.wxpub.setVisible(False)

        # self.wbip.setText(wallet.bip)
        self.waccount_index.setText(str(wallet.account_index))
        self.wchange_index.setText(str(wallet.change_index))
        self.wbalance.setText(str(wallet.balance))

        if wallet.locked is not False:
            self.wlocked.setText(str(wallet.locked))
        else:
            self.wlocked.setText('False')

        if wallet.last_updated != 0.0:
            (self.wlast_updated.setText(
                MShared.get_timestamp(wallet.last_updated)[1]))

    def reset_info_values(self):
        self.wname.setText('')
        self.lwmnemonic.setVisible(False)
        self.llwmnemonic.setVisible(False)
        self.wmnemonic.setVisible(False)
        self.cpmnemonic.setVisible(False)
        self.wmnemonic.setPlainText('')
        self.llwseed.setVisible(False)
        self.lwseed.setVisible(False)
        self.wseed.setVisible(False)
        self.cpseed.setVisible(False)
        self.wseed.setPlainText('')
        self.llxprv.setVisible(False)
        self.lxprv.setVisible(False)
        self.wxprv.setVisible(False)
        self.cpxprv.setVisible(False)
        self.wxpub.setPlainText('')
        self.wxprv.setPlainText('')
        self.lxpub.setText('ypub')
        self.wcoin.setText('')
        self.wkind.setText('')
        self.btn_watch_addr.setVisible(False)
        self.btn_addr.setVisible(False)
        self.btn_addr2.setVisible(False)
        # self.wbip.setText('')
        self.waccount_index.setText('')
        self.wchange_index.setText('')
        self.wbalance.setText('')
        self.wlocked.setText('False')
        self.wlast_updated.setText('')
