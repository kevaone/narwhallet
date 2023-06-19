from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class OffersScreen(Screen):
    wallet_list = ObjectProperty(None)
