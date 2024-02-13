import json
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
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


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class BidNamespaceScreen(Screen):
    wallet_name = Spinner()
    wallet_balance = Nwlabel()
    bid_namespaceid = Spinner()
    bid_namespace_address = Nwlabel()
    bid_amount = TextInput()
    bidtx_reservation = Nwlabel()
    offer_namespaceid = Nwlabel()
    offer_tx = Nwlabel()
    offer_shortcode = Nwlabel()
    offer_name = Nwlabel()
    offer_namespace_address = Nwlabel()
    offer_payment_address = Nwlabel()
    offer_asking_price = Nwlabel()
    offer_description = Nwlabel()
    valid_bid_amount = Image()
    valid_send_to = Image()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(BidNamespaceScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        self.used_inputs = []
        self.app = App.get_running_app()
        
    def populate(self, namespaceid):
        self.header.value = 'Create Bid'
        self._refresh = Nwrefreshpopup()
        _wallets = []
        for _w in self.app.ctrl.wallets.wallets:
            _wallets.append(_w.name)

        self.wallet_name.values = _wallets
        self.bidtx_reservation.text = str(NS_RESERVATION/100000000)
        self.bid_namespaceid.disabled = True
        self.bid_namespace_address.text = ''
        self.bid_amount.text = ''

        _ns = MShared.get_namespace(namespaceid, self.app.ctrl.kex)
        _ns = _ns['result']
        self.offer_namespaceid.text = namespaceid
        self.offer_shortcode.text = str(_ns['root_shortcode'])
        self.offer_name.text = str(_ns['name'])
        _dat = _ns['data']
        _dat.reverse()
        for _k in _dat:
            if _k['dtype'] == 'name_update':
                self.reset()
                return
            elif _k['dtype'] == 'nft_auction':
                _na = json.loads(_k['dvalue'])
                self.offer_asking_price.text = str(_na['price'])
                self.offer_payment_address.text = str(_na['addr'])
                self.offer_tx.text = _k['txid']
                self.offer_description.text = str(_na['desc'])
                break
        self.offer_namespace_address.text = _ns['data'][len(_ns['data'])-1]['addr']
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self.manager.current = 'bidnamespace_screen'

    def wallet_changed(self):
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.wallet_name.text)
        if self.wallet is None:
            return

        Clock.schedule_once(self._refresh.open, 0.1)
        Clock.schedule_once(self._wallet_changed, 0.5)

    def _wallet_changed(self, *args):
        self.app.ctrl.wallet_get_addresses(self.wallet)
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        _ns_list = []

        for address in self.wallet.addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])

        for address in self.wallet.change_addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])

        self.bid_namespaceid.values = _ns_list
        self.bid_namespaceid.disabled = False
        self._refresh.dismiss()

    def ns_changed(self):
        _set = False
        for address in self.wallet.addresses.addresses:
            for ns in address.namespaces:
                if ns['namespaceid'] == self.bid_namespaceid.text:
                    self.bid_namespace_address.text = address.address
                    _set = True
                    break
            if _set is True:
                break

        if _set is False:
            for address in self.wallet.change_addresses.addresses:
                for ns in address.namespaces:
                    if ns['namespaceid'] == self.bid_namespaceid.text:
                        self.bid_namespace_address.text = address.address
                        _set = True
                        break
                if _set is True:
                    break

        self.check_address()

    def bid_amount_input_filter(self, string, from_undo):
        if string in ('.', ''):
            if str(self.bid_amount.text).count('.') > 0:
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
            _amount = float(self.bid_amount.text)
            _bal = float(self.wallet_balance.text)

            if _amount < _bal:
                self.valid_bid_amount.size = (dp(30), dp(30))
                _a, _b, _c, _d = True, True, True, True
                if cb is True:
                    _a = self.check_payment_address(False)
                    _b = self.check_address(False)

                if _a and _b and _c and _d is True:
                    self.btn_send.disabled = False
                    return True
                else:
                    self.btn_send.disabled = True
                    return False
            else:
                self.btn_send.disabled = True    
        except Exception:
            self.valid_bid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_address(self, cb=True):
        try:
            _ = (Base58Decoder
                 .CheckDecode(self.bid_namespace_address.text))

            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_payment_address(False)
                _b = self.check_amount(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
            else:
                self.btn_send.disabled = True
                return False
        except Exception:
            self.btn_send.disabled = True
            return False
        return True

    def check_payment_address(self, cb=True):
        try:
            _ = (Base58Decoder
                 .CheckDecode(self.offer_payment_address.text))

            self.valid_send_to.size = (dp(30), dp(30))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_address(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
        except Exception:
            self.valid_send_to.size = (0, 0)
            self.btn_send.disabled = True
            return False
        return True

    def build_bid(self):
        self.bid_tx = MTransactionBuilder()
        self.bid_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.bid_tx.set_fee(int(self.fee_rate))

        _bid_amount = Ut.to_sats(float(self.bid_amount.text))

        _auc = {}
        _auc['displayName'] = self.offer_name.text
        _ns = self.offer_namespaceid.text
        _ns_key = '\x01_KEVA_NS_'
        _ns_value = json.dumps(_auc, separators=(',', ':'))
        _trans_address = self.wallet.get_unused_address()
        _trans_address = self.wallet.get_unused_address()
        _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                         _trans_address)
        _sh = Scripts.compile(_sh, True)
        _ = self.bid_tx.add_output(NS_RESERVATION, _trans_address)
        self.bid_tx.vout[0].scriptPubKey.set_hex(_sh)
        _ = self.bid_tx.add_output(_bid_amount,
                                   self.offer_payment_address.text)

        self.set_availible_usxo(True)
        _inp_sel, _need_change, _est_fee = self.bid_tx.select_inputs()

        if _inp_sel is True:
            _, _, _fv = self.bid_tx.get_current_values()
            _cv = _fv - _est_fee

            if _need_change is True:
                _ = self.bid_tx.add_output(_cv, _trans_address)

            self.bid_tx.txb_preimage(self.wallet,
                                     SIGHASH_TYPE.ALL_ANYONECANPAY)

    def set_availible_usxo(self, bid):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []

        for tx in _tmp_usxo:
            # NOTE Filtering out tx with extra data, mostly namespaces
            if 'extra' not in tx:
                _used = False
                for _vin in self.bid_tx.vin:
                    if _vin.txid == tx['txid'] and _vin.vout == tx['n']:
                        _used = True
                if _used == False:
                    _usxos.append(tx)
                    continue

            if self.bid_namespace_address.text != tx['a']:
                continue

            if self.bid_namespaceid.text == tx['extra']:
                if bid is False:
                    _usxos.insert(0, tx)

        if bid is False:
            self.new_tx.inputs_to_spend = _usxos
        else:
            self.bid_tx.inputs_to_spend = _usxos

    def set_output(self):
        _amount = NS_RESERVATION
        _ns_address = self.bid_namespace_address.text
        _ns = self.bid_namespaceid.text
        self.build_bid()

        _ns_key = (Ut.hex_to_bytes('0001') + Ut.hex_to_bytes(self.offer_tx.text))
        _ns_value = self.bid_tx.to_psbt()
        _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
                                            _ns_address)
        _sh = Scripts.compile(_sh, True)

        _ = self.new_tx.add_output(_amount, _ns_address)
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
        self.set_availible_usxo(False)
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
        send_popup.provider = self.app.ctrl.kex
        send_popup.in_value = str(Ut.from_sats(self.input_value))
        send_popup.out_value = str(Ut.from_sats(self.output_value))
        send_popup.change_value = str(Ut.from_sats(self.change_value))
        send_popup.fee_rate = self.fee_rate
        send_popup.fee = self.fee
        send_popup.txhex = self.raw_tx
        send_popup.txsize = self.txsize
        send_popup.open()
        self.manager.current = 'namespacealt_screen'
