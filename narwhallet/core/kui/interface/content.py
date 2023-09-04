from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr


class ContentScreen(Screen):
    content_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('Keavcoin Content')
        self.manager.current = 'content_screen'
