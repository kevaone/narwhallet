import json
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
from kivy.properties import StringProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.transaction_builder import MTransactionBuilder
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwpopup import Nwpopup
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup


class MediaBrowseScreen(Screen):
    file_chooser = FileChooserListView()
    header = Header()
    home_directory = os.path.expanduser('~')
    wallet_balance = StringProperty()
    send_to = StringProperty()
    amount = StringProperty()
    fee = StringProperty()
    fee_rate = StringProperty()
    txsize = StringProperty()
    txhex = StringProperty()
    btn_load = Nwbutton()

    def populate(self, wallet, ret_screen):
        self.wallet: MWallet = wallet
        self.header.value = 'Media Browse'
        self.wallet_balance = str(self.wallet.balance)
        self.send_to = ''
        self.amount = ''
        self.fee = ''
        self.txsize = ''
        self.txhex = ''
        self.up_result = {}
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.fee_rate = str(MShared.get_fee_rate(self.manager.kex))
        self.ret_screen = ret_screen
        if self.wallet.balance < 10.0:
            self.btn_load.disabled = True

        self.manager.current = 'mediabrowse_screen'


    def load(self, path, selection):
        with open(selection[0], 'rb') as f:
            data = f.read()
        _file = os.path.basename(selection[0])

        self.up_result = MShared.ipfs_upload(_file, Ut.base64_encode(data).decode(), self.manager.kex)

        if 'CID' in self.up_result and 'payment_required' in self.up_result and 'payment_address' in self.up_result:
            self.amount =  str(self.up_result['payment_required'])
            self.send_to = self.up_result['payment_address']

            self.build_send()
        elif 'CID' in self.up_result and 'status' in self.up_result:
            if self.up_result['status'] == 'paid':
                self.finish()
        else:
            result_popup = Nwpopup()
            result_popup.status._text = 'Error' + ':\n' + json.dumps(self.up_result)
            result_popup.open()

    def set_availible_usxo(self):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _usxos.append(tx)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _address = self.send_to

        # Simple Send
        # TODO Test conversion across locals, check for Kivy based solution
        _result = float(self.amount) # _locale.toDouble(self.amount_input.amount.text())
        _amount = Ut.to_sats(_result) #int(_result * 100000000)

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
        # self.btn_send._text = 'Send'
        self.process_send()

    def build_send(self):
        if self.amount == '':
            return

        if self.send_to == '':
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
        send_popup.isIPFS = self.up_result['CID']
        send_popup.provider = self.manager.kex
        send_popup.in_value = str(Ut.from_sats(self.input_value))
        send_popup.out_value = str(Ut.from_sats(self.output_value))
        send_popup.change_value = str(Ut.from_sats(self.change_value))
        send_popup.fee_rate = self.fee_rate
        send_popup.fee = self.fee
        send_popup.txhex = self.raw_tx
        send_popup.txsize = self.txsize
        send_popup.bind(msgType=self.finish)
        send_popup.open()
        # self.manager.current = self.ret_screen

    def finish(self, *args):
        _v = self.manager.createnamespacekey_screen.namespace_value.text
        _c = '{{' + self.up_result['CID'] + '|' + self.up_result['media_type'] + '}}'
        if _v == '':
            _v = _c
        else:
            _v = _c + '\n\n' + _v
        self.manager.createnamespacekey_screen.namespace_value.text = _v
        self.manager.current = self.ret_screen
