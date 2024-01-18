from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.namespaceinfoactionbar import NamespaceInfoActionBar
from narwhallet.core.kui.widgets.namespacereplyinfo import NamespaceReplyInfo
from narwhallet.core.kui.widgets.nwimage import Nwimage
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage
from narwhallet.core.kcl.favorites.favorite import MFavorite


class BidDetailScreen(Screen):
    namespaceid = StringProperty()
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    header = Header()
    favorite = Nwimage()
    favorite_source = StringProperty()

    def populate(self, namespaceid, shortcode):
        self.header.value = 'Bid'
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid
        self.shortcode.text = shortcode
        self.namespace_name.text = ''
        _ns = MShared.get_shortcode(shortcode, self.manager.kex)
        _ns = _ns['result']

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        self.namespace_name.text = str(_ns['name'])
        _dat = _ns['data']
        self.keys = len(_dat)
        _dat.reverse()
        for _kv in _dat:
            _ins = NamespaceInfo()

            _ns_action_bar = NamespaceInfoActionBar()
            _ns_action_bar.txid = str(_kv['txid'])
            _ns_action_bar.addr = str(_kv['addr'])
            _ns_action_bar.sm = self.manager
            
            if self.owner.text == '':
                self.owner.text = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator.text = _kv['addr']

            _ins.key = str(_kv['dkey'])
            _ins.data = str(_kv['dvalue'])
            _ipfs_images = self.manager.cache_IPFS(_ins.data)

            for _i in _ipfs_images:
                _im = Nwnsimage()
                _ins.data =_ins.data.replace(_i[0], '')
                _im.image_path = _i[2]
                _im.image.bind(size=_im.on_size)
                _im.image.texture_update()
                self.namespace_key_list.add_widget(_im)

            _ins.add_widget(_ns_action_bar)

            for rep in _kv['replies']:
                _nsi = NamespaceReplyInfo()
                _nsi.key = '@' + str(rep['root_shortcode']) + ' - ' + str(rep['name'])
                _nsi.data = str(rep['dvalue'])
                _nsi.txid = str(rep['txid'])
                # NOTE Currently using the address assosiated with the
                # specific key output. This may differ from current
                # namespace owner address.
                _nsi.addr = str(rep['addr'])
                _nsi.sm = self.manager

                _ipfs_images = self.manager.cache_IPFS(_nsi.data)

                for _i in _ipfs_images:
                    _im = Nwnsimage()
                    _nsi.data =_nsi.data.replace(_i[0], '')
                    _im.image_path = _i[2]
                    _im.image.bind(size=_im.on_size)
                    _nsi.add_widget(_im)

                _ins.add_widget(_nsi)
            self.namespace_key_list.add_widget(_ins)

        self.manager.current = 'biddetail_screen'

    def bid_namespace(self):
        self.manager.bidnamespace_screen.populate(self.namespaceid)

    def on_touch_down(self, touch):
        if self.favorite.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            self.set_favorite()
            return
        return super(BidDetailScreen, self).on_touch_down(touch)

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