from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
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
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class TransferNamespaceScreen(Screen):
    # wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_name = Nwlabel()
    namespace_address = Nwlabel()
    new_namespace_address = TextInput()
    namespace_key = TextInput()
    namespace_value = TextInput()
    valid_amount = Image()
    valid_address = Image()
    fee = Nwlabel()
    fee_rate = Nwlabel()
    txsize = Nwlabel()
    txhex = Nwlabel()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(TransferNamespaceScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        
    def populate(self):
        self.wallet = self.manager.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.amount.text = str(NS_RESERVATION/100000000)
        self.namespace_name.text = self.manager.namespace_screen.namespaceid.text
        self.namespace_key.text = 'Transfer'
        self.namespace_value.text = ''
        self.namespace_address.text = self.manager.namespace_screen.owner.text
        self.new_namespace_address.text = ''
        self.fee.text = ''
        self.txsize.text = ''
        self.txhex.text = ''
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'transfernamespace_screen'

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(2)
        self.manager.current = 'addressbook_screen'

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
                _a, _b, _c = True, True, True
                self.valid_amount.size = (dp(30), dp(30))
                if cb is True:
                    _a = self.check_address(False)
                    _b = self.check_key(False)
                    _c = self.check_value(False)

                if _a and _b and _c is True:
                    self.btn_send.disabled = False
                    
                    return True
            else:
                self.valid_amount.size = (0, 0)
                self.btn_send.disabled = True
        except Exception:
            self.valid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_address(self, cb=True):
        try:
            _ = (Base58Decoder
                 .CheckDecode(self.new_namespace_address.text))
            _a, _b, _c = True, True, True
            self.valid_address.size = (dp(30), dp(30))
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_key(False)
                _c = self.check_value(False)

            if _a and _b and _c is True:
                self.btn_send.disabled = False
        except Exception:
            self.valid_address.size = (0, 0)
            self.btn_send.disabled = True
            return False
        return True

    def check_key(self, cb=True):
        if self.namespace_key.text != '':
            _a, _b, _c = True, True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_address(False)
                _c = self.check_value(False)

            if _a and _b and _c is True:
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True
        
        return False

    def check_value(self, cb=True):
        if self.namespace_value.text != '':
            _a, _b, _c = True, True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_address(False)
                _c = self.check_key(False)

            if _a and _b and _c is True:
                self.btn_send.disabled = False
                return True

        self.btn_send.disabled = True

        return False

    def set_availible_usxo(self):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []
        _nsusxo = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _usxos.append(tx)
                continue

            if self.namespace_address.text != tx['a']:
                continue

            if self.namespace_name.text == tx['extra']:
                _usxos.insert(0, tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        # Namespace Key Create, Update
        _amount = NS_RESERVATION
        _sh = Scripts.KevaKeyValueUpdate(self.namespace_name.text, self.namespace_key.text,
                                             self.namespace_value.text, self.new_namespace_address.text)
        _sh = Scripts.compile(_sh, True)

        _ = self.new_tx.add_output(_amount, self.new_namespace_address.text)
        self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

    def reset_transactions(self):
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []

    def set_ready(self, _stx, _est_fee):
        self.fee.text = str(_est_fee/100000000)
        self.txsize.text = str(len(_stx))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.txhex.text = Ut.bytes_to_hex(_stx)
        # self.btn_send._text = 'Send'
        # print(self.raw_tx)
        # self.send_info.tx.setPlainText(self.raw_tx)
        self.process_send()

    def build_send(self):
        self.new_tx = MTransactionBuilder()
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_fee(int(self.fee_rate.text))

        self.set_output()
        self.set_availible_usxo() #True, False, self.namespace_address.text)
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
        self.manager.current = 'namespace_screen'
