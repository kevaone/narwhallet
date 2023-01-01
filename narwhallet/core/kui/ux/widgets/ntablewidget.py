from typing import List, Optional
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QColor


class NTableWidget(QTableWidget):
    def add_row(self):
        raise NotImplementedError

    def add_rows(self):
        raise NotImplementedError

    def clear_row(self, row: int):
        self.setRowHidden(row, True)
        for c in range(0, self.columnCount()):
            _i = self.item(row, c)
            if _i is not None:
                _i.setText('')

    def clear_rows(self):
        for i in range(0, self.rowCount()):
            self.clear_row(i)

    def get_text(self, row: int, column: int) -> Optional[str]:
        _r = self.item(row, column)
        if _r is not None:
            return _r.text()

        return None

    def remove_rows(self):
        _m = self.rowCount()

        while _m > -1:
            self.removeRow(_m)
            _m = _m - 1

    def set_columns(self, columns, headers: List[str]):
        self.setColumnCount(columns)
        self.setHorizontalHeaderLabels(headers)
        for c in range(0, columns):
            _i = self.horizontalHeaderItem(c)
            if _i is not None:
                _i.setTextAlignment(4)
        self.horizontalHeader().setMinimumSectionSize(5)

    def set_properties(self, name: str):
        self.setObjectName(name)
        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

    def set_row_color(self, row: int, color: QColor):
        for c in range(0, self.columnCount()):
            _i = self.item(row, c)
            if _i is not None:
                _i.setBackground(color)

    def set_text(self, row: int, column: int, text: str) -> None:
        _r = self.item(row, column)
        if _r is not None:
            _r.setText(text)