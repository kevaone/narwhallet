from kivy.uix.modalview import ModalView
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class Nwpopup(ModalView):
    status = Nwlabel()

    def __init__(self, **kwargs):
        super(Nwpopup, self).__init__(**kwargs)
