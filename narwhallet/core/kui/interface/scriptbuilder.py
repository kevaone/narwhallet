from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from narwhallet.core.kcl.wallet import MWallet
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.nwboxlayout import Nwboxlayout
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from kivy.properties import ObjectProperty
from narwhallet.core.kui.widgets.header import Header


class ScriptBuilderScreen(Screen):
    build_grid = GridLayout()
    header = Header()
    # mnemonic_phrase = Nwlabel()
    # seed = Nwlabel()
    # ypub = Nwlabel()
    # xpriv = Nwlabel()
    # coin = Nwlabel()
    # bip = Nwlabel()
    # kind = Nwlabel()
    # account_index = Nwlabel()
    # change_index = Nwlabel()
    # balance = Nwlabel()
    # locked_balance = Nwlabel()
    # last_updated = Nwlabel()

                # Nwboxlayout:
                #     size_hint_y: None
                #     height: 20

                #     Nwlabel:
                #         halign: 'left'
                #         text: 'Wallet Name:'
                #         text_size: self.size
                #         size_hint_x: None
                #         width: 150

                #     Nwlabel:
                #         id: wallet_name
                #         halign: 'left'
                #         text: ''
                #         text_size: self.size

    def populate(self, script):
        # TODO Create widgets to better enable making simple schema; hard code for now
        if script == 'create_namespace':
            _box_1 = Nwboxlayout()
            _box_2 = Nwboxlayout()
            _box_3 = Nwboxlayout()
            _box_4 = Nwboxlayout()
            _box_1.size_hint_y = None
            _box_1.height = 20
            _box_2.size_hint_y = None
            _box_2.height = 20
            _box_3.size_hint_y = None
            _box_3.height = 35
            _box_4.size_hint_y = None
            _box_4.height = 35
            _box_4_button_1 = Nwbutton()
            _box_1_label_1 = Nwlabel()
            _box_2_label_1 = Nwlabel()
            _box_3_textinput_1 = TextInput()
            _box_1_label_1.text = 'Create Namespace'
            _box_2_label_1.text = 'Name:'
            _box_4_button_1.text = 'Create'
            _box_1.add_widget(_box_1_label_1)
            _box_2.add_widget(_box_2_label_1)
            _box_3.add_widget(_box_3_textinput_1)
            _box_4.add_widget(_box_4_button_1)

            self.build_grid.add_widget(_box_1)
            self.build_grid.add_widget(_box_2)
            self.build_grid.add_widget(_box_3)
            self.build_grid.add_widget(_box_4)
        elif script == 'create_namespace_key':
            _box_1 = Nwboxlayout()
            _box_2 = Nwboxlayout()
            _box_3 = Nwboxlayout()
            _box_4 = Nwboxlayout()
            _box_5 = Nwboxlayout()
            _box_6 = Nwboxlayout()
            _box_1.size_hint_y = None
            _box_1.height = 20
            _box_2.size_hint_y = None
            _box_2.height = 20
            _box_3.size_hint_y = None
            _box_3.height = 35
            _box_4.size_hint_y = None
            _box_4.height = 35
            _box_5.size_hint_y = None
            _box_5.height = 65
            _box_6.size_hint_y = None
            _box_6.height = 35
            _box_6_button_1 = Nwbutton()
            _box_1_label_1 = Nwlabel()
            _box_2_label_1 = Nwlabel()
            _box_3_textinput_1 = TextInput()
            _box_4_label_1 = Nwlabel()
            _box_5_textinput_1 = TextInput()
            _box_1_label_1.text = 'Create Key'
            _box_2_label_1.text = 'Key:'
            _box_4_label_1.text = 'Value:'
            _box_6_button_1.text = 'Create'
            _box_1.add_widget(_box_1_label_1)
            _box_2.add_widget(_box_2_label_1)
            _box_3.add_widget(_box_3_textinput_1)
            _box_5.add_widget(_box_5_textinput_1)
            _box_6.add_widget(_box_6_button_1)

            self.build_grid.add_widget(_box_1)
            self.build_grid.add_widget(_box_2)
            self.build_grid.add_widget(_box_3)
            self.build_grid.add_widget(_box_4)
            self.build_grid.add_widget(_box_5)
            self.build_grid.add_widget(_box_6)

        self.manager.current = 'scriptbuilder_screen'

    def clear_screen(self):
        self.build_grid.clear_widgets()
        self.manager.current = 'namespaces_screen'
