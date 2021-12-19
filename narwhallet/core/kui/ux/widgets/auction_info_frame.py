from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QHBoxLayout, QFrame, QLabel, QLineEdit,
                             QVBoxLayout)


class AuctionInfoFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.vl = QVBoxLayout(self)
        self.hl_1 = QHBoxLayout()
        self.hl_2 = QHBoxLayout()
        self.hl_3 = QHBoxLayout()
        self.hl_4 = QHBoxLayout()
        self.hl_5 = QHBoxLayout()
        self.hl_6 = QHBoxLayout()
        self.hl_7 = QHBoxLayout()
        self.short_l = QLabel(self)
        self.nft_shortcode = QLabel(self)
        self.name_l = QLabel(self)
        self.nft_name = QLineEdit(self)
        self.desc_l = QLabel(self)
        self.nft_desc = QLineEdit(self)
        self.hashtags_l = QLabel(self)
        self.nft_hashtags = QLineEdit(self)
        self.price_l = QLabel(self)
        self.nft_price = QLineEdit(self)
        self.ns_l = QLabel(self)
        self.nft_ns = QLineEdit(self)
        self.address_l = QLabel(self)
        self.nft_address = QLineEdit(self)

        self.vl.setContentsMargins(0, 0, 0, 0)

        self.hl_1.addWidget(self.short_l)
        self.hl_1.addWidget(self.nft_shortcode)
        self.vl.addLayout(self.hl_1)
        self.hl_2.addWidget(self.name_l)
        self.hl_2.addWidget(self.nft_name)
        self.vl.addLayout(self.hl_2)
        self.hl_3.addWidget(self.desc_l)
        self.hl_3.addWidget(self.nft_desc)
        self.vl.addLayout(self.hl_3)
        self.hl_4.addWidget(self.hashtags_l)
        self.hl_4.addWidget(self.nft_hashtags)
        self.vl.addLayout(self.hl_4)
        self.hl_5.addWidget(self.price_l)
        self.hl_5.addWidget(self.nft_price)
        self.vl.addLayout(self.hl_5)
        self.hl_6.addWidget(self.ns_l)
        self.hl_6.addWidget(self.nft_ns)
        self.vl.addLayout(self.hl_6)
        self.hl_7.addWidget(self.address_l)
        self.hl_7.addWidget(self.nft_address)
        self.vl.addLayout(self.hl_7)

        self.short_l.setText(QCoreApplication.translate('AIF', 'Shortcode: '))
        self.address_l.setText(QCoreApplication.translate('AIF',
                                                          'Payment Address: '))
        self.name_l.setText(QCoreApplication.translate('AIF', 'Name: '))
        self.desc_l.setText(QCoreApplication.translate('AIF', 'Description: '))
        self.hashtags_l.setText(QCoreApplication.translate('AIF',
                                                           'Hashtags: '))
        self.price_l.setText(QCoreApplication.translate('AIF',
                                                        'Asking Price: '))
        self.ns_l.setText(QCoreApplication.translate('AIF', 'NS: '))
