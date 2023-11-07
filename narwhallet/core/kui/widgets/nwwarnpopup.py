from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty
from narwhallet.core.kui.widgets.nwlabel import Nwlabel


class Nwwarnpopup(ModalView):
    msg = Nwlabel()
    next = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Nwwarnpopup, self).__init__(**kwargs)

    def on_next(self, *args):
        self.dismiss()
