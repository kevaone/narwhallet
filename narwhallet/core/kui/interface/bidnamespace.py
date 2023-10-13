import base64
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.metrics import dp
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
    fee = Nwlabel()
    fee_rate = Nwlabel()
    txsize = Nwlabel()
    txhex = Nwlabel()
    header = Header()
    btn_send = Nwbutton()

    def __init__(self, **kwargs):
        super(BidNamespaceScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        self.used_inputs = []
        
    def populate(self, namespaceid):
        self.header.value = 'Create Bid'
        
        _wallets = []
        for _w in self.manager.wallets.wallets:
            _wallets.append(_w.name)

        self.wallet_name.values = _wallets
        self.bidtx_reservation.text = str(NS_RESERVATION/100000000)
        self.bid_namespaceid.disabled = True
        self.bid_namespace_address.text = ''
        self.bid_amount.text = ''

        _ns = MShared.get_namespace(namespaceid, self.manager.kex)
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
        self.fee.text = ''
        self.txsize.text = ''
        self.txhex.text = ''
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'bidnamespace_screen'

    def wallet_changed(self):
        self.wallet = self.manager.wallets.get_wallet_by_name(self.wallet_name.text)
        if self.wallet is None:
            return

        self.wallet_balance.text = str(self.wallet.balance)
        _ns_list = []

        for address in self.wallet.addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])

        for address in self.wallet.change_addresses.addresses:
            for ns in address.namespaces:
                _ns_list.append(ns['namespaceid'])

        self.bid_namespaceid.values = _ns_list
        self.bid_namespaceid.disabled = False

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

    # def check_tx_is_auction(self):
    #     _nft_tx = self.namespace_key_input.key.text()

    #     _nft_tx = MShared.check_tx_is_auction(_nft_tx, self.kex, self.cache)
    #     if _nft_tx[0] is True:
    #         self.auction_info.nft_name.setText(_nft_tx[2]['displayName'])
    #         self.auction_info.nft_desc.setText(_nft_tx[2]['desc'])
    #         if 'hashtags' in _nft_tx[1]:
    #             self.auction_info.nft_hashtags.setText(_nft_tx[1]['hashtags'])
    #         self.auction_info.nft_price.setText(_nft_tx[2]['price'])
    #         self.auction_info.nft_ns.setText(_nft_tx[1])
    #         self.auction_info.nft_address.setText(_nft_tx[2]['addr'])

    def build_bid(self):
        self.bid_tx = MTransactionBuilder()
        self.bid_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.bid_tx.set_fee(int(self.fee_rate.text))

        # locale = QLocale()
        # _b_amount = locale.toDouble(self.amount_input.amount.text())
        _bid_amount = Ut.to_sats(float(self.bid_amount.text)) # int(float(self.bid_amount.text) * 100000000)

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
        # Namespace Bid
        _amount = NS_RESERVATION
        _ns_address = self.bid_namespace_address.text
        _ns = self.bid_namespaceid.text
        self.build_bid()

        _ns_key = (Ut.hex_to_bytes('0001') + Ut.hex_to_bytes(self.offer_tx.text))
        _ns_value = self.bid_tx.to_psbt()
        # _testing = self.bid_tx.fr
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
        self.fee.text = str(_est_fee/100000000)
        self.txsize.text = str(len(_stx))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.txhex.text = Ut.bytes_to_hex(_stx)
        self.btn_send._text = 'Send'

    def build_send(self):
        self.new_tx = MTransactionBuilder()
        self.new_tx.set_version(Ut.hex_to_bytes('00710000'))
        self.new_tx.set_fee(int(self.fee_rate.text))

        self.set_output()
        self.set_availible_usxo(False)
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
        # pass
        _bc_result = MShared.broadcast(self.raw_tx, self.manager.kex)
        if isinstance(_bc_result[1], dict):
            _result = json.dumps(_bc_result[1])
        else:
            _result = _bc_result[1]

        msgType = int(_bc_result[0])

        result_popup = Nwpopup()

        if msgType == 1:
            result_popup.status._text = 'Error' + ':\n' + _result
        elif msgType == 2:
            result_popup.status._text = 'Ok!'

        result_popup.open()
        self.manager.current = 'bids_screen'
