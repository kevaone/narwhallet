from kivy.uix.modalview import ModalView
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class Nwrefreshpopup(ModalView):
    msg = Nwlabel()

    def __init__(self, **kwargs):
        super(Nwrefreshpopup, self).__init__(**kwargs)
