from kivy.app import App
from kivy.clock import Clock
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
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwrefreshpopup import Nwrefreshpopup
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup


class SendScreen(Screen):
    wallet_balance = Nwlabel()
    send_to = TextInput()
    amount = TextInput()
    address_book = Image()
    valid_send_to = Nwlabel()
    valid_amount = Nwlabel()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(SendScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.app = App.get_running_app()
        
    def populate(self, wallet_name):
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(wallet_name)
        self._refresh = Nwrefreshpopup()
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.send_to.text = ''
        self.amount.text = ''
        self.valid_amount.size = (0, 0)
        self.valid_send_to.size = (0, 0)
        self.fee = ''
        self.txsize = ''
        self.txhex = ''
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.manager.current = 'send_screen'
        Clock.schedule_once(self._refresh.open, 0.1)
        Clock.schedule_once(self._populate, 0.5)

    def _populate(self, *args):
        self.app.ctrl.wallet_get_addresses(self.wallet)
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self._refresh.dismiss()

    def on_enter(self, *args):
        self.send_to.focus = True

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(1)
        self.manager.current = 'addressbook_screen'

    def amount_input_filter(self, string, from_undo):
        if string in ('.', ''):
            if str(self.amount.text).count('.') > 0:
                return ''
            return string
        try:
            float(string)
            return string
        except ValueError:
            return ''

    def check_amount(self, cb=True):
        try:
            # TODO: Account for locale!!!
            # locale = QLocale()
            # _result = locale.toDouble(amount)
            _amount = float(self.amount.text)
            _bal = float(self.wallet_balance.text)
            if _amount < _bal and _amount > 0:
                _ca = True
                self.valid_amount.size = (dp(30), dp(30))
                if cb is True:
                    _ca = self.check_address(False)

                if _ca is True:
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
                 .CheckDecode(self.send_to.text))
            _ca = True
            self.valid_send_to.size = (dp(30), dp(30))
            if cb is True:
                _ca = self.check_amount(False)

            if _ca is True:
                self.btn_send.disabled = False
        except Exception:
            self.valid_send_to.size = (0, 0)
            self.btn_send.disabled = True
            return False
        return True

    def set_availible_usxo(self):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _usxos.append(tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _address = self.send_to.text

        # TODO Test conversion across locals, check for Kivy based solution
        _result = float(self.amount.text)
        _amount = Ut.to_sats(_result)

        _ = self.new_tx.add_output(_amount, _address)

    def reset_transactions(self):
        self.raw_tx = ''
        self.new_tx.set_vin([])
        self.new_tx.set_vout([])
        self.new_tx.input_signatures = []

    def set_ready(self, _stx, _est_fee):
        self.fee = str(Ut.from_sats(_est_fee))
        self.txsize = str(len(_stx))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.txhex = Ut.bytes_to_hex(_stx)
        self.process_send()

    def build_send(self):
        if self.amount.text == '':
            return

        if self.send_to.text == '':
            return

        self.new_tx = MTransactionBuilder()
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
            # TODO Validate TX
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
        self.manager.current = 'wallet_screen'
