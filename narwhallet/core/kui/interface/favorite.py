from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.namespaceinfoactionbar import NamespaceInfoActionBar
from narwhallet.core.kui.widgets.namespaceinfopopup import NamespaceInfoPopup
from narwhallet.core.kui.widgets.namespacereplyinfo import NamespaceReplyInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage


class FavoriteScreen(Screen):
    namespaceid = StringProperty()
    shortcode = StringProperty()
    namespace_key_list = BoxLayout()
    creator = StringProperty()
    namespace_name = StringProperty()
    owner = StringProperty()
    header = Header()
    favorite_source = StringProperty()
    info_button = Nwbutton()

    def populate(self, namespaceid):
        self.header.value = 'Favorite'
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid
        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
        _ns = _ns['result']
        self.namespace_name = str(_ns['name'])
        self.shortcode = str(_ns['root_shortcode'])
        self.header.value = self.shortcode + ' ' + self.namespace_name
        self.owner = ''

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        _dat = _ns['data']
        self.keys = len(_dat)
        _dat.reverse()

        for _kv in _dat:
            _dns = NamespaceInfo()
            _dns.key = str(_kv['dkey'])
            _dns.data = str(_kv['dvalue'])
            _dns.sm = self.manager

            _ns_action_bar = NamespaceInfoActionBar()
            _ns_action_bar.txid = str(_kv['txid'])
            _ns_action_bar.addr = str(_kv['addr'])
            _ns_action_bar.sm = self.manager

            if self.owner == '':
                self.owner = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator = _kv['addr']

            _ipfs_images = self.manager.cache_IPFS(_dns.data)
                        
            for _i in _ipfs_images:
                _im = Nwnsimage()
                _dns.data =_dns.data.replace(_i[0], '')
                _im.image_path = _i[2]
                _im.image.bind(size=_im.on_size)
                _dns.add_widget(_im)

            _dns.add_widget(_ns_action_bar)

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

                _dns.add_widget(_nsi)
            self.namespace_key_list.add_widget(_dns)
            
        self.manager.current = 'favorite_screen'

    def info_popup(self):
        _nsi = NamespaceInfoPopup()
        _nsi.namespaceid._text = self.namespaceid
        _nsi.header.value = self.header.value
        _nsi.header.is_popup = True
        _nsi.namespace_name._text = self.namespace_name
        _nsi.shortcode._text = self.shortcode
        _nsi.owner._text = self.owner
        _nsi.creator._text = self.creator
        _nsi.manager = self.manager
        _nsi.open()

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