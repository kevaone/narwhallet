from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class BlockScreen(Screen):
    header = Header()
