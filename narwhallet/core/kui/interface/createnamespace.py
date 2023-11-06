from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.ksc import Scripts
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class CreateNamespaceScreen(Screen):
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_name = TextInput()
    namespace_address = Nwlabel()
    valid_amount = Image()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(CreateNamespaceScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        
    def populate(self):
        app = App.get_running_app()
        self.wallet = app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.amount.text = str(NS_RESERVATION/100000000)
        self.namespace_name.text = ''
        self.namespace_address.text = ''
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate = str(MShared.get_fee_rate(self.manager.kex))
        _address = self.wallet.get_unused_address()
        self.namespace_address.text = _address
        self.manager.current = 'createnamespace_screen'

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
                _a = True
                self.valid_amount.size = (dp(30), dp(30))
                if cb is True:
                    _a = self.check_value(False)

                if _a is True:
                    self.btn_send.disabled = False
                    
                    return True
            else:
                self.valid_amount.size = (0, 0)
                self.btn_send.disabled = True    
        except Exception:
            self.valid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_value(self, cb=True):
        if self.namespace_name.text != '':
            _a = True
            if cb is True:
                _a = self.check_amount(False)

            if _a is True:
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True

        return False

    def tx_to_ns(self, tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    def set_availible_usxo(self):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _usxos.append(tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _amount = NS_RESERVATION
        _temp_ns = self.tx_to_ns(TEMP_TX, 0)
        _ns_value = self.namespace_name.text
        _sh = Scripts.KevaNamespaceCreation(_temp_ns, _ns_value,
                                                self.namespace_address.text)
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

            _ns = self.tx_to_ns(self.new_tx.vin[0].txid,
                                self.new_tx.vin[0].vout)
            _ns_value = self.namespace_name.text
            _n_sh = (Scripts.KevaNamespaceCreation
                     (_ns, _ns_value, self.namespace_address.text))
            _n_sh = Scripts.compile(_n_sh, True)
            self.new_tx.vout[0].scriptPubKey.set_hex(_n_sh)
            
            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)

            _stx = self.new_tx.serialize_tx()
            self.input_value = _iv
            self.output_value = _ov
            self.set_ready(_stx, _est_fee)

            # TODO Validate TX and Broadcast
        else:
            self.reset_transactions()

    def process_send(self):
        send_popup = Nwsendpopup()
        send_popup.provider = self.manager.kex
        send_popup.in_value = str(Ut.from_sats(self.input_value))
        send_popup.out_value = str(Ut.from_sats(self.output_value))
        send_popup.change_value = str(Ut.from_sats(self.change_value))
        send_popup.fee_rate = self.fee_rate
        send_popup.fee = self.fee
        send_popup.txhex = self.raw_tx
        send_popup.txsize = self.txsize
        send_popup.open()
        self.manager.current = 'namespaces_screen'
