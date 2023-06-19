from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class MarketScreen(Screen):
    wallet_list = ObjectProperty(None)
