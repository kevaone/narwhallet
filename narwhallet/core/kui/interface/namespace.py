from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage


class NamespaceScreen(Screen):
    namespaceid = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    owner = Nwlabel()
    transfer_button = Image()
    auction_button = Image()
    btn_create = Nwbutton()
    header = Header()

    def populate(self, namespaceid):
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.header.value = self.manager.wallet_screen.header.value
        self.namespaceid.text = namespaceid
        
        _w = self.manager.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return

        if _w.kind == EWalletKind.NORMAL:
            self.btn_create.disabled = False
            self.transfer_button.size = (dp(30), dp(30))
            self.auction_button.size = (dp(30), dp(30))
        else:
            self.btn_create.disabled = True
            self.transfer_button.size = (0, 0)
            self.auction_button.size = (0, 0)

        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
        _ns = _ns['result']
        self.namespace_name.text = str(_ns['name'])
        self.shortcode.text = str(_ns['root_shortcode'])
        self.owner.text = ''
        self.creator.text = ''

        _dat = _ns['data']
        _dat.reverse()
        for _kv in _dat:
            _xdns = NamespaceInfo()
            _xdns.key = str(_kv['dkey'])
            _xdns.data = str(_kv['dvalue'])
            _xdns.sm = self.manager

            if self.owner.text == '':
                self.owner.text = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator.text = _kv['addr']

            _ipfs_images = self.manager.cache_IPFS(_xdns.data)
            
            self.namespace_key_list.add_widget(_xdns)
            for _i in _ipfs_images:
                _im = Nwnsimage()
                _im.image_path = _i
                self.namespace_key_list.add_widget(_im)
            # self.namespace_key_list.data.append(_dns)
        self.manager.current = 'namespace_screen'

    def transfer_namespace(self):
        self.manager.transfernamespace_screen.populate()

    def auction_namespace(self):
        self.manager.auctionnamespace_screen.populate()

    def update_namespace_name(self):
        self.manager.createnamespacekey_screen.populate()
        self.manager.createnamespacekey_screen.namespace_key.text = '\x01_KEVA_NS_'
        self.manager.createnamespacekey_screen.namespace_key.disabled = True
        self.manager.createnamespacekey_screen.namespace_value.text = self.namespace_name.text
