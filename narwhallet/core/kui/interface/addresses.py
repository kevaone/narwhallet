from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, ColorProperty)
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from kivy.graphics import Color, Rectangle


class AddressesScreen(Screen):
    address_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AddressesScreen, self).__init__(**kwargs)

    def populate(self, wallet_name):
        self.address_list.clear_widgets()
        
        _w = self.manager.wallets.get_wallet_by_name(wallet_name.text)

        if _w is not None:
            for address in _w.addresses.addresses:
                if address is not None:
                    _a = AddressListInfo()
                    _a.address.text = address.address
                    _a.address_label.text = address.label
                    _a.balance.text = str(address.balance)
                    _a.transactions.text = str(len(address.history))
                    _a.wallet_name = wallet_name
                    _a.sm = self.manager

                    with _a.canvas:
                        Color(rgba=(125/255, 127/255, 127/255, 1))
                        # Color(1, 0, 0, 1)  # set the colour to red
                        # Rectangle(pos=self.pos,
                        #           size=(self.size))
                    # _a.canvas.ask_update()
                    self.address_list.add_widget(_a)
            for address in _w.change_addresses.addresses:
                if address is not None:
                    _a = AddressListInfo()
                    _a.address.text = address.address
                    _a.address_label.text = address.label
                    _a.balance.text = str(address.balance)
                    _a.transactions.text = str(len(address.history))
                    _a.wallet_name = wallet_name
                    _a.sm = self.manager

                    with _a.canvas:
                        Color(rgba=(0, 1, 0, 1))
                        self.rect = Rectangle(pos=self.center,
                                  size=(self.width/2.,
                                        self.height/2.))
                    self.address_list.add_widget(_a)
        self.address_list.parent.scroll_y = 1
        self.manager.current = 'addresses_screen'
