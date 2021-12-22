from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class NamespaceKeyInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.key = QLineEdit()
        self.key.setMinimumWidth(350)
        self.addWidget(self.label)
        self.addWidget(self.key)

        self.label.setText(QCoreApplication.translate('NamespaceKeyInput',
                                                      'Key:'))

    def show(self):
        self.label.setVisible(True)
        self.key.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.key.setVisible(False)
