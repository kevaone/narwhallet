import copy
import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kex.cmd import _custom
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwgrid import Nwgrid
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class MarketScreen(Screen):
    auction_list = Nwgrid()
    header = Header()
    btn_filter_all = Nwbutton()
    btn_filter_media = Nwbutton()
    btn_filter_content = Nwbutton()

    def __init__(self, **kwargs):
        super(MarketScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()
        self._original = []

    def populate(self):
        self.header.value = 'Market'
        self.auction_list.scroll_y = 1
        self.auction_list.data = []
        # https://kva.keva.one/get_nft_auctions
        
        try:
            _ = self.app.ctrl.kex.peers[self.app.ctrl.kex.active_peer].connect()
            _data = json.loads(self.app.ctrl.kex.call(_custom.get_nft_auctions(1)))
            self.app.ctrl.kex.peers[self.app.ctrl.kex.active_peer].disconnect()
        except:
            # TODO: Handle failure in aquiring market data
            return

        for result in _data['result']['data']:
            if result['nsid'] in self.manager.favorites.favorites:
                _fav = 'narwhallet/core/kui/assets/star_dark.png'
            else:
                _fav = 'narwhallet/core/kui/assets/star.png'

            _auction = {
                'time': result['time'],
                'root_shortcode': str(result['root_shortcode']),
                'keys': str(''),
                'desc': str(result['desc']),
                'displayName': str(result['displayName']),
                'price': str(result['price']),
                'bids': str(result['bids'][0]),
                'high_bid': str(result['bids'][1]),
                'favorite_source': _fav,
                'namespaceid': result['nsid'],
                'sm': self.manager,
                'image_path': ''
            }

            if 'media' in result:
                if 'video' not in result['media']:
                    _auction['image_path'] = result['media']

            self.auction_list.data.append(_auction)

        self.manager.current = 'market_screen'

    def filter_media(self, type):
        if self._original == []:
            self._original = self.auction_list.data

        _tmp = []

        if type == 'media':    
            for _i in self._original:
                if _i['image_path'] != '':
                    _tmp.append(_i)
            self.auction_list.data = _tmp
            self.btn_filter_all.background_color = [54/255, 58/255, 59/255, 1]
            self.btn_filter_media.background_color = [86/255, 86/255, 86/255, 1]
            self.btn_filter_content.background_color = [54/255, 58/255, 59/255, 1]
        elif type == 'content':
            for _i in self._original:
                if _i['image_path'] == '':
                    _tmp.append(_i)
            self.auction_list.data = _tmp
            self.btn_filter_all.background_color = [54/255, 58/255, 59/255, 1]
            self.btn_filter_media.background_color = [54/255, 58/255, 59/255, 1]
            self.btn_filter_content.background_color = [86/255, 86/255, 86/255, 1]
        elif type == 'all':
            self.auction_list.data = self._original
            self.btn_filter_all.background_color = [86/255, 86/255, 86/255, 1]
            self.btn_filter_media.background_color = [54/255, 58/255, 59/255, 1]
            self.btn_filter_content.background_color = [54/255, 58/255, 59/255, 1]
