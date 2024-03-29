from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.header import Header


class NamespacesScreen(Screen):
    namespaces_list = ObjectProperty(None)
    btn_create = Nwbutton()
    header = Header()

    def __init__(self, **kwargs):
        super(NamespacesScreen, self).__init__(**kwargs)

        self.app = App.get_running_app()

    @staticmethod
    def _sort(item):
        return item['shortcode']

    def populate(self):
        self.header.value = self.manager.wallet_screen.header.value
        self.namespaces_list.scroll_y = 1
        self.namespaces_list.data = []
        _w = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return

        if _w.kind == EWalletKind.NORMAL:
            self.btn_create.disabled = False
        else:
            self.btn_create.disabled = True

        _nsl = []
        for _n in _w.namespaces:
            if _n['namespaceid'] in self.manager.favorites.favorites:
                _fav = 'narwhallet/core/kui/assets/star_dark.png'
            else:
                _fav = 'narwhallet/core/kui/assets/star.png'
            _ns = {
            'address': _n['namespaceid'],
            'shortcode': str(_n['shortcode']),
            'keys': str(_n['keys']),
            'sm': self.manager,
            'ns_name': str(_n['name']),
            'favorite_source': _fav}
            _nsl.append(_ns)

        _nsl.sort(reverse=True, key=self._sort)        
        self.namespaces_list.data = _nsl
        self.manager.current = 'namespaces_screen'
