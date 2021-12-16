from PyQt5.QtWidgets import QWidget, QTableWidget
from narwhallet.core.kui.ux.widgets.generator import UShared


class _electrumx_peers_table(QTableWidget):
    def __init__(self, name: str, _parent: QWidget):
        super().__init__()

        UShared.set_table_properties(self, name)
        UShared.set_table_columns(10, ['', 'Coin', 'Host', 'Port',
                                       'Type', 'TLS', 'Ping', 'Status',
                                       '', 'Active'], self)
        self.setColumnHidden(1, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)

    def add_peer(self, coin, host, port, tls):
        _r = self.rowCount()
        self.insertRow(self.rowCount())
        _vpic = UShared.create_table_item_graphic(11)
        _vpic.setToolTip('Edit ElectrumX Peer')
        _dellabel = UShared.create_table_item_graphic(3)
        _dellabel.setToolTip('Delete ElectrumX Peer')

        if isinstance(tls, bool):
            if tls is True:
                tls = 'True'
            elif tls is False:
                tls = 'False'

        self.setCellWidget(_r, 0, _vpic)
        self.setItem(_r, 0, UShared.create_table_item(''))
        self.setItem(_r, 1, UShared.create_table_item(coin))
        self.setItem(_r, 2, UShared.create_table_item(host))
        self.setItem(_r, 3, UShared.create_table_item(port))
        self.setItem(_r, 4, UShared.create_table_item('HTTP'))
        self.setItem(_r, 5, UShared.create_table_item(tls))
        self.setItem(_r, 6, UShared.create_table_item('0ms'))
        self.setItem(_r, 7, UShared.create_table_item('disconnected'))
        self.setCellWidget(_r, 8, _dellabel)
        self.setItem(_r, 8, UShared.create_table_item(''))
        self.resizeColumnsToContents()

    def update_peer_status(self, row: int, status: str):
        self.setItem(row, 7, UShared.create_table_item(status))
        self.resizeColumnsToContents()

    def update_active(self, active_row: int):
        for row in range(0, self.rowCount()):
            self.removeCellWidget(row, 9)
        _vpic = UShared.create_table_item_graphic(9)
        _vpic.setToolTip('Default ElectrumX Peer')
        self.setCellWidget(active_row, 9, _vpic)
        self.resizeColumnsToContents()
