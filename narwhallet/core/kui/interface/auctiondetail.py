from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.auctioninfo import AuctionInfo
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwimage import Nwimage
from narwhallet.core.kcl.favorites.favorite import MFavorite


class AuctionDetailScreen(Screen):
    namespaceid = StringProperty()
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    owner = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    header = Header()
    favorite = Nwimage()
    favorite_source = StringProperty()

    def __init__(self, **kwargs):
        super(AuctionDetailScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self, namespaceid, shortcode):
        self.header.value = 'Auction'
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid
        self.shortcode.text = shortcode
        self.namespace_name.text = ''
        _ns = MShared.get_namespace(namespaceid, self.app.ctrl.kex)
        if _ns is None:
            return

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        if _ns.social_name != '':
            self.namespace_name.text = str(_ns.social_name)
        else:
            self.namespace_name.text = str(_ns.name)

        self.keys = len(_ns.keys.keys)
        _ns.keys.keys.reverse()
        self.owner.text = _ns.address
        self.creator.text = _ns.creator
        for _kv in _ns.keys.keys:
            if _kv.dtype == 'nft_auction':
                for _r in _kv.replies:
                    _ins = AuctionInfo()
                    _ins.auction_namespace = namespaceid
                    _ins.auction_namespace_addr = self.owner.text
                    _ins.time = _r.date[0]
                    _ins.shortcode = str(_r.root_shortcode)
                    _ins.nsname = str(_r.name)
                    _ins.bid = str(_r.dvalue)
                    _ins.transaction = _r.txid
                    _ins.sm = self.manager
                    if str(_r.dvalue) != 'error':
                        self.namespace_key_list.add_widget(_ins)
                break

        self.manager.current = 'auctiondetail_screen'

    def decline_bid(self, transaction):
        pass

    def on_touch_down(self, touch):
        if self.favorite.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            self.set_favorite()
            return
        return super(AuctionDetailScreen, self).on_touch_down(touch)

    def set_favorite(self):
        _add_fav = False
        if self.favorite_source == 'narwhallet/core/kui/assets/star.png':
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
            _add_fav = True
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        if _add_fav:
            # TODO Validate inputs
            _a = MFavorite()
            # TODO Make more dynamic once more favorite types come into play
            _a.set_id(self.namespaceid)
            _a.set_coin('KEVACOIN')
            _a.set_kind('Namespace')
            _a.set_value([self.namespaceid, self.shortcode, self.namespace_name, self.keys])
            _a.set_filter([])

            self.manager.favorites.favorites[_a.id] = _a
        else:
            self.manager.favorites.remove_favorite(self.namespaceid)

        self.manager.favorites.save_favorites()
