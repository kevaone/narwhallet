from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.namespaceselectpopup import NamespaceSelectPopup


class NamespaceInfo(BoxLayout):
    key = StringProperty()
    data = StringProperty()
    txid = StringProperty()
    addr = StringProperty()
    sm = ObjectProperty(None)
    background_color = ListProperty()
    hover = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(NamespaceInfo, self).__init__(**kwargs)

        # Window.bind(mouse_pos=self.on_mouse_pos)

    def sizer(self):
        height = 0
        for child in self.children:
            height += child.size[1]
        self.height = height

    def on_mouse_pos(self, window, pos):
        if self.collide_point(pos[0], pos[1]):
            if self.hover is False:
                self.background_color = [146/255, 149/255, 149/255, 1]
                self.hover = True
        else:
            if self.hover is True:
                self.background_color = [54/255, 58/255, 59/255, 1]
                self.hover = False

    def namespace_select_popup(self, action):
        _nsi = NamespaceSelectPopup()
        if action == 1:
            _key = (Ut.hex_to_bytes('0001') + Ut.hex_to_bytes(self.txid))
        elif action == 2:
            _key = (Ut.hex_to_bytes('0002') + Ut.hex_to_bytes(self.txid))
        elif action == 3:
            _key = (Ut.hex_to_bytes('0003') + Ut.hex_to_bytes(self.txid))
        else:
            # NOTE Bad action, just return for now
            return
        
        if action == 3:
            _nsi.populate(self.sm, _key, 'createnamespacekey_screen', self.addr)
        else:    
            _nsi.populate(self.sm, _key, 'createnamespacekey_screen')

        app = App.get_running_app()
        if app.ctrl.settings.default_wallet != '':
            _nsi.wallets.text = app.ctrl.settings.default_wallet

        if app.ctrl.settings.default_namespace[0] != '':
            _nsi.namespaces.text = app.ctrl.settings.default_namespace[0]
            _nsi.owners[app.ctrl.settings.default_namespace[0]] = app.ctrl.settings.default_namespace[1]
            _nsi.process_send()
        else:
            _nsi.open()
