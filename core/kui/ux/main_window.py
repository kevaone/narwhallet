from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QSizePolicy, QTabWidget, QMenuBar, QStatusBar)

from core.kui.ux.wallets_tab import Ui_WalletTab
from core.kui.ux.address_book_tab import Ui_AddressBookTab
from core.kui.ux.namespaces_tab import Ui_NamespacesTab
from core.kui.ux.nft_tab import Ui_NFTTab
from core.kui.ux.settings_tab import Ui_SettingsTab
from core.kui.ux.utils_tab import Ui_UtilsTab


class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow: QMainWindow):
        # MainWindow.setObjectName('MainWindow')
        # MainWindow.resize(858, 806)
        # MainWindow.setWindowTitle('Narwhallet')
        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.tabWidget = QTabWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        self.w_tab = Ui_WalletTab()
        self.ns_tab = Ui_NamespacesTab()
        self.nft_tab = Ui_NFTTab()
        self.ab_tab = Ui_AddressBookTab()
        self.u_tab = Ui_UtilsTab()
        self.settings_tab = Ui_SettingsTab()
        self.menubar = QMenuBar(MainWindow)
        self.statusbar = QStatusBar(MainWindow)
        table_pallet = QtGui.QPalette()
        table_pallet_color = QtGui.QColor(QtCore.Qt.GlobalColor.darkBlue)

        self.tabWidget.setEnabled(True)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy()
                                     .hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(550, 0))
        self.tabWidget.setStyleSheet('')
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 858, 22))
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        table_pallet_color.setAlpha(25)
        table_pallet.setColor(QtGui.QPalette.ColorRole.AlternateBase,
                              table_pallet_color)

        self.w_tab.setupUi()
        self.tabWidget.addTab(self.w_tab.tabWallets, '')
        self.ns_tab.setupUi()
        self.tabWidget.addTab(self.ns_tab.tabNamespaces, '')
        self.nft_tab.setupUi()
        self.tabWidget.addTab(self.nft_tab.tabNFT, '')
        self.ab_tab.setupUi()
        self.tabWidget.addTab(self.ab_tab.tabAddBook, '')
        self.u_tab.setupUi()
        self.tabWidget.addTab(self.u_tab.tabUtils, '')
        self.settings_tab.setupUi()
        self.tabWidget.addTab(self.settings_tab.tabSettings, '')
        self.verticalLayout.addWidget(self.tabWidget)

        self.w_tab.retranslateUi()
        self.ns_tab.retranslateUi()
        self.nft_tab.retranslateUi()
        self.ab_tab.retranslateUi()
        self.u_tab.retranslateUi()
        self.settings_tab.retranslateUi()

        self.tabWidget.setCurrentIndex(0)

        self.w_tab.tbl_w.setPalette(table_pallet)
        self.w_tab.tbl_tx.setPalette(table_pallet)
        self.w_tab.tbl_addr.setPalette(table_pallet)
        self.w_tab.tbl_addr2.setPalette(table_pallet)
        self.ns_tab.tbl_ns.setPalette(table_pallet)
        self.nft_tab.tbl_auctions.setPalette(table_pallet)
        self.ab_tab.tbl_addr.setPalette(table_pallet)
        self.settings_tab.elxp_tbl.setPalette(table_pallet)
        self.settings_tab.ipfs_tbl.setPalette(table_pallet)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.w_tab.tabWallets),
                                  _translate('MainWindow', 'Wallets'))
        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.ab_tab.tabAddBook),
                                  _translate('MainWindow', 'Address Book'))
        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.ns_tab.tabNamespaces),
                                  _translate('MainWindow', 'Namespaces'))
        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.nft_tab.tabNFT),
                                  _translate('MainWindow', 'NFT'))
        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.settings_tab.tabSettings),
                                  _translate('MainWindow', 'Settings'))
        self.tabWidget.setTabText(self.tabWidget
                                  .indexOf(self.u_tab.tabUtils),
                                  _translate('MainWindow', 'Utils'))
