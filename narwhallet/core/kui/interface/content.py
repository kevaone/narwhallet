from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class ContentScreen(Screen):
    content_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = 'Keavcoin Content'
        self.manager.current = 'content_screen'