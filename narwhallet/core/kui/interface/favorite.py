from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class FavoriteScreen(Screen):
    namespaceid = ObjectProperty(None)
    shortcode = ObjectProperty(None)
    namespace_key_list = ObjectProperty(None)
    creator = ObjectProperty(None)
    namespace_name = ObjectProperty(None)
    header = Header()

    def populate(self, namespaceid):
        self.header.value = 'Favorite'
        self.namespace_key_list.scroll_y = 1
        # self.header.value = self.manager.wallet_screen.header.value
        self.namespace_key_list.data = []
        _ns = self.manager.cache.ns.get_namespace_by_id(namespaceid)
        self.namespaceid.text = namespaceid
        self.namespace_name.text = ''

        for ns in _ns:
            _dns = {} #NamespaceInfo()
            _dns['key'] = str(ns[5])
            _dns['data'] = str(ns[6])
            _dns['sm'] = self.manager

            if ns[4] == 'OP_KEVA_NAMESPACE':
                self.creator.text = ns[8]
                self.shortcode.text = str(len(str(ns[0]))) + str(ns[0]) + str(ns[1])
                if self.namespace_name.text == '':
                    self.namespace_name.text = ns[6]
            # elif ns[4] == 'OP_KEVA_PUT':
            if ns[5] == '\x01_KEVA_NS_':
                if self.namespace_name.text == '':
                    self.namespace_name.text = ns[6]
            
            self.owner.text = ns[8]
            
            self.namespace_key_list.data.append(_dns)
        self.manager.current = 'favorite_screen'
