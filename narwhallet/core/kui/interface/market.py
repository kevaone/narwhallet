from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class MarketScreen(Screen):
    wallet_list = ObjectProperty(None)
    header = Header()
