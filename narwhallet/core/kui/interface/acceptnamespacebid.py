import base64
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.metrics import dp
from narwhallet.core.ksc.scripts import Scripts
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import keva_psbt
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Decoder, Base58Encoder
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.ksc import Scripts
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.nwpopup import Nwpopup
from narwhallet.core.kui import _translate as _tr


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class AcceptNamespaceBidScreen(Screen):
    wallet_name = Spinner()
    wallet_balance = Nwlabel()
    namespaceid = Spinner()
    namespace_address = Nwlabel()
    bid_amount = TextInput()
    # bidtx_reservation = Nwlabel()
    # bid_namespaceid = Nwlabel()
    bid_tx = Nwlabel()
    # bid_shortcode = Nwlabel()
    # bid_name = Nwlabel()
    # bid_namespace_address = Nwlabel()
    payment_address = Nwlabel()
    asking_price = Nwlabel()
    description = Nwlabel()
    valid_bid_amount = Image()
    valid_send_to = Image()
    fee = Nwlabel()
    fee_rate = Nwlabel()
    txsize = Nwlabel()
    txhex = Nwlabel()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(AcceptNamespaceBidScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        self.used_inputs = []
        
    def populate(self, txid, namespaceid, namespace_address):
        self.header.value = _tr.translate('Accept Bid')

        self.bid_tx.text = txid
        # self.bid = MTransactionBuilder()
        
        # TODO Replace with wallet scan for auction NS
        # _wallets = []
        for _w in self.manager.wallets.wallets:
            for _a in _w.addresses.addresses:
                # print('_a', _a.address, namespace_address)
                if _a.address == namespace_address:
                    
                    self.wallet = _w
                    self.wallet_name.text = _w.name
                    break
            for _a in _w.change_addresses.addresses:
                if _a.address == namespace_address:
                    self.wallet = _w
                    self.wallet_name.text = _w.name
                    break
            # _wallets.append(_w.name)
        self.wallet_balance.text = str(self.wallet.balance)
        # self.wallet_name.text = _wallets
        # self.bidtx_reservation.text = str(NS_RESERVATION/100000000)
        # self.bid_namespaceid.disabled = True
        self.namespaceid.text = namespaceid
        self.namespace_address.text = namespace_address
        self.bid_amount.text = ''

        _provider = self.manager.settings_screen.settings.content_providers[0]
        _ns = MShared.get_namespace(namespaceid, _provider)
        # print('_ns', _ns)
        _dat = _ns['result']['data']
        _dat.reverse()
        for _kv in _dat:
            # if self.owner.text == '':
            #     self.owner.text = _kv['addr']
            if _kv['dtype'] == 'nft_auction':
                _auc = json.loads(_kv['dvalue'])
                self.payment_address.text = _auc['addr']
                self.asking_price.text = str(_auc['price'])
                self.description.text = str(_auc['desc'])
                break

        # _ns = _ns['result']
        # self.bid_namespaceid.text = namespaceid
        self.check_tx_is_bid(txid)
        # self.offer_shortcode.text = str(_ns['root_shortcode'])
        # self.offer_name.text = _ns['name']
        # _dat = _ns['data']
        # _dat.reverse()
        # for _k in _dat:
        #     if _k['dtype'] == 'name_update':
        #         self.reset()
        #         return
        #     elif _k['dtype'] == 'nft_auction':
        #         _na = json.loads(_k['dvalue'])
        #         self.offer_asking_price.text = str(_na['price'])
        #         self.offer_payment_address.text = str(_na['addr'])
        #         self.offer_tx.text = _k['txid']
        #         self.offer_description.text = _na['desc']
        #         break
        # self.offer_namespace_address.text = _ns['data'][len(_ns['data'])-1]['addr']
        self.fee.text = ''
        self.txsize.text = ''
        self.txhex.text = ''
        self.btn_send.text = _tr.translate('Create TX')
        self.btn_send.disabled = False
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'acceptnamespacebid_screen'

    def check_tx_is_bid(self, txid):
        _nft_tx = MShared.check_tx_is_bid(txid, self.manager.kex, self.manager.cache)
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
                    if _r[0] == 'PSBT_IN_WITNESS_UTXO':
                        self.new_tx.vin[_idx].tb_value = (Ut
                                                          .bytes_to_int(
                                                              _r[2][:8],
                                                              'little'))
                    elif _r[0] == 'PSBT_IN_PARTIAL_SIG':
                        (self.new_tx.input_signatures
                         .append([Ut.bytes_to_hex(_r[2]),
                                 Ut.bytes_to_hex(_r[1][1:])]))
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

            # if _amount < 0.01:
            #     self.valid_bid_amount.size = (0, 0)
            #     self.btn_send.disabled = True
            #     return False

            if _amount < _bal:
                self.valid_bid_amount.size = (dp(30), dp(30))
                _a, _b, _c, _d = True, True, True, True
                if cb is True:
                    _a = self.check_payment_address(False)
                    _b = self.check_address(False)
                    # _c = self.check_price(False)
                    # _d = self.check_desc(False)

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
                # _c = self.check_price(False)
                # _d = self.check_desc(False)

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
                # _c = self.check_price(False)
                # _d = self.check_desc(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
        except Exception:
            self.valid_send_to.size = (0, 0)
            self.btn_send.disabled = True
            return False
        return True

    def set_availible_usxo(self, bid):
        _tmp_usxo = self.wallet.get_usxos()
        _usxos = []
        _nsusxo = []

        for tx in _tmp_usxo:
            # TODO Check for usxo's used by bids
            _tx = self.manager.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], self.manager.kex, True)

            if _tx is not None and isinstance(_tx, dict):
                _tx = self.manager.cache.tx.add_from_json(_tx)

            if 'OP_KEVA' not in _tx.vout[tx['tx_pos']].scriptPubKey.asm:
                _used = False
                # for _vin in self.bid.vin:
                #     if _vin.txid == _tx.txid and _vin.vout == tx['tx_pos']:
                #         _used = True
                if _used == False:
                    _usxos.append(tx)
            elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
                    and tx['a'] == self.namespace_address.text):
                _nsusxo = tx

        if _nsusxo is not None:
            if bid is False:
                _usxos.insert(0, _nsusxo)

        if bid is False:
            self.new_tx.inputs_to_spend = _usxos
        # else:
        #     self.bid.inputs_to_spend = _usxos

    def set_output(self):
        pass
        # # Namespace Bid
        # _amount = NS_RESERVATION
        # _ns_address = self.bid_namespaceid.text
        # _ns = self.bid_namespaceid.text
        # self.build_bid()

        # _ns_key = (Ut.hex_to_bytes('0001') + Ut.hex_to_bytes(self.offer_tx.text))
        # _ns_value = self.bid_tx.to_psbt()
        # # _testing = self.bid_tx.fr
        # _sh = Scripts.KevaKeyValueUpdate(_ns, _ns_key, _ns_value,
        #                                     _ns_address)
        # _sh = Scripts.compile(_sh, True)

        # _ = self.new_tx.add_output(_amount, self.bid_namespace_address.text)
        # self.new_tx.vout[0].scriptPubKey.set_hex(_sh)

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
        # self.new_tx = MTransactionBuilder()
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_fee(int(self.fee_rate.text))

        # self.set_output()
        self.set_availible_usxo(False)
        # _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        if len(self.new_tx.inputs_to_spend) == 0:
            _inp_sel = False
        else:
            tx = self.new_tx.inputs_to_spend[0]
            self.new_tx.add_input(tx['value'],
                                    str(tx['a_idx'])+':'+str(tx['ch']),
                                    tx['tx_hash'], tx['tx_pos'])
            _inp_sel = True
            # _need_change = False
        
        if _inp_sel is True:
            # _, _, _fv = self.new_tx.get_current_values()
            # if _need_change is True:
            #     _cv = _fv - _est_fee
            #     _change_address = self.wallet.get_unused_change_address()
            #     _ = self.new_tx.add_output(_cv, _change_address)

            self.new_tx.txb_preimage(self.wallet,
                                         SIGHASH_TYPE.ALL_ANYONECANPAY, True)
            _, _, _est_fee = self.new_tx.get_current_values()

            _stx = self.new_tx.serialize_tx()
            self.set_ready(_stx, _est_fee)
            # TODO Validate TX and Broadcast
        else:
            self.reset_transactions()

    def process_send(self):
        # pass
        _bc_result = MShared.broadcast(self.raw_tx, self.manager.kex)
        if isinstance(_bc_result[1], dict):
            _result = json.dumps(_bc_result[1])
        else:
            _result = _bc_result[1]

        msgType = int(_bc_result[0])

        result_popup = Nwpopup()

        if msgType == 1:
            result_popup.status.text = _tr.translate('Error') + ':\n' + _result
        elif msgType == 2:
            result_popup.status.text = _tr.translate('Ok!')

        result_popup.open()
        self.manager.current = 'auctiondetail_screen'
