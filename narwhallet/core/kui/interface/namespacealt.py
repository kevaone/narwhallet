import base64
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty)
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header


class NamespaceAltScreen(Screen):
    namespaceid = StringProperty()
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    # wallet_name = Nwlabel()
    # transfer_button = Image()
    header = Header()
    # nav_0 = Nwbutton()

    def populate(self, namespaceid):
        self.namespaceid = namespaceid
        # self.header.value = self.manager.wallet_screen.header.value
        self.namespace_key_list.clear_widgets()
        self.namespace_key_list.rows = 0

        # self.nav_0.bind(on_press=self.set_current)
        _ns = MShared.get_namespace_keys(namespaceid, self.manager.kex)
        for ns in _ns:
            _dns = NamespaceInfo()
            if ns['type'] == 'REG':
                self.creator.text = '' #ns[8]
                self.shortcode.text = '' #str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])

            # if ns[5] == '\x01_KEVA_NS_':
                # self.namespace_name.text = ns[6]
            try:
                _dns.key.text = base64.b64decode(ns['key']).decode()
            except:
                _dns.key.text = Ut.bytes_to_hex(base64.b64decode(ns['key']))
                
            if ns['type'] not in ('REG', 'DEL'):
                _dns.data.text = base64.b64decode(ns['value']).decode()
            else:
                _dns.data.text = ''
            self.owner.text = ''

            self.namespace_key_list.rows_minimum[self.namespace_key_list.rows] = 25 * len(str(_dns.data.text).split('\n'))
            self.namespace_key_list.rows += 1
            self.namespace_key_list.add_widget(_dns)

        self.manager.current = 'namespacealt_screen'
