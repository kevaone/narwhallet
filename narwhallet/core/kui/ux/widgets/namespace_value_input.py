from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit


class NamespaceValueInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.value = QPlainTextEdit()
        self.addWidget(self.label)
        self.addWidget(self.value)

        self.label.setText(QCoreApplication.translate('NamespaceValueInput',
                                                      'Value:'))

    def show(self):
        self.label.setVisible(True)
        self.value.setVisible(True)

    def hide(self):
        self.label.setVisible(False)
        self.value.setVisible(False)
