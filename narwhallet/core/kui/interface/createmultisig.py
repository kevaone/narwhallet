from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.app import App
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder
from narwhallet.core.kcl.wallet.address import MAddress
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.ksc import Scripts
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwboxlayout import Nwboxlayout


class CreateMultiSigScreen(Screen):
    address = Nwlabel()
    address_label = Nwlabel()
    header = Header()
    btn_create = Nwbutton()
    public_keys = TextInput()
    required_signatures = TextInput()
    from_redeem = CheckBox()
    public_key_data = Nwboxlayout()
    redeem_script_data = Nwboxlayout()
    redeem_script = TextInput()
    display_box = Nwboxlayout()
    preview = TextInput()
    preview_label = Nwlabel()

    def __init__(self, **kwargs):
        super(CreateMultiSigScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        self._address_indexes = []
        self._redeem_script = ''
        self.app = App.get_running_app()

    def populate(self):
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self.header.value = self.manager.wallet_screen.header.value
        self.from_redeem.active = True
        self.btn_create.disabled = True
        self.address.text = ''
        self.preview.text = ''
        self.redeem_script.text = ''
        self.required_signatures.text = ''
        self.public_keys.text = ''
        self._address_indexes = []
        self._redeem_script = ''
        self.manager.current = 'createmultisig_screen'

    def input_filter(self, string, from_undo):
        try:
            int(string)
            return string
        except ValueError:
            return ''

    def on_from_redeem_active(self):
        self.address.text = ''
        self.preview.text = ''
        self._address_indexes = []
        self._redeem_script = ''
        self.btn_create.disabled = True
        if self.from_redeem.active:
            self.required_signatures.disabled = True
            self.public_keys.disabled = True
            self.redeem_script.text = ''
            self.required_signatures.text = ''
            self.public_keys.text = ''
            self.preview_label._text = 'Public Keys' + self.app.translate_text(':')
            self.redeem_script_data.opacity = 1
            self.public_key_data.opacity = 0
            self.display_box.height = dp(610)
            self.redeem_script_data.height = dp(170)
            self.public_key_data.height = dp(0)
            for c in self.redeem_script_data.children:
                c.size_hint_y = 1
            
            for c in range(0, len(self.public_key_data.children)):
                self.public_key_data.remove_widget(self.public_key_data.children[0])

            self.redeem_script_data.children[0].size_hint_y = None
            self.redeem_script_data.children[0].height = dp(150)
        else:
            self.required_signatures.disabled = False
            self.public_keys.disabled = False
            self.redeem_script.text = ''
            self.required_signatures.text = ''
            self.public_keys.text = ''
            self.preview_label._text = 'Redeem Script' + self.app.translate_text(':')
            self.redeem_script_data.opacity = 0
            self.public_key_data.opacity = 1
            self.redeem_script_data.height = dp(0)
            self.public_key_data.height = dp(55) * len(self.public_key_data.children)
            self.display_box.height = dp(610) + (dp(55) * len(self.public_key_data.children))
            for c in self.redeem_script_data.children:
                c.size_hint_y = None
                c.height = dp(0)

    def set_public_keys(self):
        if self.from_redeem.active is False:
            if self.public_keys.text == '':
                return
            _keys = int(self.public_keys.text)
            _set_keys = len(self.public_key_data.children)

            if _set_keys > _keys:
                for _ in range(_set_keys - _keys):
                    self.public_key_data.remove_widget(self.public_key_data.children[0])

            for _p in range(_set_keys, _keys):
                _box = Nwboxlayout(size_hint_y=None, height=dp(55), orientation='vertical')
                _label_box = Nwboxlayout(size_hint_y=None, height=dp(20), orientation='horizontal')
                _label = Nwlabel(halign='left', _text='Public Key ' + str(_p + 1) + self.app.translate_text(':'),
                                text_size=self.size, padding=[10, 0, 0, 0], size_hint_x=None,
                                width=dp(225))

                _public_key_box = Nwboxlayout(size_hint_y=None, height=dp(35), orientation='vertical')
                _public_key = Nwboxlayout(size_hint_y=None, height=dp(30), orientation='horizontal')
                _public_key_box_hpad = Nwlabel(_text='', size_hint_x=None, width=dp(10))
                _public_key_input = TextInput(halign='left', _text='',
                                            text_size=self.size, size_hint_x=None,
                                            width=self.width - dp(40), write_tab=False)
                _public_key_input.bind(text=self.validate)
                _public_key_box_vpad = Nwboxlayout(size_hint_y=None, height=dp(5), orientation='horizontal')
                _label_box.add_widget(_label)
                _public_key.add_widget(_public_key_box_hpad)
                _public_key.add_widget(_public_key_input)
                _public_key_box.add_widget(_public_key)
                _public_key_box.add_widget(_public_key_box_vpad)
                _box.add_widget(_label_box)
                _box.add_widget(_public_key_box)
                self.public_key_data.add_widget(_box)
            self.public_key_data.height = dp(55) * len(self.public_key_data.children)
            self.display_box.height = dp(610) + (dp(55) * len(self.public_key_data.children))
            self.validate()

    def validate(self, *args):
        self.btn_create.disabled = True
        self.preview.text = ''
        self._redeem_script = ''
        self.address.text = ''
        self._address_indexes = []
        _public_keys = []

        if self.from_redeem.active:
            try:
                _script = Scripts.decompile(self.redeem_script.text)
                _req_sig = _script[0]
                _pubk = _script[-2]
            except:
                return

            if isinstance(_req_sig, int) is False:
                return

            if isinstance(_pubk, int) is False:
                return

            for _p in range(1, _pubk + 1):
                try:
                    _ = Ut.hex_to_bytes(_script[_p])
                except:
                    return

                if len(_script[_p]) != 66:
                    return

                _public_keys.append(_script[_p])
                self._address_indexes.append(self.wallet.get_account_address_index(_script[_p]))

            self.required_signatures.text = str(_req_sig)
            self.public_keys.text = str(_pubk)
            _, _redeem_script, _address = Scripts.P2SHMultisigScriptHash(_req_sig, _public_keys)

            if _redeem_script != self.redeem_script.text:
                return

            for _p in _public_keys:
                self.preview.text = self.preview.text + str(_p) + '\n'
        else:
            _redeem_script = self.required_signatures.text
            if self.required_signatures.text != '':
                _req_sig = int(self.required_signatures.text)
            else:
                _req_sig = -1

            for _p in range(0, len(self.public_key_data.children)):
                _public_key = self.public_key_data.children[_p].children[0].children[1].children[0].text
                if _public_key != '':
                    try:
                        _ = Ut.hex_to_bytes(_public_key)
                    except:
                        return

                    if len(_public_key) != 66 and len(_public_key) != 130:
                        return

                    _public_keys.append(_public_key)
                    self._address_indexes.append(self.wallet.get_account_address_index(_public_key))
                
            if len(_public_keys) != len(self.public_key_data.children):
                return

            if _req_sig <= 0 or _req_sig > len(_public_keys):
                return

            _public_keys.reverse()
            self._address_indexes.reverse()
            _, _redeem_script, _address = Scripts.P2SHMultisigScriptHash(_req_sig, _public_keys)
            self.preview.text = _redeem_script

        self._redeem_script = _redeem_script
        self.address.text = _address

        try:
            _ = (Base58Decoder
                 .CheckDecode(self.address.text))
            try:
                _ = self.wallet.multi_sig_addresses.get_address_by_name(self.address.text)
            except:
                self.btn_create.disabled = False
        except Exception:
            return

    def create(self):
        _multi_sig_address = MAddress()
        _multi_sig_address.set_address(self.address.text)
        if self.address_label.text != '':
            _multi_sig_address.set_label(self.address_label.text)
        _multi_sig_address.set_is_multi_sig(True)
        _multi_sig_address.set_multi_sig_redeem_script(self._redeem_script)
        _multi_sig_address.set_multi_sig_address_indexes(self._address_indexes)

        self.wallet.multi_sig_addresses._addresses.append(_multi_sig_address)
        self.wallet.multi_sig_addresses._names[_multi_sig_address.address] = len(self.wallet.multi_sig_addresses._addresses)
        self.app.ctrl.wallets.save_wallet(self.wallet.name)
        self.manager.addresses_screen.populate(self.wallet.name)
