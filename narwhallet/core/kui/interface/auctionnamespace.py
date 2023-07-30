import json
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


TEMP_TX = 'c1ec98af03dcc874e2c1cf2a799463d14fb71bf29bec4f6b9ea68a38a46e50f2'
NS_RESERVATION = 1000000

class AuctionNamespaceScreen(Screen):
    # wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_name = Nwlabel()
    namespace_address = Nwlabel()
    price = TextInput()
    description = TextInput()
    payment_address = TextInput()
    valid_amount = Image()
    valid_price = Image()
    fee = Nwlabel()
    fee_rate = Nwlabel()
    txsize = Nwlabel()
    txhex = Nwlabel()
    header = Header()
    btn_send = Nwbutton()
    address_book = Image()
    valid_send_to = Image()
    valid_description = Image()

    def __init__(self, **kwargs):
        super(AuctionNamespaceScreen, self).__init__(**kwargs)

        self.wallet: MWallet
        
    def populate(self):
        self.wallet = self.manager.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self.header.value = self.wallet.name
        self.wallet_balance.text = str(self.wallet.balance)
        self.amount.text = str(NS_RESERVATION/100000000)
        # TODO: Refactor ids for namespace; they clash with others
        self.namespace_name.text = self.manager.namespace_screen.namespaceid.text
        self.price.text = ''
        self.description.text = ''
        self.payment_address.text = ''
        self.namespace_address.text = self.manager.namespace_screen.owner.text
        self.fee.text = ''
        self.txsize.text = ''
        self.txhex.text = ''
        self.btn_send.text = 'Create TX'
        self.btn_send.disabled = True
        self.fee_rate.text = str(MShared.get_fee_rate(self.manager.kex))
        self.manager.current = 'auctionnamespace_screen'

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
                self.valid_amount.size = (dp(30), dp(30))
                _a, _b, _c, _d = True, True, True, True
                if cb is True:
                    _a = self.check_payment_address(False)
                    _b = self.check_address(False)
                    _c = self.check_price(False)
                    _d = self.check_desc(False)

                if _a and _b and _c and _d is True:
                    self.btn_send.disabled = False
                    return True
                else:
                    self.btn_send.disabled = True
                    return False
            else:
                self.btn_send.disabled = True    
        except Exception:
            self.valid_amount.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_price(self, cb=True):
        try:
            # TODO: Account for locale!!!
            # locale = QLocale()
            # _result = locale.toDouble(amount)
            _amount = float(self.price.text)

            if _amount < 0.00000001:
                self.valid_price.size = (0, 0)
                self.btn_send.disabled = True
                return False

            self.valid_price.size = (dp(30), dp(30))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_payment_address(False)
                _b = self.check_address(False)
                _c = self.check_amount(False)
                _d = self.check_desc(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
                return True
            else:
                self.btn_send.disabled = True    
        except Exception:
            self.valid_price.size = (0, 0)
            self.btn_send.disabled = True
            
        return False

    def check_desc(self, cb=True):
        if self.description.text != '':
            self.valid_description.size = (dp(30), dp(30))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_payment_address(False)
                _b = self.check_address(False)
                _c = self.check_price(False)
                _d = self.check_amount(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
                return True
            else:
                self.btn_send.disabled = True
                return False

        self.valid_description.size = (0, 0)
        self.btn_send.disabled = True
        
        return False

    def check_address(self, cb=True):
        try:
            _ = (Base58Decoder
                 .CheckDecode(self.namespace_address.text))

            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_payment_address(False)
                _b = self.check_amount(False)
                _c = self.check_price(False)
                _d = self.check_desc(False)

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
                 .CheckDecode(self.payment_address.text))

            self.valid_send_to.size = (dp(30), dp(30))
            _a, _b, _c, _d = True, True, True, True
            if cb is True:
                _a = self.check_amount(False)
                _b = self.check_address(False)
                _c = self.check_price(False)
                _d = self.check_desc(False)

            if _a and _b and _c and _d is True:
                self.btn_send.disabled = False
        except Exception:
            self.valid_send_to.size = (0, 0)
            self.btn_send.disabled = True
            return False
        return True

    def set_availible_usxo(self):
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
                _usxos.append(tx)
            elif ('OP_KEVA' in _tx.vout[tx['tx_pos']].scriptPubKey.asm
                    and tx['a'] == self.namespace_address.text):
                _nsusxo = tx

        if _nsusxo is not None:
            _usxos.insert(0, _nsusxo)

        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        # Namespace Auction
        _amount = NS_RESERVATION
        _ns_address = self.namespace_address.text
        _ns = self.namespace_name.text
        _auc = {}
        _auc['displayName'] = self.manager.namespace_screen.namespace_name.text
        _auc['price'] = str(self.price.text)
        _auc['desc'] = self.description.text

        # TODO: Add ui widgets for hashtags then reenable.
        # _tags = {}
        # _hashtags = self.auction_info.nft_hashtags.text().split(' ')
        # for tag in _hashtags:
        #     tag = tag.split(',')
        #     for t in tag:
        #         t = t.replace('#', '').strip()
        #         if t != '':
        #             _tags['#' + t] = ''
        # _tags = list(_tags.keys())
        # if len(_tags) > 0:
        #     _auc['hashtags'] = _tags
        # _payment_addr = self.wallet.get_unused_change_address()
        _payment_addr = self.payment_address.text
        
        _auc['addr'] = _payment_addr
        _ns_value = json.dumps(_auc, separators=(',', ':'))

        _sh = Scripts.KevaKeyValueUpdate(_ns, '\x01_KEVA_NS_', _ns_value,
                                            _ns_address)
        _sh = Scripts.compile(_sh, True)


        _ = self.new_tx.add_output(_amount, self.namespace_address.text)
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
        self.btn_send.text = 'Send'

    def build_send(self):
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

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(3)
        self.manager.current = 'addressbook_screen'

    def process_send(self):
        pass
