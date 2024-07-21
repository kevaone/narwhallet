from functools import partial
import os
import time
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.psbt_decoder import keva_psbt
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kui.widgets.mediabrowsepopup import Mediabrowsepopup
from narwhallet.core.kui.widgets.nwpopup import Nwpopup
from narwhallet.core.kui.widgets.psbtlistinfo import PsbtListInfo
from narwhallet.core.kui.widgets.txinputlistinfo import TXInputListInfo
from narwhallet.core.kui.widgets.txinputlistpopup import Txinputlistpopup
from narwhallet.core.kui.widgets.txoutputlistinfo import TXOutputListInfo
from narwhallet.core.kui.widgets.header import Header
from narwhallet.core.kui.widgets.txoutputlistpopup import Txoutputlistpopup
from narwhallet.core.kui.widgets.nwboxlayout import Nwboxlayout
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class PsbtScreen(Screen):
    version = Nwlabel()
    tx_size = Nwlabel()
    vsize = Nwlabel()
    locktime = Nwlabel()
    vin = Nwlabel()
    vout = Nwlabel()
    global_box = Nwboxlayout()
    header = Header()

    def __init__(self, **kwargs):
        super(PsbtScreen, self).__init__(**kwargs)

        self.pvin = Txinputlistpopup()
        self.pvout = Txoutputlistpopup()
        
        # self.phex = Nwpopup()
        # self.pjson = Nwpopup()
        self.app = App.get_running_app()
        self.psbt = None

    def populate(self):
        self.header.value = self.manager.wallet_screen.header.value
        #     self.phex.status._text = _asa['hex']
        #     self.phex.header.value = 'HEX'
        #     self.pjson.status._text = json.dumps(_asa, indent=4)
        #     self.pjson.header.value = 'JSON'

        self.manager.current = 'psbt_screen'

    def view_inputs(self):
        self.pvin.open()

    def view_outputs(self):
        self.pvout.open()

    # def view_hex(self):
    #     self.phex.open()

    # def view_json(self):
    #     self.pjson.open()

    def view_save(self):
        if self.psbt is not None:
            _p = Ut.bytes_to_hex(self.psbt.serialize())
            _name = 'test_bid_' + str(time.time_ns())
            self.app.ctrl.save_psbt(_p, _name)

    def view_browse(self):
        _browse = Mediabrowsepopup()
        _browse.bind(psbt=partial(self.load_psbt))
        _browse.popen(os.path.join(self.app.ctrl.user_path, 'saved_psbt'))

    def load_psbt(self, instance: Mediabrowsepopup, value: str):
        _psbt: keva_psbt = self.app.ctrl.load_psbt(value)
        self.psbt = _psbt
        self.pvin.vin.clear_widgets()
        self.pvout.vout.clear_widgets()

        for _g in _psbt.globals_to_list():
            _e = PsbtListInfo()
            _e.key_name._text = _g[0]
            if isinstance(_g[1], bytes):
                _e.value_data._text = Ut.bytes_to_hex(_g[1])
            else:
                _e.key_data._text = Ut.bytes_to_hex(_g[1][0])
                _e.value_data._text = Ut.bytes_to_hex(_g[1][1])
            self.global_box.add_widget(_e)

        self.vin.text = str(len(_psbt.tx.vin))
        self.vout.text = str(len(_psbt.tx.vout))
        for idx, v in enumerate(_psbt.tx.vin):
            _i = TXInputListInfo()
            _i.txid._text = Ut.bytes_to_hex(v.txid)
            _i.vout._text = str(Ut.bytes_to_int(v.vout, 'little'))
            _i.sequence._text = str(Ut.bytes_to_hex(v.sequence))
            _i.scriptsig._text = str(Ut.bytes_to_hex(v.scriptsig.script))

            for _inp in _psbt.get_input(idx):
                _e = PsbtListInfo()
                _e.key_name._text = _inp[0]
                if isinstance(_inp[1], bytes):
                    _e.value_data._text = Ut.bytes_to_hex(_inp[1])
                else:
                    _e.key_data._text = Ut.bytes_to_hex(_inp[1][0])
                    _e.value_data._text = Ut.bytes_to_hex(_inp[1][1])

                _i.children[0].add_widget(_e)
            self.pvin.vin.add_widget(_i)

        for i, o in enumerate(_psbt.tx.vout):
            _o = TXOutputListInfo()
            _o.n._text = str(i)
            _o.value._text = str(round(Ut.from_sats(Ut.bytes_to_int(o.amount, 'little')), 8))
            _o.scriptpubkey_asm._text = Ut.bytes_to_hex(o.scriptpubkey.script)

            for _out in _psbt.get_output(idx):
                _e = PsbtListInfo()
                _e.key_name._text = _out[0]
                if isinstance(_out[1], bytes):
                    _e.value_data._text = Ut.bytes_to_hex(_out[1])
                else:
                    _e.key_data._text = Ut.bytes_to_hex(_out[1][0])
                    _e.value_data._text = Ut.bytes_to_hex(_out[1][1])

                _o.children[0].add_widget(_e)
            self.pvout.vout.add_widget(_o)
