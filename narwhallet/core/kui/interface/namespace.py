from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.metrics import dp
from kivy.app import App
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.namespaceinfoactionbar import NamespaceInfoActionBar
from narwhallet.core.kui.widgets.namespacereplyinfo import NamespaceReplyInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage
from narwhallet.core.kui.widgets.namespaceinfopopup import NamespaceInfoPopup


class NamespaceScreen(Screen):
    namespace_key_list = ObjectProperty(None)
    namespace_name = StringProperty(None)
    namespaceid = StringProperty(None)
    owner = StringProperty(None)
    creator = StringProperty(None)
    shortcode = StringProperty(None)
    transfer_button = Nwbutton()
    auction_button = Nwbutton()
    name_update_button = Nwbutton()
    btn_create = Nwbutton()
    info_button = Nwbutton()
    header = Header()
    favorite_source = StringProperty()

    def __init__(self, **kwargs):
        super(NamespaceScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    def populate(self, namespaceid):
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid = namespaceid

        _w = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return

        if _w.kind == EWalletKind.NORMAL:
            self.btn_create.disabled = False
            self.transfer_button.disabled = False
            self.auction_button.disabled = False
            self.name_update_button.disabled = False
            self.transfer_button.size = (dp(30), dp(30))
            self.auction_button.size = (dp(30), dp(30))
        else:
            self.btn_create.disabled = True
            self.transfer_button.disabled = True
            self.auction_button.disabled = True
            self.name_update_button.disabled = True
            self.transfer_button.size = (0, 0)
            self.auction_button.size = (0, 0)

        if namespaceid in self.manager.favorites.favorites:
            self.favorite_source = 'narwhallet/core/kui/assets/star_dark.png'
        else:
            self.favorite_source = 'narwhallet/core/kui/assets/star.png'

        _ns = MShared.get_namespace(namespaceid, self.app.ctrl.kex)
        _ns = _ns['result']
        self.namespace_name = str(_ns['name'])
        self.header.value = str(_ns['root_shortcode']) + ' ' + self.namespace_name
        self.shortcode = str(_ns['root_shortcode'])

        _dat = _ns['data']
        self.keys = len(_dat)
        _dat.reverse()
        self.owner = ''
        for _kv in _dat:
            _xdns = NamespaceInfo()
            _ns_action_bar = NamespaceInfoActionBar()
            _xdns.key = str(_kv['dkey'])
            _xdns.data = str(_kv['dvalue'])
            _xdns.txid = str(_kv['txid'])
            _ns_action_bar.txid = str(_kv['txid'])
            # NOTE Currently using the address assosiated with the
            # specific key output. This may differ from current
            # namespace owner address.
            _xdns.addr = str(_kv['addr'])
            _ns_action_bar.addr = str(_kv['addr'])
            _xdns.sm = self.manager
            _ns_action_bar.sm = self.manager

            if self.owner == '':
                self.owner = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator = _kv['addr']

            _ipfs_images = self.manager.cache_IPFS(_xdns.data)

            for _i in _ipfs_images:
                _xdns.data =_xdns.data.replace(_i[0], '')
                _im = Nwnsimage()
                _im.image_path = _i[2]
                _im.image.bind(size=_im.on_size)
                _xdns.add_widget(_im)

            _xdns.add_widget(_ns_action_bar)

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

                _xdns.add_widget(_nsi)

            self.namespace_key_list.add_widget(_xdns)

        self.manager.current = 'namespace_screen'

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

    def transfer_namespace(self):
        self.manager.transfernamespace_screen.populate()

    def auction_namespace(self):
        self.manager.auctionnamespace_screen.populate()

    def update_namespace_name(self):
        self.manager.editnamespace_screen.populate()

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
            _a.set_id(self.namespaceid)
            _a.set_coin('KEVACOIN')
            _a.set_kind('Namespace')
            _a.set_value([self.namespaceid, self.shortcode, self.namespace_name, self.keys])
            _a.set_filter([])

            self.manager.favorites.favorites[_a.id] = _a
        else:
            self.manager.favorites.remove_favorite(self.namespaceid)

        self.manager.favorites.save_favorites()