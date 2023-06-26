from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo


class NamespaceScreen(Screen):
    namespaceid = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)

    def populate(self, namespaceid):
        self.namespace_key_list.clear_widgets()
        self.namespace_key_list.rows = 0
        _ns = self.manager.cache.ns.get_namespace_by_id(namespaceid)
        self.namespaceid.text = namespaceid

        for ns in _ns:
            _dns = NamespaceInfo()
            if ns[4] == 'OP_KEVA_NAMESPACE':
                self.creator.text = ns[8]
                self.shortcode.text = str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])
            # elif ns[4] == 'OP_KEVA_PUT':
            if ns[5] == '\x01_KEVA_NS_':
                self.namespace_name.text = ns[6]
            _dns.key.text = ns[5]
            _dns.data.text = ns[6]
            self.owner.text = ns[8]
            
            self.namespace_key_list.rows_minimum[self.namespace_key_list.rows] = 25 * len(ns[6].split('\n'))
            self.namespace_key_list.rows += 1
            self.namespace_key_list.add_widget(_dns)

        self.manager.current = 'namespace_screen'