import json
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.nwpopup import Nwpopup
from narwhallet.core.kui.widgets.txinputlistinfo import TXInputListInfo
from narwhallet.core.kui.widgets.txinputlistpopup import Txinputlistpopup
from narwhallet.core.kui.widgets.txoutputlistinfo import TXOutputListInfo
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.txoutputlistpopup import Txoutputlistpopup


class TransactionScreen(Screen):
    txid = ObjectProperty(None)
    tx_hash = ObjectProperty(None)
    version = ObjectProperty(None)
    tx_size = ObjectProperty(None)
    vsize = ObjectProperty(None)
    locktime = ObjectProperty(None)
    blockhash = ObjectProperty(None)
    vin = ObjectProperty(None)
    vout = ObjectProperty(None)
    confirmations = ObjectProperty(None)
    time = ObjectProperty(None)
    blocktime = ObjectProperty(None)
    header = Header()

    def __init__(self, **kwargs):
        super(TransactionScreen, self).__init__(**kwargs)

        self.pvin = Txinputlistpopup()
        self.pvout = Txoutputlistpopup()
        self.phex = Nwpopup()
        self.pjson = Nwpopup()
        self.app = App.get_running_app()

    def populate(self, txid):
        self.header.value = self.manager.wallet_screen.header.value
        self.txid.text = txid
        _asa = MShared.get_transaction(txid, self.app.ctrl.kex)
        self.pvin.vin.clear_widgets()
        self.pvout.vout.clear_widgets()
        if _asa is not None:
            # TODO Interface cache for rest of tx data
            self.tx_hash.text = _asa['hash']
            self.version.text = str(_asa['version'])
            self.tx_size.text = str(_asa['size'])
            self.vsize.text = str(_asa['vsize'])
            self.locktime.text = str(_asa['locktime'])
            self.blockhash.text = _asa['blockhash']
            self.vin.text = str(len(_asa['vin']))
            self.vout.text = str(len(_asa['vout']))
            for v in _asa['vin']:
                _i = TXInputListInfo()
                _i.txid._text = v['txid']
                _i.vout._text = str(v['vout'])
                self.pvin.vin.add_widget(_i)
                
            for o in _asa['vout']:
                _o = TXOutputListInfo()
                _o.n._text = str(o['n'])
                _o.value._text = str(round(o['value'], 8))
                _o.scriptpubkey_asm._text = o['scriptPubKey']['asm']
                self.pvout.vout.add_widget(_o)
            self.phex.status._text = _asa['hex']
            self.phex.header.value = 'HEX'
            self.pjson.status._text = json.dumps(_asa, indent=4)
            self.pjson.header.value = 'JSON'
            self.confirmations.text = str(_asa['confirmations'])
            self.time.text = str(_asa['time'])
            self.blocktime.text = str(_asa['blocktime'])

        self.manager.current = 'transaction_screen'

    def view_inputs(self):
        self.pvin.open()

    def view_outputs(self):
        self.pvout.open()

    def view_hex(self):
        self.phex.open()

    def view_json(self):
        self.pjson.open()
