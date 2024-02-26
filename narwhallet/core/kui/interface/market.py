import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kex.cmd import _custom
from narwhallet.core.kui.widgets.header import Header


class MarketScreen(Screen):
    auction_list = ObjectProperty(None)
    header = Header()

    def __init__(self, **kwargs):
        super(MarketScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

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
