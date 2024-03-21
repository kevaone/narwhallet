from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
from kivy.properties import NumericProperty
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


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class CreateNamespaceKeyScreen(Screen):
    wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_id = Nwlabel()
    namespace_address = Nwlabel()
    namespace_key = TextInput()
    namespace_value = TextInput()
    valid_amount = Image()
    header = Header()
    btn_send = Nwbutton()
    btn_ipfs_upload = Nwbutton()
    key_size = NumericProperty(0)
    value_size = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CreateNamespaceKeyScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        self.isReward: bool = False
        self.ns_key: bytes = b''
        self.app = App.get_running_app()
        
    def populate(self, wallet=None, reward_address=None):
        self._refresh = Nwrefreshpopup()
        self.isReward = False
        if wallet is None:
            self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
            self.namespace_id.text = self.manager.namespace_screen.namespaceid
            self.namespace_address.text = self.manager.namespace_screen.owner
        else:
            self.wallet = self.app.ctrl.wallets.get_wallet_by_name(wallet)
        self.header.value = self.manager.namespace_screen.header.value
        self.wallet_name._text = self.wallet.name
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.amount.text = str(NS_RESERVATION/100000000)
        
        self.namespace_key.text = ''
        self.namespace_value.text = ''

        if reward_address is not None:
            self.isReward = True
            self.reward_address = reward_address
        
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        if self.wallet.balance < 10.0:
            self.btn_ipfs_upload.disabled = True

        self.namespace_key.disabled = False
        self.manager.current = 'createnamespacekey_screen'
        Clock.schedule_once(self._refresh.open, 0.1)
        Clock.schedule_once(self._populate, 0.5)

    def _populate(self, *args):
        self.app.ctrl.wallet_get_addresses(self.wallet)
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self._refresh.dismiss()

    def on_enter(self, *args):
        if self.namespace_key.text == '':
            self.namespace_key.focus = True
        else:
            self.namespace_value.focus = True

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
                _a, _b = True, True
                self.valid_amount.size = (dp(30), dp(30))
                if cb is True:
                    _a = self.check_key(False)
                    _b = self.check_value(False)

                if _a and _b is True:
                    self.btn_send.disabled = False
                    
                    return True
            else:
                self.valid_amount.size = (0, 0)
                self.btn_send.disabled = True    
        except Exception:
            self.valid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_key(self, cb=True):
        self.key_size = len(self.namespace_key.text.encode())
        if self.key_size > 255:
            self.btn_send.disabled = True
            return False

        if self.namespace_key.text != '':
            _a, _b = True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_value(False)

            if _a and _b is True:
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True
        
        return False

    def ns_value_input_filter(self, string, from_undo):
        if self.isReward == False:
            return string

        if string in ('.', ''):
            if str(self.namespace_value.text).count('.') > 0:
                return ''
            return string
        try:
            float(string)
            return string
        except ValueError:
            return ''

    def check_value(self, cb=True):
        self.value_size = len(self.namespace_value.text.encode())
        if self.value_size > 3072:
            self.btn_send.disabled = True
            return False

        if self.namespace_value.text != '':
            _a, _b = True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_key(False)

            if _a and _b is True:
                if self.isReward == True:
                    try:
                        _ = float(self.namespace_value.text)
                    except:
                        self.btn_send.disabled = True
                        return False
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True

        return False

    def set_availible_usxo(self):
        _usxos = self.wallet.get_usxos(self.namespace_address.text, self.namespace_id.text)
        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _amount = NS_RESERVATION
        if self.isReward is False:
            if self.ns_key != b'':
                _sh = Scripts.KevaKeyValueUpdate(self.namespace_id.text, self.ns_key,
                                                    self.namespace_value.text, self.namespace_address.text)
                _sh = Scripts.compile(_sh, True)
            else:
                _sh = Scripts.KevaKeyValueUpdate(self.namespace_id.text, self.namespace_key.text,
                                                    self.namespace_value.text, self.namespace_address.text)
                _sh = Scripts.compile(_sh, True)

            _ = self.new_tx.add_output(_amount, self.namespace_address.text)
            self.new_tx.vout[0].scriptPubKey.set_hex(_sh)
        else:
            _sh = Scripts.KevaKeyValueUpdate(self.namespace_id.text, self.ns_key,
                                                '', self.namespace_address.text)
            _sh = Scripts.compile(_sh, True)

            _ = self.new_tx.add_output(_amount, self.namespace_address.text)
            self.new_tx.vout[0].scriptPubKey.set_hex(_sh)
            _reward_amount = Ut.to_sats(float(self.namespace_value.text))
            _ = self.new_tx.add_output(_reward_amount, self.reward_address)
 
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
        self.new_tx.set_version('00710000')
        self.new_tx.set_fee_rate(int(self.fee_rate))

        self.set_output()
        self.set_availible_usxo()
        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        
        if _inp_sel is True:
            _input_value, _output_value, _to_fee = self.new_tx.get_current_values()
            if _need_change is True:
                _cv = _to_fee - _est_fee
                _change_address = self.wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)
                self.change_value = _cv

            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)

            _stx = self.new_tx.serialize_tx()
            self.input_value = _input_value
            self.output_value = _output_value
            self.set_ready(_stx, _est_fee)
            # TODO Validate TX and Broadcast
        else:
            self.reset_transactions()

    def ipfs_upload(self):
        self.manager.mediabrowse_screen.populate(self.wallet, 'createnamespacekey_screen')

    def ipfs_added(self):
        self.manager.current = 'createnamespacekey_screen'
        _ = self.app.ctrl.kex.peers[self.app.ctrl.kex.active_peer].connect()
        MShared.get_addresses(self.wallet, self.app.ctrl.kex)
        self.app.ctrl.kex.peers[self.app.ctrl.kex.active_peer].disconnect()
        _update_time = Ut.get_timestamp()
        self.wallet.set_last_updated(_update_time[0])
        self.app.ctrl.wallets.save_wallet(self.wallet.name)

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
        self.manager.current = 'namespaces_screen'
