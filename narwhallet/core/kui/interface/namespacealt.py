import base64
import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwimage import Nwimage
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage
from narwhallet.core.kcl.favorites.favorite import MFavorite


class NamespaceAltScreen(Screen):
    namespaceid = StringProperty()
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    header = Header()
    favorite = Nwimage()
    favorite_source = StringProperty()

    def populate(self, namespaceid, shortcode):
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid
        self.shortcode.text = shortcode
        self.namespace_name.text = ''
        _ns = MShared.get_namespace_keys(namespaceid, self.manager.kex)

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'

        for ns in _ns:
            _ins = NamespaceInfo()
            if ns['type'] == 'REG':
                self.creator.text = ''

                if self.namespace_name.text == '':
                    self.namespace_name.text = base64.b64decode(ns['key']).decode()
            try:
                _ins.key = base64.b64decode(ns['key']).decode()

                if _ins.key == '\x01_KEVA_NS_':
                    if self.namespace_name.text == '':
                        try:
                            _k = json.loads(base64.b64decode(ns['value']).decode())['displayName']
                            self.namespace_name.text = _k
                        except:
                            self.namespace_name.text = base64.b64decode(ns['value']).decode()
            except:
                _ins.key = Ut.bytes_to_hex(base64.b64decode(ns['key']))
                
            if ns['type'] not in ('REG', 'DEL'):
                _ins.data = base64.b64decode(ns['value']).decode()
            else:
                _ins.data = ''
            self.owner.text = ''

            _ipfs_images = self.manager.cache_IPFS(_ins.data)
            self.namespace_key_list.add_widget(_ins)
            for _i in _ipfs_images:
                _im = Nwnsimage()
                _im.image_path = _i
                _im.image.texture_update()
                print('_im', _im.size, _im.minimum_height)
                self.namespace_key_list.add_widget(_im)

        self.manager.current = 'namespacealt_screen'

    def bid_namespace(self):
        self.manager.bidnamespace_screen.populate(self.namespaceid)

    def on_touch_down(self, touch):
        if self.favorite.collide_point(touch.x, touch.y) and touch.is_mouse_scrolling is False:
            self.set_favorite()
            return
        return super(NamespaceAltScreen, self).on_touch_down(touch)

    def set_favorite(self):
        _add_fav = False
        if self.favorite_source == 'narwhallet/core/kui/assets/star_dark.png':
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'
            _add_fav = True
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'

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