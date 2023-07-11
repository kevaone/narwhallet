from kivy.uix.screenmanager import Screen
from narwhallet.core.kcl.wallet import MWallet
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class UtilsScreen(Screen):
    wallet_name = Spinner()
    address = Spinner()
    file = Nwlabel()
    mnemonic = TextInput()
    _w = MWallet()
    header = Header()

    def __init__(self, **kwargs):
        super(UtilsScreen, self).__init__(**kwargs)

    def populate(self):
        self.reset_screen()
        self.manager.current = 'utils_screen'

    def return_home(self):
        self.reset_screen()
        self.manager.current = 'home_screen'

    def reset_screen(self):
        pass
