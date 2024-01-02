import time
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kui.widgets.nwbutton import Nwbutton


class Nwpasswordpopup(ModalView):
    kpas = TextInput()
    ckpas = TextInput()
    btn_next = Nwbutton()
    next = BooleanProperty(False)

    def __init__(self, wallet, **kwargs):
        super(Nwpasswordpopup, self).__init__(**kwargs)

        self.wallet: MWallet = wallet

    def on_next_click(self, *args):
        app = App.get_running_app()
        self.wallet.set_k(self.kpas.text)
        try:
            app.ctrl.wallets.load_wallet(self.wallet.name, self.wallet)
            _wallet = app.ctrl.wallets.get_wallet_by_name(self.wallet.name)
            if _wallet is not None:
                _wallet.set_unlocked(time.time())
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
            self.btn_next.disabled = False
            return
        self.btn_next.disabled = True

    def on_enter(self, *args):
        if self.kpas.text != '':
            self.on_next_click()
