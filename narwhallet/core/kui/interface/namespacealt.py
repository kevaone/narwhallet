from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.namespaceinfopopup import NamespaceInfoPopup
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwimage import Nwimage
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage
from narwhallet.core.kcl.favorites.favorite import MFavorite


class NamespaceAltScreen(Screen):
    namespaceid = StringProperty()
    shortcode = StringProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = StringProperty(None)
    owner = StringProperty(None)
    namespace_name = StringProperty(None)
    header = Header()
    favorite = Nwimage()
    favorite_source = StringProperty()
    info_button = Nwbutton()

    def populate(self, namespaceid, shortcode):
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid
        self.shortcode = shortcode
        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
        _ns = _ns['result']

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        self.namespace_name = str(_ns['name'])
        self.header.value = shortcode + ' ' + self.namespace_name
        _dat = _ns['data']
        _dat.reverse()
        self.owner = ''
        for _kv in _dat:
            _ins = NamespaceInfo()
            if self.owner == '':
                self.owner = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator = _kv['addr']

            _ins.key = str(_kv['dkey'])
            _ins.data = str(_kv['dvalue'])
            _ipfs_images = self.manager.cache_IPFS(_ins.data)
            self.namespace_key_list.add_widget(_ins)
            for _i in _ipfs_images:
                _im = Nwnsimage()
                _im.image_path = _i
                _im.image.bind(size=_im.on_size)
                _im.image.texture_update()
                self.namespace_key_list.add_widget(_im)

        self.manager.current = 'namespacealt_screen'

    def info_popup(self):
        _nsi = NamespaceInfoPopup()
        _nsi.namespaceid._text = self.namespaceid
        _nsi.header.value = self.header.value
        _nsi.namespace_name._text = self.namespace_name
        _nsi.shortcode._text = self.shortcode
        _nsi.owner._text = self.owner
        _nsi.creator._text = self.creator
        _nsi.manager = self.manager
        _nsi.open()

    def bid_namespace(self):
        self.manager.bidnamespace_screen.populate(self.namespaceid)

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
            _a.set_coin('KEVACOIN')
            _a.set_kind('Namespace')
            _a.set_value(self.namespaceid)
            _a.set_filter([])

            self.manager.favorites.favorites[_a.value] = _a
        else:
            self.manager.favorites.remove_favorite(self.namespaceid)

        self.manager.favorites.save_favorites()
