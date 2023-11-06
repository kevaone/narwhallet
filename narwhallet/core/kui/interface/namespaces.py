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

    def populate(self):
        self.header.value = self.manager.wallet_screen.header.value
        self.namespaces_list.scroll_y = 1
        self.namespaces_list.data = []
        app = App.get_running_app()
        _w = app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        if _w is None:
            return

        if _w.kind == EWalletKind.NORMAL:
            self.btn_create.disabled = False
        else:
            self.btn_create.disabled = True

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
            self.namespaces_list.data.append(_ns)

        self.manager.current = 'namespaces_screen'
