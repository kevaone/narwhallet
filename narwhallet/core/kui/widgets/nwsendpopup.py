import json
from kivy.uix.modalview import ModalView
from narwhallet.core.kex.KEXc import KEXclient
from narwhallet.control.shared import MShared
from narwhallet.core.kui.widgets.nwpopup import Nwpopup
from kivy.properties import StringProperty, NumericProperty


class Nwsendpopup(ModalView):
    provider = KEXclient()
    in_value = StringProperty()
    out_value = StringProperty()
    change_value = StringProperty()
    fee = StringProperty()
    fee_rate = StringProperty()
    txsize = StringProperty()
    txhex = StringProperty()
    return_screen = StringProperty()
    msgType = NumericProperty()

    def __init__(self, **kwargs):
        super(Nwsendpopup, self).__init__(**kwargs)

    def process_send(self):
        _bc_result = MShared.broadcast(self.txhex, self.provider)
        if isinstance(_bc_result[1], dict):
            _result = json.dumps(_bc_result[1])
        else:
            _result = _bc_result[1]

        self.msgType = int(_bc_result[0])

        result_popup = Nwpopup()

        if self.msgType == 1:
            result_popup.status._text = 'Error' + ':\n' + _result
        elif self.msgType == 2:
            result_popup.status._text = 'Ok!'

        result_popup.open()
        self.dismiss()
