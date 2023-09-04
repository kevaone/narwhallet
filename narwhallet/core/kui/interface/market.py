import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kex.peer import _peer
from narwhallet.core.kex.cmd import _custom
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class MarketScreen(Screen):
    auction_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('Market')
        self.auction_list.scroll_y = 1
        self.auction_list.data = []
        # https://kva.keva.one/get_nft_auctions
        _data_provider = self.manager.settings_screen.settings.content_providers[0]
        _market_data_peer = _peer(_data_provider[1], _data_provider[2], _data_provider[3], _data_provider[4])
        try:
            _market_data_peer.connect()
            _data = json.loads(_market_data_peer.comm(_custom.get_nft_auctions(1)))
        except:
            # TODO: Handle failure in aquiring market data
            return

        for result in _data['result']['data']:
            if result['nsid'] in self.manager.favorites.favorites:
                _fav = 'narwhallet/core/kui/assets/star.png'
            else:
                _fav = 'narwhallet/core/kui/assets/star_dark.png'

            _auction = {
                'time': result['time'],
                'root_shortcode': str(result['root_shortcode']),
                'desc': str(result['desc']),
                'displayName': str(result['displayName']),
                'price': str(result['price']),
                'bids': str(result['bids'][0]),
                'high_bid': str(result['bids'][1]),
                'favorite_source': _fav,
                'namespaceid': result['nsid'],
                'sm': self.manager
            }
            self.auction_list.data.append(_auction)

        self.manager.current = 'market_screen'
