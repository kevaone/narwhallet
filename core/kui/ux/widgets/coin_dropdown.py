from PyQt5.QtWidgets import QComboBox


_coins = [
    ['Bitcoin', 'BIT', [44, 49]],
    ['Dogecoin', 'DOGE', [44, 49]],
    ['Kevacoin', 'KVA', [49]],
    ['Litecoin', 'LTC', [44, 49]],
    ['Monero', 'XMR', [44, 49]]
]


class _coin_dropdown(QComboBox):
    def __init__(self, QWidget):
        super().__init__()

        self.coins = _coins
        self.coin_filter = 0
        self.load_coins()

    def load_coins(self):
        self.clear()
        self.addItem('-', '-')
        for i in self.coins:
            if self.coin_filter in i[2] or self.coin_filter == 0:
                self.addItem(i[0], i[1])

    def set_coins(self, coins):
        if coins == 'bip44' or coins == 44:
            self.coin_filter = 44
        elif coins == 'bip49' or coins == 49:
            self.coin_filter = 49
        self.load_coins()
