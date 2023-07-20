from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class OffersScreen(Screen):
    bid_list = ObjectProperty(None)
    header = Header()

    def populate(self):
        self.header.value = 'My Offers'
        self.manager.current = 'offers_screen'