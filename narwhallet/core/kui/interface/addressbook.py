from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from narwhallet.core.kui.widgets.addressbooklistinfo import AddressBookListInfo


class AddressBookScreen(Screen):
    address_list = GridLayout()

    def __init__(self, **kwargs):
        super(AddressBookScreen, self).__init__(**kwargs)

    def populate(self):
        self.address_list.clear_widgets()
        
        try:
            self.manager.address_book.load_address_book(self.manager.user_path)
            
            _book = self.manager.address_book.to_dict_list()

            for _entry in _book:
                _a = AddressBookListInfo()
                _a.address.text = _entry['address']
                _a.address_name.text = _entry['name']
                _a.address_label.text = _entry['label']
                _a.coin.text = _entry['coin']
                _a.balance.text = str(_entry['received'] - _entry['sent'])
                _a.sent.text = str(_entry['sent'])
                _a.received.text = str(_entry['received'])

                _a.sm = self.manager
                self.address_list.add_widget(_a)
            
        except Exception:
            print('Error Loading address book')

        self.address_list.parent.scroll_y = 1
        self.manager.current = 'addressbook_screen'
