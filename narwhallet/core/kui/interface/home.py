from kivy.app import App
from kivy.uix.screenmanager import Screen
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.core.kui.widgets.header import Header


class HomeScreen(Screen):
    wallet_list = Nwgrid()
    header = Header()

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self):
        self.wallet_list.data = []
        
        for _w in self.app.ctrl.wallets.wallets:
            if _w is not None:
                _t = {}
                _t['wallet_name'] = _w.name
                _t['ticker'] = _w.coin
                _t['balance'] = str(round(_w.balance, 8))
                _t['last_updated'] = Ut.get_timestamp(_w.last_updated)[1]
                _t['sm'] = self.manager

                if _w.locked == True:
                    _t['lock_icon'] = 'narwhallet/core/kui/assets/lock.png'
                else:
                    _t['lock_icon'] = 'narwhallet/core/kui/assets/lock-open.png'
                self.wallet_list.data.append(_t)
