from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.core.kui.ux.widgets.generator import UShared


class _address_book_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        UShared.set_table_properties(self, name)
        UShared.set_table_columns(9, ['', 'Coin', 'Name', 'Address', 'Sent',
                                      'Received', 'Label', '', ''], self)
        self.setColumnHidden(1, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)

    def add_bookaddresses(self, book_addresses: list):
        UShared.remove_table_rows(self)

        for i in book_addresses:
            self.add_bookaddress(i)

        self.resizeColumnsToContents()
        self.setColumnWidth(7, 20)

    def add_bookaddress(self, book_address: dict):
        self.setSortingEnabled(False)
        _r = self.rowCount()
        self.insertRow(_r)

        _vpic = UShared.create_table_item_graphic(1)
        _bvpic = UShared.create_table_item_graphic(2)

        _coin = UShared.create_table_item(book_address['coin'])
        _name = UShared.create_table_item(book_address['name'])
        _address = UShared.create_table_item(book_address['address'])
        if 'sent' in book_address:
            _sent = UShared.create_table_item(book_address['sent'])
        else:
            _sent = UShared.create_table_item('0.0')

        if 'received' in book_address:
            _received = UShared.create_table_item(book_address['received'])
        else:
            _received = UShared.create_table_item('0.0')

        _label = UShared.create_table_item(book_address['label'])
        _dellabel = UShared.create_table_item_graphic(3)

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setItem(_r, 1, _coin)
        self.setItem(_r, 2, _name)
        self.setItem(_r, 3, _address)
        self.setItem(_r, 4, _sent)
        self.setItem(_r, 5, _received)
        self.setItem(_r, 6, _label)
        self.setCellWidget(_r, 7, _dellabel)
        self.setItem(_r, 7, UShared.create_table_item(''))
        self.setCellWidget(_r, 8, _bvpic)
        self.setItem(_r, 9, UShared.create_table_item(''))
        self.setSortingEnabled(True)
