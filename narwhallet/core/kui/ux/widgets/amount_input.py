from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class AmountInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.amount = QLineEdit()
        self.addWidget(self.label)
        self.addWidget(self.amount)

        self.label.setText(QCoreApplication.translate('AmountInput',
                                                      'Amount:'))

    def show(self):
        self.label.setVisible(True)
        self.amount.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.amount.setVisible(False)
