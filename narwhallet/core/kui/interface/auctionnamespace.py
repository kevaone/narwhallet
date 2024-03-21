import json
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.app import App
from kivy.properties import NumericProperty
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

class AuctionNamespaceScreen(Screen):
    wallet_name = Nwlabel()
    wallet_balance = Nwlabel()
    amount = TextInput()
    namespace_id = Nwlabel()
    namespace_address = Nwlabel()
    price = TextInput()
    description = TextInput()
    payment_address = TextInput()
    valid_amount = Image()
    valid_price = Image()
    header = Header()
    btn_send = Nwbutton()
    address_book = Image()
    valid_send_to = Image()
    valid_description = Image()
    value_size = NumericProperty(0)

    def __init__(self, **kwargs):
        super(AuctionNamespaceScreen, self).__init__(**kwargs)

        self.fee = ''
        self.fee_rate = ''
        self.txsize = ''
        self.txhex = ''
        self.wallet: MWallet
        self.app = App.get_running_app()
        
    def populate(self):
        self.wallet = self.app.ctrl.wallets.get_wallet_by_name(self.manager.wallet_screen.header.value)
        self._refresh = Nwrefreshpopup()
        self.header.value = self.manager.namespace_screen.header.value
        self.wallet_name._text = self.wallet.name
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.amount.text = str(NS_RESERVATION/100000000)
        # TODO: Refactor ids for namespace; they clash with others
        self.namespace_id.text = self.manager.namespace_screen.namespaceid
        self.price.text = ''
        self.description.text = ''
        self.payment_address.text = ''
        self.namespace_address.text = self.manager.namespace_screen.owner
        self.input_value = 0
        self.output_value = 0
        self.change_value = 0
        self.btn_send._text = 'Create TX'
        self.btn_send.disabled = True
        self.manager.current = 'auctionnamespace_screen'
        Clock.schedule_once(self._refresh.open, 0.1)
        Clock.schedule_once(self._populate, 0.5)

    def _populate(self, *args):
        self.app.ctrl.wallet_get_addresses(self.wallet)
        self.wallet_balance.text = str(round(self.wallet.balance, 8))
        self.fee_rate = str(MShared.get_fee_rate(self.app.ctrl.kex))
        self._refresh.dismiss()

    def on_enter(self, *args):
        self.payment_address.focus = True

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

    def price_input_filter(self, string, from_undo):
        if string in ('.', ''):
            if str(self.price.text).count('.') > 0:
                return ''
            return string
        try:
            float(string)
            return string
        except ValueError:
            return ''

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
        try:
            _name = json.loads(self.manager.namespace_screen.namespace_name)['displayName']
        except:
            _name = self.manager.namespace_screen.namespace_name
        _sd = {}
        _sd['displayName'] = _name
        _sd['addr'] = self.payment_address.text
        if self.price.text == '':
            _sd['price'] = 0.0
        else:
            _sd['price'] = float(self.price.text)
        _sd['desc'] = self.description.text
        _sdj = json.dumps(_sd, separators=(',', ':'))
        self.value_size = len(_sdj)
        if self.value_size > 3072:
            self.btn_send.disabled = True
            return False

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
        _valid = Ut.check_address_valid(self.namespace_address.text)

        if _valid is False:
            self.btn_send.disabled = True
            return False

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

        return True

    def check_payment_address(self, cb=True):
        _valid = Ut.check_address_valid(self.payment_address.text)

        if _valid is False:
            self.valid_send_to.size = (0, 0)
            self.btn_send.disabled = True
            return False

        self.valid_send_to.size = (dp(30), dp(30))
        _a, _b, _c, _d = True, True, True, True
        if cb is True:
            _a = self.check_amount(False)
            _b = self.check_address(False)
            _c = self.check_price(False)
            _d = self.check_desc(False)

        if _a and _b and _c and _d is True:
            self.btn_send.disabled = False

        return True

    def set_availible_usxo(self):
        _usxos = self.wallet.get_usxos(self.namespace_address.text, self.namespace_id.text)
        self.new_tx.inputs_to_spend = _usxos

    def set_output(self):
        _amount = NS_RESERVATION
        _ns_address = self.namespace_address.text
        _ns = self.namespace_id.text
        _auc = {}

        try:
            _name = json.loads(self.manager.namespace_screen.namespace_name)['displayName']
        except:
            _name = self.manager.namespace_screen.namespace_name

        _auc['displayName'] = _name
        _auc['price'] = float(self.price.text)
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
        self.fee = str(_est_fee/100000000)
        self.txsize = str(len(_stx))
        self.raw_tx = Ut.bytes_to_hex(_stx)
        self.txhex = Ut.bytes_to_hex(_stx)
        self.process_send()

    def build_send(self):
        self.new_tx = MTransactionBuilder()
        self.new_tx.set_version('00710000')
        self.new_tx.set_fee_rate(int(self.fee_rate))
        self.set_output()
        self.set_availible_usxo()
        _inp_sel, _need_change, _est_fee = self.new_tx.select_inputs()
        
        if _inp_sel is True:
            _input_value, _output_value, _to_fee = self.new_tx.get_current_values()
            if _need_change is True:
                _cv = _to_fee - _est_fee
                _change_address = self.wallet.get_unused_change_address()
                _ = self.new_tx.add_output(_cv, _change_address)
                self.change_value = _cv

            self.new_tx.txb_preimage(self.wallet, SIGHASH_TYPE.ALL)
            _stx = self.new_tx.serialize_tx()
            self.input_value = _input_value
            self.output_value = _output_value
            self.set_ready(_stx, _est_fee)
        else:
            self.reset_transactions()

    def select_from_address_book(self):
        self.manager.addressbook_screen.populate(3)
        self.manager.current = 'addressbook_screen'

    def get_address_from_wallet(self):
        if self.wallet is not None:
            _addr = self.wallet.get_unused_address()
            self.payment_address.text = _addr
            self.app.ctrl.wallets.save_wallet(self.wallet.name)

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
        self.manager.current = 'namespace_screen'
