from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel


class AddressComboBox(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.combo = QComboBox()
        self.addWidget(self.label)
        self.addWidget(self.combo)

        self.combo.setMinimumWidth(350)
        self.combo.addItem('-', '-')
        self.label.setText(QCoreApplication.translate('AddressComboBox',
                                                      'Address:'))

    def show(self):
        self.label.setVisible(True)
        self.combo.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.combo.setVisible(False)
