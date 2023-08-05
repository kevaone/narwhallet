import json
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.factory import Factory
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kui.widgets.header import Header


class SendScreen(Screen):
    # wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    send_to = TextInput()
    amount = TextInput()
    address_book = Image()
    valid_send_to = Nwlabel()
    valid_amount = Nwlabel()
    fee = Nwlabel()
    fee_rate = Nwlabel()
    txsize = Nwlabel()
    txhex = Nwlabel()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(SendScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        
    def populate(self, wallet_name):
        self.wallet = self.manager.wallets.get_wallet_by_name(wallet_name)
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.send_to.text = ''
        self.amount.text = ''
        self.valid_amount.size = (0, 0)
        self.valid_send_to.size = (0, 0)
        self.fee.text = ''
        self.txsize.text = ''
        self.txhex.text = ''
        self.btn_send.text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'send_screen'

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(1)
        self.manager.current = 'addressbook_screen'

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
            # TODO Check for usxo's used by bids
            _tx = self.manager.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], self.manager.kex, True)

            if _tx is not None and isinstance(_tx, dict):
                _tx = self.manager.cache.tx.add_from_json(_tx)

            if 'OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
                _usxos.append(tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _address = self.send_to.text

        # Simple Send
        # TODO Test conversion across locals, check for Kivy based solution
        _result = float(self.amount.text) # _locale.toDouble(self.amount_input.amount.text())
        _amount = int(_result * 100000000)

        _ = self.new_tx.add_output(_amount, _address)

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
        self.btn_send.text = 'Send'

    def build_send(self):
        if self.amount.text == '':
            return

        if self.send_to.text == '':
            return

        self.new_tx = MTransactionBuilder()
        self.new_tx.set_fee(int(self.fee_rate.text))

        self.set_output()
        self.set_availible_usxo()
        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        
        if _inp_sel is True:
            _, _, _fv = self.new_tx.get_current_values()
            if _need_change is True:
                _cv = _fv - _est_fee
                _change_address = self.wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)

            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)

            _stx = self.new_tx.serialize_tx()
            self.set_ready(_stx, _est_fee)
            # TODO Validate TX and Broadcast
        else:
            self.reset_transactions()

    def process_send(self):
        _bc_result = MShared.broadcast(self.raw_tx, self.manager.kex)
        if isinstance(_bc_result[1], dict):
            _result = json.dumps(_bc_result[1])
        else:
            _result = _bc_result[1]

        msgType = int(_bc_result[0])

        if msgType == 1:
            popup = Popup(title='Send',
            content=Nwlabel(text='Error:\n' + _result),
            size_hint=(None, None), size=(200, 200))

        elif msgType == 2:
            popup = Popup(title='Send',
            content=Nwlabel(text=_result),
            size_hint=(None, None), size=(200, 200))

        popup.open()
        self.manager.current = 'wallet_screen'
