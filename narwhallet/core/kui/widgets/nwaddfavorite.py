import json
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.textinput import TextInput
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder
from narwhallet.core.kcl.favorites.favorite import MFavorite
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class Nwaddfavorite(ModalView):
    namespace = TextInput()
    btn_next = Nwbutton()
    next = BooleanProperty(False)
    sm = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Nwaddfavorite, self).__init__(**kwargs)

        self.app = App.get_running_app()
        self.kind: int = -1

    def on_next_click(self, *args):
        if self.kind == 0:
            _ns = MShared.get_shortcode(self.namespace.text, self.app.ctrl.kex)
        elif self.kind == 1:
            _ns = MShared.get_namespace(self.namespace.text, self.app.ctrl.kex)

        if _ns is None:
            self.btn_next.disabled = True
            self.kind = 0
            return

        if _ns.social_name != '':
            _name = str(_ns.social_name)
        else:
            _name = str(_ns.name)

        _favorite = _ns.namespaceid
        _shortcode = _ns.shortcode
        _keys = len(_ns.keys.keys)

        _a = MFavorite()
        _a.set_id(_favorite)
        _a.set_coin('KEVACOIN')
        _a.set_kind('Namespace')
        _a.set_value([_favorite, _shortcode, _name, _keys])
        _a.set_filter([])

        self.sm.favorites.favorites[_a.id] = _a
        self.sm.favorites.save_favorites()
        self.next = True

    def on_next(self, *args):
        self.dismiss()

    def on_open(self, *args):
        self.namespace.focus = True

    def verify(self):
        # Test if shortcode
        try:
            _ = int(self.namespace.text)
            if len(self.namespace.text) - 1 > int(self.namespace.text[0]):
                self.btn_next.disabled = False
                self.kind = 0
                return
            self.btn_next.disabled = True
            self.kind = 0
            return
        except:
            # Test if namespace id
            try:
                _ = Base58Decoder.CheckDecode(self.namespace.text)
                self.btn_next.disabled = False
                self.kind = 1
                return
            except:
                self.btn_next.disabled = True
                self.kind = 0

    def on_enter(self, *args):
        if self.btn_next.disabled is False:
            self.on_next_click()
