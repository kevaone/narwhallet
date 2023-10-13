from kivy.uix.screenmanager import Screen
from narwhallet.core.kui.widgets.header import Header

class AboutScreen(Screen):
    header = Header()

    def populate(self):
        self.header.value = 'About'
        self.manager.current = 'about_screen'
