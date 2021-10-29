from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class _namespace_keys_list(QListWidget):
    def __init__(self, name: str, QWidget):
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
        for i in range(0, len(keys)):
            if keys[i][5] == '_KEVA_NS_' or keys[i][5] == '\x01_KEVA_NS_':
                _pl.append(i)

        _pl.reverse()
        for i in range(0, len(_pl)-1):
            _ = keys.pop(_pl[i]-0)
            _plc += 1

        for i in range(0, len(keys)):
            self._add_key(i, keys[i][5], keys[i][7])

    def _add_key(self, idx: int, key: str, special):
        if idx == self.count():
            _key = QListWidgetItem(key)
            _key.setForeground(QtCore.Qt.black)
            self.addItem(_key)
        elif idx <= self.count():
            _key = self.item(idx)
            _key.setText(key)
            _key.setHidden(False)

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
