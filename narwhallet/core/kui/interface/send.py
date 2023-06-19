from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)


class SendScreen(Screen):
    wallet_name = ObjectProperty(None)
    send_to = ObjectProperty(None)
    send_amount = ObjectProperty(None)
