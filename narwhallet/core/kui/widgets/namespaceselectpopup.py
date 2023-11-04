from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from narwhallet.core.ksc.utils import Ut


class NamespaceSelectPopup(ModalView):
    return_screen = StringProperty()
    namespaces = Spinner()
    wallets = Spinner()
    manager = ObjectProperty()
    btn_next = Nwbutton()

    def __init__(self, **kwargs):
        super(NamespaceSelectPopup, self).__init__(**kwargs)

        self.owners = {}
        self.reward_address = None
        self.key: bytes = b''

    def populate(self, manager, key, target_screen, reward_address=None):
        self.manager = manager
        self.key = key
        self.target_screen = target_screen
        self.reward_address = reward_address
        self.namespaces.values = []
        self.namespaces.disabled = True
        self.btn_next.disabled = True
        
        _wallets = []
        for _w in self.manager.wallets.wallets:
            _wallets.append(_w.name)

        self.wallets.values = _wallets


    def wallet_changed(self):
        self.wallet = self.manager.wallets.get_wallet_by_name(self.wallets.text)
        if self.wallet is None:
            return

        _ns_list = []

        for address in self.wallet.addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])
                self.owners[ns['namespaceid']] = address.address

        for address in self.wallet.change_addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])
                self.owners[ns['namespaceid']] = address.address

        self.namespaces.values = _ns_list
        self.namespaces.disabled = False

    def ns_changed(self):
        if self.namespaces.text != '':
            self.btn_next.disabled = False

    def process_send(self):
        if self.target_screen == 'createnamespacekey_screen':
            if self.reward_address is not None:
                self.manager.createnamespacekey_screen.populate(self.wallet.name, self.reward_address)
            else:
                self.manager.createnamespacekey_screen.populate(self.wallet.name)

            self.manager.createnamespacekey_screen.namespace_key.text = Ut.bytes_to_hex(self.key)
            self.manager.createnamespacekey_screen.ns_key = self.key
            self.manager.createnamespacekey_screen.namespace_key.disabled = True
            self.manager.createnamespacekey_screen.namespace_name.text = self.namespaces.text
            self.manager.createnamespacekey_screen.namespace_address.text = self.owners[self.namespaces.text]

        self.manager.current = self.target_screen

        self.dismiss()
