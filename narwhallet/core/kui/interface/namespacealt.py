import base64
import json
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
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

    def populate(self, namespaceid, shortcode):
        self.namespace_key_list.scroll_y = 1
        self.namespace_key_list.data = []
        self.namespaceid = namespaceid
        self.shortcode.text = shortcode
        self.namespace_name.text = ''
        # self.header.value = self.manager.wallet_screen.header.value
        # self.namespace_key_list.clear_widgets()
        # self.namespace_key_list.rows = 0

        # self.nav_0.bind(on_press=self.set_current)
        _ns = MShared.get_namespace_keys(namespaceid, self.manager.kex)
        # _ns.reverse()
        # for ns in _ns:
        #     _key = base64.b64decode(ns['key']).decode()
        #     print('_dns[key]', _key, ns['type'])
        #     if _key == '\x01_KEVA_NS_':
        #         self.namespace_name.text = base64.b64decode(ns['value']).decode()
        # _ns.reverse()
        for ns in _ns:
            _dns = {} #NamespaceInfo()
            if ns['type'] == 'REG':
                self.creator.text = '' #ns[8]
                # self.shortcode.text = '' #str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])

            # if ns[5] == '\x01_KEVA_NS_':
                if self.namespace_name.text == '':
                    self.namespace_name.text = base64.b64decode(ns['key']).decode()
            try:
                _dns['key'] = base64.b64decode(ns['key']).decode()
                # print('_dns[key]', _dns['key'])
                if _dns['key'] == '\x01_KEVA_NS_':
                    if self.namespace_name.text == '':
                        try:
                            _k = json.loads(base64.b64decode(ns['value']).decode())['displayName']
                            self.namespace_name.text = _k
                        except:
                            self.namespace_name.text = base64.b64decode(ns['value']).decode()
            except:
                _dns['key'] = Ut.bytes_to_hex(base64.b64decode(ns['key']))
                
            if ns['type'] not in ('REG', 'DEL'):
                _dns['data'] = base64.b64decode(ns['value']).decode()
            else:
                _dns['data'] = ''
            self.owner.text = ''

            self.manager.cache_IPFS(_dns['data'])
            self.namespace_key_list.data.append(_dns)

        self.manager.current = 'namespacealt_screen'

    def bid_namespace(self):
        pass
