from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui import _translate as _tr

class AboutScreen(Screen):
    header = Header()

    def populate(self):
        self.header.value = _tr.translate('About')
        self.manager.current = 'about_screen'
