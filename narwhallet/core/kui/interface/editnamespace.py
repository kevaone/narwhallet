import json
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
from kivy.properties import NumericProperty
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.ksc import Scripts
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwrefreshpopup import Nwrefreshpopup
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup
from narwhallet.core.kui.widgets.nwboxlayout import Nwboxlayout


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class EditNamespaceScreen(Screen):
    wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_id = Nwlabel()
    namespace_address = Nwlabel()
    ns_value = TextInput()
    ns_displayName = TextInput()
    preview = TextInput()
    namespace_key = TextInput()
    valid_amount = Image()
    header = Header()
    btn_send = Nwbutton()
    valid_send_to = Image()
    valid_description = Image()
    key_size = NumericProperty(0)
    value_size = NumericProperty(0)
    is_social = CheckBox()
    root_data = Nwboxlayout()
    social_data = Nwboxlayout()
    display_box = Nwboxlayout()
    temp_data = None

    def __init__(self, **kwargs):
        super(EditNamespaceScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        self.value = None
        self.app = App.get_running_app()
        
    def populate(self):
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self._refresh = Nwrefreshpopup()
        self.header.value = self.manager.namespace_screen.header.value
        self.wallet_name._text = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.amount.text = str(NS_RESERVATION/100000000)
        self.namespace_id.text = self.manager.namespace_screen.namespaceid
        self.namespace_key.disabled = True

        self.namespace_address.text = self.manager.namespace_screen.owner
        self.is_social.active = True
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.manager.current = 'editnamespace_screen'
        Clock.schedule_once(self._refresh.open, 0.1)
        Clock.schedule_once(self._populate, 0.5)

    def _populate(self, *args):
        self.app.ctrl.wallet_get_addresses(self.wallet)
        self.wallet_balance.text = str(self.wallet.balance)
        _ns = MShared.get_namespace(self.namespace_id.text, self.app.ctrl.kex)
        _ns = _ns['result']
        _dat = _ns['data']
        _dat.reverse()
        _ss = False
        _rs = False

        for _kv in _dat:
            if _kv['dkey'] == '\x01_KEVA_NS_':
                if _ss is False:
                    try:
                        self.ns_displayName.text = str(json.loads(_kv['dvalue'])['displayName'])
                        self.value = json.loads(_kv['dvalue'])
                    except:
                        self.ns_displayName.text = ''
                    _ss = True
            elif _kv['dkey'] == '_KEVA_NS_':
                if _rs is False:
                    self.ns_value.text = str(_kv['dvalue'])
                    _rs = True

        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self._refresh.dismiss()

    def on_enter(self, *args):
        if self.is_social.active:
            self.ns_displayName.focus = True
        else:
            self.ns_value.focus = True

    def on_is_social_active(self):
        if self.is_social.active:
            self.namespace_key.text = '\x01_KEVA_NS_'
            self.root_data.opacity = 0
            self.social_data.opacity = 1
            self.display_box.height = dp(525)
            self.root_data.height = dp(0)
            self.social_data.height = dp(265)
            for c in self.root_data.children:
                c.size_hint_y = None
                c.height = dp(0)
                for cx in c.children:
                    cx.size_hint_y = None
                    cx.height = dp(0)
            
            for c in self.social_data.children:
                c.size_hint_y = 1
                for cx in c.children:
                    cx.size_hint_y = 1

            self.social_data.children[6].size_hint_y = None
            self.social_data.children[6].height = dp(20)
            self.social_data.children[5].size_hint_y = None
            self.social_data.children[5].height = dp(10)
            self.social_data.children[4].size_hint_y = None
            self.social_data.children[4].height = dp(20)
            self.social_data.children[3].size_hint_y = None
            self.social_data.children[3].height = dp(35)
            self.social_data.children[2].size_hint_y = None
            self.social_data.children[2].height = dp(10)
            self.social_data.children[1].size_hint_y = None
            self.social_data.children[1].height = dp(20)
            self.social_data.children[0].size_hint_y = None
            self.social_data.children[0].height = dp(150)
        else:
            self.namespace_key.text = '_KEVA_NS_'
            self.root_data.opacity = 1
            self.social_data.opacity = 0
            self.display_box.height = dp(430)
            self.root_data.height = dp(170)
            self.social_data.height = dp(0)
            for c in self.root_data.children:
                c.size_hint_y = 1
                for cx in c.children:
                    cx.size_hint_y = 1
            
            for c in self.social_data.children:
                c.size_hint_y = None
                c.height = dp(0)
                for cx in c.children:
                    cx.size_hint_y = None
                    cx.height = dp(0)

            self.root_data.children[0].size_hint_y = None
            self.root_data.children[0].height = dp(150)

        self.check_ns_value()

    def check_amount(self, cb=True):
        try:
            # TODO: Account for locale!!!
            # locale = QLocale()
            # _result = locale.toDouble(amount)
            _amount = float(self.amount.text)
            _bal = float(self.wallet_balance.text)
            if _amount < 0.01:
                self.valid_amount.size = (0, 0)
                self.btn_send.disabled = True
                return False

            if _amount < _bal:
                self.valid_amount.size = (dp(30), dp(30))
                _a, _b, _c, _d = True, True, True, True
                if cb is True:
                    _a = self.check_key(False)
                    _b = self.check_address(False)
                    # _c = self.check_price(False)
                    _d = self.check_ns_value(False)

                if _a and _b and _c and _d is True:
                    self.btn_send.disabled = False
                    return True
                else:
                    self.btn_send.disabled = True
                    return False
            else:
                self.btn_send.disabled = True    
        except Exception:
            self.valid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_ns_value(self, cb=True):
        if self.is_social.active is True:
            if self.value is not None:
                _val = self.value
            else:
                _val = {}

            if self.ns_displayName.text != '':
                _val['displayName'] = self.ns_displayName.text
            else:
                if 'displayName' in _val:
                    del _val['displayName']
            _value = json.dumps(_val, separators=(',', ':'))
            self.value = _val
            self.preview.text = _value
        else:
            _value = self.ns_value.text

        self.value_size = len(_value)
        if _value == '{}':
            self.valid_description.size = (0, 0)
            self.btn_send.disabled = True
            return False

        if self.value_size < 3072 and self.value_size > 0:
            self.valid_description.size = (dp(30), dp(30))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_key(False)
                _b = self.check_address(False)
                # _c = self.check_price(False)
                _d = self.check_amount(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
                return True

        self.valid_description.size = (0, 0)
        self.btn_send.disabled = True
        
        return False

    def check_address(self, cb=True):
        try:
            _ = (Base58Decoder
                 .CheckDecode(self.namespace_address.text))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                # _a = self.check_payment_address(False)
                _b = self.check_amount(False)
                _c = self.check_key(False)
                _d = self.check_ns_value(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
            else:
                self.btn_send.disabled = True
                return False
        except Exception:
            self.btn_send.disabled = True
            return False
        return True

    def check_key(self, cb=True):
        self.key_size = len(self.namespace_key.text.encode())
        if self.key_size > 255:
            self.btn_send.disabled = True
            return False

        if self.namespace_key.text != '':
            _a, _b = True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_ns_value(False)

            if _a and _b is True:
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True
        
        return False

    def set_availible_usxo(self):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _usxos.append(tx)
                continue

            if self.namespace_address.text != tx['a']:
                continue

            if self.namespace_id.text == tx['extra']:
                _usxos.insert(0, tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _amount = NS_RESERVATION
        _ns_address = self.namespace_address.text
        _ns = self.namespace_id.text

        if self.is_social.active is True:
            _key = '\x01_KEVA_NS_'
            _value = json.dumps(self.value, separators=(',', ':'))
        else:
            _key = '_KEVA_NS_'
            _value = self.ns_value.text

        _sh = Scripts.KevaKeyValueUpdate(_ns, _key, _value,
                                            _ns_address)
        _sh = Scripts.compile(_sh, True)
        _ = self.new_tx.add_output(_amount, self.namespace_address.text)
        self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

    def reset_transactions(self):
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []

    def set_ready(self, _stx, _est_fee):
        self.fee = str(_est_fee/100000000)
        self.txsize = str(len(_stx))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.txhex = Ut.bytes_to_hex(_stx)
        self.process_send()

    def build_send(self):
        self.new_tx = MTransactionBuilder()
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_fee(int(self.fee_rate))
        self.set_output()
        self.set_availible_usxo()
        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        
        if _inp_sel is True:
            _iv, _ov, _fv = self.new_tx.get_current_values()
            if _need_change is True:
                _cv = _fv - _est_fee
                _change_address = self.wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)
                self.change_value = _cv

            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)
            _stx = self.new_tx.serialize_tx()
            self.input_value = _iv
            self.output_value = _ov
            self.set_ready(_stx, _est_fee)
        else:
            self.reset_transactions()

    def process_send(self):
        send_popup = Nwsendpopup()
        send_popup.provider = self.app.ctrl.kex
        send_popup.in_value = str(Ut.from_sats(self.input_value))
        send_popup.out_value = str(Ut.from_sats(self.output_value))
        send_popup.change_value = str(Ut.from_sats(self.change_value))
        send_popup.fee_rate = self.fee_rate
        send_popup.fee = self.fee
        send_popup.txhex = self.raw_tx
        send_popup.txsize = self.txsize
        send_popup.open()
        self.manager.current = 'namespace_screen'
