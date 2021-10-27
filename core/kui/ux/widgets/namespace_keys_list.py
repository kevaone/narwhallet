from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class _namespace_keys_list(QListWidget):
    def __init__(self, name: str, QWidget):
        super().__init__()

        self.setObjectName(name)

    def clear_rows(self):
        self.clear()

    def add_keys(self, keys: list):
        self.clear()

        for i in keys:
            self._add_key(i[5], i[7])

    def _add_key(self, key: str, special):
        _key = QListWidgetItem(key)
        _key.setForeground(QtCore.Qt.black)
        # TODO Store color selections in settings to allow adjustment
        if special == 'root_ns':
            _key.setBackground(QtCore.Qt.magenta)
        elif special == 'root_ns_update':
            _key.setBackground(QtCore.Qt.cyan)
        elif special == 'reply':
            _key.setBackground(QtCore.Qt.yellow)
        elif special == 'repost':
            _key.setBackground(QtCore.Qt.gray)
        elif special == 'reward':
            _key.setBackground(QtCore.Qt.green)
        elif special == 'nft_bid':
            _key.setBackground(QtCore.Qt.darkYellow)
        elif special == 'nft_auction':
            _key.setBackground(QtCore.Qt.lightGray)
        elif special == 'nft_confirm_sell':
            _key.setBackground(QtCore.Qt.blue)

        self.addItem(_key)
