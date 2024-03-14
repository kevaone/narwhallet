import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.metrics import dp
from narwhallet.core.ksc.scripts import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import keva_psbt
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.ksc import Scripts
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwsendpopup import Nwsendpopup


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class AcceptNamespaceBidScreen(Screen):
    wallet_name = Spinner()
    wallet_balance = Nwlabel()
    namespaceid = Spinner()
    namespace_address = Nwlabel()
    bid_amount = TextInput()
    bid_tx = Nwlabel()
    payment_address = Nwlabel()
    asking_price = Nwlabel()
    description = Nwlabel()
    valid_bid_amount = Image()
    valid_send_to = Image()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(AcceptNamespaceBidScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        self.used_inputs = []
        self.app = App.get_running_app()
        
    def populate(self, txid, namespaceid, namespace_address):
        self.header.value = 'Accept Bid'
        self.bid_tx.text = txid
        
        for _w in self.app.ctrl.wallets.wallets:
            for _a in _w.addresses.addresses:
                if _a.address == namespace_address:
                    
                    self.wallet = _w
                    self.wallet_name.text = _w.name
                    break
            for _a in _w.change_addresses.addresses:
                if _a.address == namespace_address:
                    self.wallet = _w
                    self.wallet_name.text = _w.name
                    break

        self.wallet_balance.text = str(self.wallet.balance)
        self.namespaceid.text = namespaceid
        self.namespace_address.text = namespace_address
        self.bid_amount.text = ''

        _ns = MShared.get_namespace(namespaceid, self.app.ctrl.kex)
        if _ns is None:
            return

        _ns.keys.keys.reverse()
        for _kv in _ns.keys.keys:
            if _kv.dtype == 'nft_auction':
                _auc = json.loads(_kv.dvalue)
                self.payment_address.text = _auc['addr']
                self.asking_price.text = str(_auc['price'])
                self.description.text = str(_auc['desc'])
                break

        self.check_tx_is_bid(txid)
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = False
        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self.manager.current = 'acceptnamespacebid_screen'

    def check_tx_is_bid(self, txid):
        _nft_tx = MShared.check_tx_is_bid(txid, self.app.ctrl.kex)
        if _nft_tx[0] is True:
            _bid_psbt = keva_psbt(_nft_tx[2])
            _sh = (Scripts.AddressScriptHash
                   (self.payment_address.text))
            _sh = Scripts.compile(_sh, True)
            if _bid_psbt.tx.vout[1].scriptPubKey.hex == _sh:
                self.bid_amount.text = str(_bid_psbt.tx.vout[1].value/100000000)
                self.new_tx = _bid_psbt.tx
                _idx = 0
                for _, _r in enumerate(_bid_psbt.psbt_records):
                    _sig = {}
                    if _r[0] == 'PSBT_IN_WITNESS_UTXO':
                        self.new_tx.vin[_idx].tb_value = (Ut
                                                          .bytes_to_int(
                                                              _r[2][:8],
                                                              'little'))
                    elif _r[0] == 'PSBT_IN_PARTIAL_SIG':
                        _sig[Ut.bytes_to_hex(_r[1][1:])] = Ut.bytes_to_hex(_r[2])
                        self.new_tx.input_signatures.append(_sig)
                    elif _r[0] == 'PSBT_IN_REDEEM_SCRIPT':
                        (self.new_tx.vin[_idx].scriptSig
                         .set_hex(Ut.bytes_to_hex(_r[2])))
                        _idx += 1

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

    def set_availible_usxo(self):
        _usxos = self.wallet.get_usxos(self.namespace_address.text, self.namespaceid.text)
        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        pass

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
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_fee(int(self.fee_rate))

        self.set_availible_usxo()
        if len(self.new_tx.inputs_to_spend) == 0:
            _inp_sel = False
        else:
            tx = self.new_tx.inputs_to_spend[0]
            self.new_tx.add_input(tx['value'],
                                    str(tx['a_idx'])+':'+str(tx['ch']),
                                    tx['txid'], tx['n'])
            _inp_sel = True
        
        if _inp_sel is True:
            self.new_tx.txb_preimage(self.wallet,
                                         SIGHASH_TYPE.ALL_ANYONECANPAY, True)
            _, _, _est_fee = self.new_tx.get_current_values()

            _stx = self.new_tx.serialize_tx()
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
        self.manager.current = 'auctiondetail_screen'
