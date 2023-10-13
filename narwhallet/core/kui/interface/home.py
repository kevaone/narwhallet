from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header


class HomeScreen(Screen):
    wallet_list = Nwgrid()
    header = Header()

    def populate(self):
        self.wallet_list.data = []
        
        for _w in self.manager.wallets.wallets:
            if _w is not None:
                _t = {}
                _t['wallet_name'] = _w.name
                _t['ticker'] = _w.coin
                _t['balance'] = str(round(_w.balance, 8))
                _t['last_updated'] = MShared.get_timestamp(_w.last_updated)[1]
                _t['sm'] = self.manager
                self.wallet_list.data.append(_t)
