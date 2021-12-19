from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class TransactionInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.tx = QLineEdit()
        self.addWidget(self.label)
        self.addWidget(self.tx)

        self.label.setText(QCoreApplication.translate('TransactionInput',
                                                      'TX:'))

    def show(self):
        self.label.setVisible(True)
        self.tx.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.tx.setVisible(False)
