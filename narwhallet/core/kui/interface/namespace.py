from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header


class NamespaceScreen(Screen):
    namespaceid = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    # wallet_name = Nwlabel()
    transfer_button = Image()
    header = Header()

    def populate(self, namespaceid):
        self.namespace_key_list.scroll_y = 1
        # self.namespace_key_list.children[0].default_size = None, None
        # self.namespace_key_list.children[0].height = self.namespace_key_list.children[0].minimum_height
        self.header.value = self.manager.wallet_screen.header.value
        self.namespace_key_list.data = []
        _ns = self.manager.cache.ns.get_namespace_by_id(namespaceid)
        self.namespaceid.text = namespaceid

        for ns in _ns:
            _dns = {} #NamespaceInfo()
            _dns['key'] = str(ns[5])
            _dns['data'] = str(ns[6])
            _dns['sm'] = self.manager

            if ns[4] == 'OP_KEVA_NAMESPACE':
                self.creator.text = ns[8]
                self.shortcode.text = str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])
            # elif ns[4] == 'OP_KEVA_PUT':
            if ns[5] == '\x01_KEVA_NS_':
                self.namespace_name.text = ns[6]
            
            self.owner.text = ns[8]
            
            self.namespace_key_list.data.append(_dns)
        self.manager.current = 'namespace_screen'

    def transfer_namespace(self):
        self.manager.transfernamespace_screen.populate()