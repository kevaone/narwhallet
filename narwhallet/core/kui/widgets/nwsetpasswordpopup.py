import time
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class Nwsetpasswordpopup(ModalView):
    kpas = TextInput()
    ckpas = TextInput()
    btn_next = Nwbutton()
    next = BooleanProperty(False)

    def __init__(self, wallet, **kwargs):
        super(Nwsetpasswordpopup, self).__init__(**kwargs)

        self.wallet: MWallet = wallet

    def on_next_click(self, *args):
        app = App.get_running_app()
        self.wallet.set_k(self.kpas.text)
        try:
            self.wallet.set_k(self.kpas.text)
            self.wallet.set_state_lock(1)
            self.wallet.set_locked(False)
            app.ctrl.wallets.save_wallet(self.wallet.name)

            self.next = True
        except:
            # TODO Add Error Dialog
            pass

    def on_next(self, *args):
        self.dismiss()

    def on_open(self, *args):
        self.kpas.focus = True

    def verify(self):
        if self.kpas.text != '':
            if self.kpas.text == self.ckpas.text:
                self.btn_next.disabled = False
                return
        self.btn_next.disabled = True
