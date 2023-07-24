from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class PendingScreen(Screen):
    pending_offers = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = 'My Pending Offers'
        self.manager.current = 'pending_screen'