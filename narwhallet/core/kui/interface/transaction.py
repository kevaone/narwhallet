from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.txinputlistinfo import TXInputListInfo
from narwhallet.core.kui.widgets.txoutputlistinfo import TXOutputListInfo
from narwhallet.core.kui.widgets.header import Header


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
    hex = ObjectProperty(None)
    confirmations = ObjectProperty(None)
    time = ObjectProperty(None)
    blocktime = ObjectProperty(None)
    header = Header()


    def populate(self, txid):
        self.header.value = self.manager.wallet_screen.header.value
        self.txid.text = txid
        _provider = self.manager.settings_screen.settings.content_providers[0]
        _asa = MShared.get_transaction(txid, _provider)
        self.vin.clear_widgets()
        self.vout.clear_widgets()
        if _asa is not None:
            # TODO Interface cache for rest of tx data
            self.tx_hash.text = _asa['hash'] # 'tx_hash'
            self.version.text = str(_asa['version']) # 'version'
            self.tx_size.text = str(_asa['size']) # 'tx_size'
            self.vsize.text = str(_asa['vsize']) # 'vsize'
            self.locktime.text = str(_asa['locktime']) # 'locktime'
            self.blockhash.text = _asa['blockhash'] # 'blockhash'
            for v in _asa['vin']:
                _i = TXInputListInfo()
                _i.txid.text = v['txid']
                _i.vout.text = str(v['vout'])
                self.vin.add_widget(_i)
                
            for o in _asa['vout']:
                _o = TXOutputListInfo()
                _o.n.text = str(o['n'])
                _o.value.text = str(round(o['value'], 8)) #str(o.value)
                _o.scriptpubkey_asm.text = o['scriptPubKey']['asm']
                self.vout.add_widget(_o)
            self.hex.text = _asa['hex'] # 'hex'
            self.confirmations.text = str(_asa['confirmations']) # 'confirmations'
            self.time.text = str(_asa['time']) # 'time'
            self.blocktime.text = str(_asa['blocktime']) # 'blocktime'

        self.manager.current = 'transaction_screen'
