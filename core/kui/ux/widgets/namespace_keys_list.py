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
            self._add_key(i[5])

    def _add_key(self, key: str):
        _key = QListWidgetItem(key)
        _key.setForeground(QtCore.Qt.black)

        self.addItem(_key)
