from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.walletlistinfo import WalletListInfo
from narwhallet.control.shared import MShared
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class HomeScreen(Screen):
    wallet_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.wallet_list.clear_widgets()
        
        for _w in self.manager.wallets.wallets:
            if _w is not None:
                _t = WalletListInfo()
                _t.wallet_name.text = _w.name
                _t.ticker.text = _w.coin
                _t.balance.text = str(round(_w.balance, 8)) #str(_w.balance)
                _t.last_updated.text = MShared.get_timestamp(_w.last_updated)[1]
                _t.sm = self.manager

                self.wallet_list.add_widget(_t)
