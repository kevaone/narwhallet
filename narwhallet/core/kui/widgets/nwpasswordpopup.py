from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class Nwpasswordpopup(ModalView):
    kpas = TextInput()
    ckpas = TextInput()
    btn_next = Nwbutton()
    next = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Nwpasswordpopup, self).__init__(**kwargs)

    def on_next(self, *args):
        self.dismiss()

    def verify(self):
        if self.kpas.text != '':
            self.btn_next.disabled = False
            return
        self.btn_next.disabled = True
