from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
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
    header = Header()

    def __init__(self, **kwargs):
        super(SendScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        
    def populate(self, wallet_name):
        self.wallet = self.manager.wallets.get_wallet_by_name(wallet_name)
        # self.wallet_name.text = self.wallet.name
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.send_to.text = ''
        self.amount.text = ''
        self.fee.text = ''
        self.txsize.text = ''
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'send_screen'

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(1)
        self.manager.current = 'addressbook_screen'

    def validate_address(self):
        pass

    def validate_amount(self):
        pass

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
        print(self.raw_tx)
        # self.send_info.tx.setPlainText(self.raw_tx)

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