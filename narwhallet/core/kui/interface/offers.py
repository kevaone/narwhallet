from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kui.widgets.header import Header


class OffersScreen(Screen):
    wallet_list = ObjectProperty(None)
    header = Header()
