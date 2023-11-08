from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from narwhallet.core.kcl.addr_book.book_address import MBookAddress
from narwhallet.core.kui.widgets.header import Header


class AddAddressBookEntryScreen(Screen):
    address = TextInput()
    address_name = TextInput()
    label = TextInput()
    coin = Spinner()
    header = Header()

    def populate(self):
        self.reset_screen()
        self.manager.current = 'addaddressbookentry_screen'

    def on_enter(self, *args):
        self.address.focus = True

    def reset_screen(self):
        self.address.text = ''
        self.address_name.text = ''
        self.label.text = ''

    def cancel(self):
        self.reset_screen()
        self.manager.current = 'addressbook_screen'

    def add_entry(self):
        # TODO Validate inputs
        _a = MBookAddress()
        _a.set_address(self.address.text)
        _a.set_name(self.address_name.text)
        _a.set_label(self.label.text)

        self.manager.address_book.addresses[_a.address] = _a
        self.manager.address_book.save_address_book()

        self.reset_screen()
        self.manager.addressbook_screen.mode
        self.manager.addressbook_screen.populate(self.manager.addressbook_screen.mode)
