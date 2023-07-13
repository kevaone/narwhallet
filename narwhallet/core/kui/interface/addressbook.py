from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.addressbooklistinfo import AddressBookListInfo
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class AddressBookScreen(Screen):
    address_list = GridLayout()
    nav0 = Nwbutton()
    header = Header()

    def __init__(self, **kwargs):
        super(AddressBookScreen, self).__init__(**kwargs)

        self.is_populated = False
        self.mode = 0

    def set_current(self, button: Nwbutton):
        if self.mode == 0:
            self.manager.current = 'home_screen'
        elif self.mode == 1:
            self.manager.current = 'send_screen'
        elif self.mode == 2:
            self.manager.current = 'transfernamespace_screen'

    def populate(self, _mode=0):
        self.mode = _mode
        self.address_list.data = []
        if _mode == 0:
            self.nav0.text = 'Home'
            self.nav0.icon = 'narwhallet/core/kui/assets/home_white.png'
            self.nav0.bind(on_press=self.set_current)
        elif _mode == 1:
            self.nav0.text = 'Cancel'
            self.nav0.icon = ''
            
            self.nav0.bind(on_press=self.set_current)
        elif _mode == 2:
            self.nav0.text = 'Cancel'
            self.nav0.icon = ''
            self.nav0.bind(on_press=self.set_current)
        
        try:
            _book = self.manager.address_book.to_dict_list()

            for _entry in _book:
                _a = {
                'mode': _mode,
                'address': _entry['address'],
                'address_name': _entry['name'],
                'address_label': _entry['label'],
                'coin': _entry['coin'],
                'sent': str(_entry['sent']),
                'received': str(_entry['received']),
                'sm': self.manager}
                self.address_list.data.append(_a)
            
        except Exception:
            print('Error Loading address book')

        self.address_list.scroll_y = 1
        self.manager.current = 'addressbook_screen'

    def add_address(self):
        self.manager.addaddressbookentry_screen.populate()