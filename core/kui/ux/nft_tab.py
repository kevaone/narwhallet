from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QLabel, QSplitter, QPushButton, QSpacerItem,
                             QSizePolicy)

from core.kui.ux.widgets.auctions_table import _auctions_table
from core.kui.ux.widgets.bids_table import _bids_table
from core.kui.ux.widgets.bid_table import _bid_table


class Ui_NFTTab(QObject):
    def setupUi(self):
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum

        self.tabNFT = QWidget()
        self.tabNFT.setObjectName('tabNFT')

        self.tab_vl = QVBoxLayout(self.tabNFT)
        self.tbl_auctions = _auctions_table('nft_auctions', self.tabNFT)
        self.tbl_bids = _bids_table('nft_bids', self.tabNFT)
        self.tbl_bids_2 = _bid_table('nft_bids_2', self.tabNFT)
        self.frame_1 = QFrame(self.tabNFT)
        self.frame_1a = QFrame(self.frame_1)
        self.frame_1b = QFrame(self.frame_1)
        self.frame_2 = QFrame(self.tabNFT)
        self.frame_3 = QFrame(self.tabNFT)
        self.frame_1_vl = QVBoxLayout(self.frame_1)
        self.frame_1a_vl = QVBoxLayout(self.frame_1a)
        self.frame_1b_vl = QVBoxLayout(self.frame_1b)
        self.frame_2_vl = QVBoxLayout(self.frame_2)
        self.frame_3_vl = QVBoxLayout(self.frame_3)
        self.frame_1_hl = QHBoxLayout()
        self.frame_2_hl_0 = QHBoxLayout()
        self.frame_2_hl_1 = QHBoxLayout()
        self.frame_2_hl_2 = QHBoxLayout()
        self.frame_2_hl_3 = QHBoxLayout()
        self.frame_2_hl_4 = QHBoxLayout()
        self.frame_2_hl_5 = QHBoxLayout()
        self.frame_2_hl_6 = QHBoxLayout()
        self.auctions_l = QLabel()
        self.bids_l = QLabel()
        self.auction_info_l = QLabel()
        self.display_name_l = QLabel()
        self.desc_l = QLabel()
        self.asking_l = QLabel()
        self.high_bid_l = QLabel()
        self.num_bids_l = QLabel()
        self.address_l = QLabel()
        self.hashtags_l = QLabel()
        self.display_name = QLabel()
        self.desc = QLabel()
        self.asking = QLabel()
        self.high_bid = QLabel()
        self.num_bids = QLabel()
        self.address = QLabel()
        self.hashtags = QLabel()

        self.btn_create_auction = QPushButton()
        self.btn_create_bid = QPushButton()
        self.btn_create_accept_bid = QPushButton()
        splitter_tables = QSplitter(QtCore.Qt.Orientation.Vertical)
        splitter_meta = QSplitter(QtCore.Qt.Orientation.Horizontal)

        self.frame_1_hl.addItem(QSpacerItem(20, 20, _sp_exp, _sp_min))
        self.frame_1_hl.addWidget(self.btn_create_auction)
        self.frame_1_hl.addWidget(self.btn_create_bid)
        self.frame_1_hl.addWidget(self.btn_create_accept_bid)
        self.tab_vl.addLayout(self.frame_1_hl)
        self.frame_1a_vl.addWidget(self.auctions_l)
        self.frame_1a_vl.addWidget(self.tbl_auctions)
        self.frame_1b_vl.addWidget(self.bids_l)
        self.frame_1b_vl.addWidget(self.tbl_bids)
        splitter_tables.addWidget(self.frame_1a)
        splitter_tables.addWidget(self.frame_1b)
        self.frame_1_vl.addWidget(splitter_tables)
        self.tab_vl.addWidget(splitter_tables)
        self.frame_2_vl.addWidget(self.auction_info_l)
        self.frame_2_hl_0.addWidget(self.display_name_l)
        self.frame_2_hl_0.addWidget(self.display_name)
        self.frame_2_vl.addLayout(self.frame_2_hl_0)
        self.frame_2_hl_1.addWidget(self.desc_l)
        self.frame_2_hl_1.addWidget(self.desc)
        self.frame_2_vl.addLayout(self.frame_2_hl_1)
        self.frame_2_hl_2.addWidget(self.hashtags_l)
        self.frame_2_hl_2.addWidget(self.hashtags)
        self.frame_2_vl.addLayout(self.frame_2_hl_2)
        self.frame_2_hl_3.addWidget(self.asking_l)
        self.frame_2_hl_3.addWidget(self.asking)
        self.frame_2_vl.addLayout(self.frame_2_hl_3)
        self.frame_2_hl_4.addWidget(self.high_bid_l)
        self.frame_2_hl_4.addWidget(self.high_bid)
        self.frame_2_vl.addLayout(self.frame_2_hl_4)
        self.frame_2_hl_5.addWidget(self.num_bids_l)
        self.frame_2_hl_5.addWidget(self.num_bids)
        self.frame_2_vl.addLayout(self.frame_2_hl_5)
        self.frame_2_hl_6.addWidget(self.address_l)
        self.frame_2_hl_6.addWidget(self.address)
        self.frame_2_vl.addLayout(self.frame_2_hl_6)
        self.frame_3_vl.addWidget(self.tbl_bids_2)
        splitter_meta.addWidget(self.frame_2)
        splitter_meta.addWidget(self.frame_3)
        splitter_meta.setSizes([275, 300])
        self.tab_vl.addWidget(splitter_meta)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.auctions_l.setText(_translate('tabNFT', 'My Auctions -'))
        self.auction_info_l.setText(_translate('tabNFT', 'Auction Info -'))
        self.bids_l.setText(_translate('tabNFT', 'My Bids -'))
        self.display_name_l.setText(_translate('tabNFT', 'Display Name:'))
        self.desc_l.setText(_translate('tabNFT', 'Description:'))
        self.hashtags_l.setText(_translate('tabNFT', 'Hashtags:'))
        self.asking_l.setText(_translate('tabNFT', 'Asking:'))
        self.high_bid_l.setText(_translate('tabNFT', 'High Bid:'))
        self.num_bids_l.setText(_translate('tabNFT', 'Total Bids:'))
        self.address_l.setText(_translate('tabNFT', 'Address:'))
        self.btn_create_auction.setText(_translate('tabNFT', 'Create Auction'))
        self.btn_create_bid.setText(_translate('tabNFT', 'Create Bid'))
        self.btn_create_accept_bid.setText(_translate('tabNFT', 'Accept Bid'))
