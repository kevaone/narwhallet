from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem


class _namespace_keys_list(QListWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        self.setObjectName(name)

    def clear_rows(self):
        for i in range(0, self.count()):
            self.item(i).setText('')
            self.item(i).setBackground(QtCore.Qt.white)
            self.item(i).setHidden(True)

    def add_keys(self, keys: list):
        self.clear_rows()

        _pl = []
        _plc = 0
        for c, i in enumerate(keys):
            if i[5] == '_KEVA_NS_' or i[5] == '\x01_KEVA_NS_':
                _pl.append(c)

        _pl.reverse()
        for i in range(0, len(_pl)-1):
            _ = keys.pop(_pl[i]-0)
            _plc += 1

        for c, i in enumerate(keys):
            self._add_key(c, i[5], i[7])

    def _add_key(self, idx: int, key: str, special):
        if idx == self.count():
            _key = QListWidgetItem(key)
            _key.setForeground(QtCore.Qt.black)
            self.addItem(_key)
        elif idx <= self.count():
            _key = self.item(idx)
            _key.setText(key)
            _key.setHidden(False)
        self._set_key_special(_key, special)

    @staticmethod
    def _set_key_special(key: QListWidgetItem, special: str):
        # TODO Store color selections in settings to allow adjustment
        if special == 'root_ns':
            key.setBackground(QtCore.Qt.magenta)
        elif special == 'root_ns_update':
            key.setBackground(QtCore.Qt.cyan)
        elif special == 'reply':
            key.setBackground(QtCore.Qt.yellow)
        elif special == 'repost':
            key.setBackground(QtCore.Qt.gray)
        elif special == 'reward':
            key.setBackground(QtCore.Qt.green)
        elif special == 'nft_bid':
            key.setBackground(QtCore.Qt.darkYellow)
        elif special == 'nft_auction':
            key.setBackground(QtCore.Qt.lightGray)
        elif special == 'nft_confirm_sell':
            key.setBackground(QtCore.Qt.blue)
