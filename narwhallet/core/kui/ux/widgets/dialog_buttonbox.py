from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton
from narwhallet.core.kui.ux.widgets.delay_button import DelayPushButton


class DialogButtonBox(QDialogButtonBox):
    def __init__(self, parent):
        super().__init__()

        self.setParent(parent)
        self.setOrientation(QtCore.Qt.Horizontal)
        _ar = QDialogButtonBox.ActionRole
        _ac = QDialogButtonBox.AcceptRole
        self.next = QPushButton(self)
        self.back = QPushButton(self)
        self.cancel = QPushButton(self)
        self.send = DelayPushButton('Send', 5)

        self.addButton(self.cancel, _ar)
        self.addButton(self.next, _ar)
        self.addButton(self.back, _ar)
        self.addButton(self.send, _ac)

        self.back.setVisible(False)
        self.next.setEnabled(False)
        self.send.setEnabled(False)

        self.cancel.setText(QCoreApplication.translate('DialogButtonBox',
                                                       'Cancel'))
        # self.send.setText(QCoreApplication.translate('DialogButtonBox',
        #                                              'Send'))
        self.next.setText(QCoreApplication.translate('DialogButtonBox',
                                                     'Next'))
        self.back.setText(QCoreApplication.translate('DialogButtonBox',
                                                     'Back'))
