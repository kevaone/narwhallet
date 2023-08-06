from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage


class NamespaceScreen(Screen):
    namespaceid = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    # wallet_name = Nwlabel()
    transfer_button = Image()
    auction_button = Image()
    btn_create = Nwbutton()
    header = Header()

    def populate(self, namespaceid):
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.header.value = self.manager.wallet_screen.header.value
        _ns = self.manager.cache.ns.get_namespace_by_id(namespaceid)
        self.namespaceid.text = namespaceid
        self.namespace_name.text = ''
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

        for ns in _ns:
            _xdns = NamespaceInfo()
            _xdns.key = str(ns[5])
            _xdns.data = str(ns[6])
            _xdns.sm = self.manager

            if ns[4] == 'OP_KEVA_NAMESPACE':
                self.creator.text = ns[8]
                self.shortcode.text = str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])
            # elif ns[4] == 'OP_KEVA_PUT':
            if ns[5] == '\x01_KEVA_NS_' or ns[5] == '_KEVA_NS_':
                if self.namespace_name.text == '':
                    self.namespace_name.text = ns[6]

            # NOTE: Key list is newest to oldest; be aware of owner if sort changes
            # Possible to set via ns cache last_address at expense of extra query.
            if self.owner.text == '':
                self.owner.text = ns[8]
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
