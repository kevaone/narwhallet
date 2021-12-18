from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel


class WalletComboBox(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.combo = QComboBox()
        self.addWidget(self.label)
        self.addWidget(self.combo)

        # _combo.setMinimumWidth(250)
        self.combo.addItem('-', '-')
        self.label.setText(QCoreApplication.translate('WalletComboBox',
                                                      'Wallet:'))
