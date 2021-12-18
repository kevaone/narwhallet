from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton


class DialogButtonBox(QDialogButtonBox):
    def __init__(self, parent):
        super().__init__()

        self.setParent(parent)
        _ar = QDialogButtonBox.ActionRole
        _ac = QDialogButtonBox.AcceptRole
        self.next = QPushButton(self)
        self.back = QPushButton(self)
        self.cancel = QPushButton(self)
        self.send = QPushButton(self)

        self.setOrientation(QtCore.Qt.Horizontal)
        self.addButton(self.cancel, _ar)
        self.addButton(self.next, _ar)
        self.addButton(self.back, _ar)
        self.addButton(self.send, _ac)
        self.back.setVisible(False)
        self.next.setEnabled(False)
        self.send.setEnabled(False)
        self.cancel.setText(QCoreApplication.translate('DialogButtonBox', 'Cancel'))
        self.send.setText(QCoreApplication.translate('DialogButtonBox', 'Send'))
        self.next.setText(QCoreApplication.translate('DialogButtonBox', 'Next'))
        self.back.setText(QCoreApplication.translate('DialogButtonBox', 'Back'))

