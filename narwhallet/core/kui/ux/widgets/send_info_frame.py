from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (QHBoxLayout, QFrame, QLabel, QPlainTextEdit,
                             QVBoxLayout)


class SendInfoFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.vl = QVBoxLayout(self)
        self.fee_hl = QHBoxLayout()
        self.fee_l = QLabel()
        self.fee = QLabel()
        self.feerate_hl = QHBoxLayout()
        self.feerate_l = QLabel()
        self.feerate = QLabel()
        self.tx_hl = QHBoxLayout()
        self.tx_l = QLabel()
        self.txsize_l = QLabel()
        self.txsize = QLabel()
        self.tx = QPlainTextEdit()

        self.vl.setContentsMargins(0, 0, 0, 0)
        self.tx.setMaximumHeight(65)
        self.tx.setReadOnly(True)

        self.fee_hl.addWidget(self.fee_l)
        self.fee_hl.addWidget(self.fee)
        self.vl.addLayout(self.fee_hl)
        self.feerate_hl.addWidget(self.feerate_l)
        self.feerate_hl.addWidget(self.feerate)
        self.vl.addLayout(self.feerate_hl)
        self.tx_hl.addWidget(self.tx_l)
        self.tx_hl.addWidget(self.txsize_l)
        self.tx_hl.addWidget(self.txsize)
        self.vl.addLayout(self.tx_hl)
        self.vl.addWidget(self.tx)

        self.fee_l.setText(QCoreApplication.translate('SIF', 'Fee (KVA):'))
        _frl = 'Fee Rate (Satoshi per byte):'
        self.feerate_l.setText(QCoreApplication.translate('SIF', _frl))
        self.tx_l.setText(QCoreApplication.translate('SIF', 'Raw TX -'))
