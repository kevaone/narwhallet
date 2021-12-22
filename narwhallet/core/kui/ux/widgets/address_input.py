from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class AddressInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.address = QLineEdit()
        self.addWidget(self.label)
        self.addWidget(self.address)

        self.address.setMinimumWidth(350)
        self.label.setText(QCoreApplication.translate('AddressInput',
                                                      'Address:'))

    def show(self):
        self.label.setVisible(True)
        self.address.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.address.setVisible(False)
