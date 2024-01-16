from kivy.uix.modalview import ModalView
from narwhallet.core.kui.widgets.nwlabel import Nwlabel
from narwhallet.core.kui.widgets.header import Header


class Nwpopup(ModalView):
    status = Nwlabel()
    header = Header()

    def __init__(self, **kwargs):
        super(Nwpopup, self).__init__(**kwargs)
