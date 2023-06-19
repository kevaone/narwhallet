from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class PendingScreen(Screen):
    wallet_list = ObjectProperty(None)
