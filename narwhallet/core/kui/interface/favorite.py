from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.nwnsimage import Nwnsimage
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class FavoriteScreen(Screen):
    namespaceid = Nwlabel()
    shortcode = Nwlabel()
    namespace_key_list = BoxLayout()
    creator = Nwlabel()
    namespace_name = Nwlabel()
    owner = Nwlabel()
    header = Header()

    def populate(self, namespaceid):
        self.header.value = 'Favorite'
        self.namespace_key_list.parent.scroll_y = 1
        self.namespace_key_list.clear_widgets()
        self.namespaceid.text = namespaceid
        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
        _ns = _ns['result']
        self.namespace_name.text = str(_ns['name'])
        self.shortcode.text = str(_ns['root_shortcode'])
        self.owner.text = ''
        self.creator.text = ''
        _dat = _ns['data']
        _dat.reverse()

        for _kv in _dat:
            _dns = NamespaceInfo()
            _dns.key = str(_kv['dkey'])
            _dns.data = str(_kv['dvalue'])
            _dns.sm = self.manager

            if self.owner.text == '':
                self.owner.text = _kv['addr']

            if _kv['op'] == 'KEVA_NAMESPACE':
                self.creator.text = _kv['addr']

            _ipfs_images = self.manager.cache_IPFS(_dns.data)
            
            self.namespace_key_list.add_widget(_dns)
            for _i in _ipfs_images:
                _im = Nwnsimage()
                _im.image_path = _i
                self.namespace_key_list.add_widget(_im)

            _ipfs_images = self.manager.cache_IPFS(_dns.data)
            
        self.manager.current = 'favorite_screen'
