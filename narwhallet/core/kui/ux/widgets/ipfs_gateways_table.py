from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.core.kui.ux.widgets.generator import UShared


class _ipfs_gateways_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        UShared.set_table_properties(self, name)
        UShared.set_table_columns(8, ['', 'Online', 'CORS', 'Origin',
                                      'Host', 'Delay', '', 'Active'], self)
        self.setColumnHidden(1, True)
        self.setColumnHidden(5, True)

    def add_gateway_from_list(self, gateway_data: list):
        _r = self.rowCount()
        self.insertRow(self.rowCount())

        _vpic = UShared.create_table_item_graphic(10)
        _gvpic = UShared.create_table_item_graphic(11)
        _gvpic.setToolTip('Edit IPFS Gateway')
        _dellabel = UShared.create_table_item_graphic(3)
        _dellabel.setToolTip('Delete IPFS Gateway')

        self.setCellWidget(_r, 0, _gvpic)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setCellWidget(_r, 1, _vpic)
        self.setItem(_r, 1, UShared.create_table_item(''))
        self.setItem(_r, 2, UShared.create_table_item(gateway_data[0]))
        self.setItem(_r, 3, UShared.create_table_item(gateway_data[1]))
        self.setItem(_r, 4, UShared.create_table_item(gateway_data[2]))
        self.setItem(_r, 5, UShared.create_table_item('~ms'))
        self.setCellWidget(_r, 6, _dellabel)
        self.setItem(_r, 6, UShared.create_table_item(''))

        self.resizeColumnsToContents()

    def update_gateway_status(self, row: int, status: str):
        _vpic = UShared.create_table_item_graphic(4)
        self.setCellWidget(row, 1, _vpic)
        self.resizeColumnsToContents()

    def update_active(self, active_row: int):
        for row in range(0, self.rowCount()):
            self.removeCellWidget(row, 7)
        _vpic = UShared.create_table_item_graphic(9)
        _vpic.setToolTip('Default IPFS Gateway')
        self.setCellWidget(active_row, 7, _vpic)
        self.resizeColumnsToContents()
