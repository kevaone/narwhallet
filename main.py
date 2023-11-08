from functools import partial
import os
import sys
import threading
import time
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.utils import platform
from kivy.core.window import Window
from kivy.properties import NumericProperty
from narwhallet.core.kui.widgets.nwpasswordpopup import Nwpasswordpopup
from narwhallet.core.kui.widgets.nwsetpasswordpopup import Nwsetpasswordpopup
from narwhallet.core.kui.widgets.nwwarnpopup  import Nwwarnpopup
from narwhallet import _version
from narwhallet.control.controller import Controller
# NOTE NarwhalletScreens import moved after set_paths called
# Config.set('graphics', 'width', '500')
# Config.set('graphics', 'height', '700')
from kivy.clock import Clock


Clock.max_iteration = 20

def resourcePath():
    '''Returns path containing content - either locally or in pyinstaller tmp file'''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)

    return os.path.join(os.path.abspath("."))

_program_path = os.path.dirname(__file__)

from narwhallet.core.kui.interface.screenmanager import NarwhalletScreens


class MainApp(App):
    lang = NumericProperty(0)
    icon = 'narwhallet/core/kui/assets/narwhal.png'
    title = 'Narwhallet v.' + str(_version.__version__)

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        self.ctrl = Controller(_program_path)
        self.lang = self.ctrl.lang_dat.data['active']
        self.exiting = False
        self.auto_lock_thread = threading.Thread(target=self.auto_lock_wallets)

    def on_request_close(self, *args, **kwargs):
        self.exiting = True

    def translate_text(self, text):
        _lang = self.ctrl.lang_dat.data['available'][self.lang][1]

        try:
            _t = self.ctrl.lang_dat.data['strings'][text][_lang]
        except:
            _t = text
        
        return _t

    def auto_lock_wallets(self):
        while self.exiting is False:
            if self.ctrl.settings.auto_lock_timer != 0:
                for _w in self.ctrl.wallets.wallets:
                    if _w.state_lock != 1:
                        continue

                    if _w.locked is True:
                        continue

                    if _w.updating is True:
                        continue

                    if time.time() - _w.unlocked <= self.ctrl.settings.auto_lock_timer:
                        continue

                    self._lock_wallet(_w, None)

                    if self.sm.current_screen.header.value == _w.name:
                        def go_home(*args):
                            self.sm.current = 'home_screen'
                        Clock.schedule_once(go_home, 0)
                                    
            time.sleep(1)

    def wallet_lock(self, wallet, instance):
        wallet = self.ctrl.wallets.get_wallet_by_name(wallet)
        if wallet.state_lock == 0:
            _msg = 'Wallet is not encrypted. Do you wish to encrypt?'
            warn_popup = Nwwarnpopup()
            warn_popup.msg._text = _msg
            warn_popup.bind(next=partial(self.set_wallet_lock, wallet, instance))
            warn_popup.open()
        elif wallet.state_lock == 1:
            if wallet.locked is True:
                pass_popup = Nwpasswordpopup()
                pass_popup.bind(next=partial(self._unlock_wallet, wallet, instance))
                pass_popup.open()
            else:
                self._lock_wallet(wallet, instance)

    def _lock_wallet(self, wallet, instance=None):
        if wallet.updating == True:
            return

        _reloaded = self.ctrl.wallets.relock_wallet(wallet.name)
        if _reloaded is True:
            if instance is not None:
                instance.lock_icon = 'narwhallet/core/kui/assets/lock.png'
            else:
                for _i in self.sm.home_screen.wallet_list.data:
                    if _i['wallet_name'] == wallet.name:
                        _i['lock_icon'] = 'narwhallet/core/kui/assets/lock.png'
                self.sm.home_screen.wallet_list.refresh_from_data()

    def _unlock_wallet(self, wallet, ref_instance, instance, next):
        wallet.set_k(instance.kpas.text)
        self.ctrl.wallets.load_wallet(wallet.name, wallet)
        ref_instance.lock_icon = 'narwhallet/core/kui/assets/lock-open.png'
        _wallet = self.ctrl.wallets.get_wallet_by_name(wallet.name)
        _wallet.set_unlocked(time.time())

    def set_wallet_lock(self, wallet, ref_instance, instance, next):
        pass_popup = Nwsetpasswordpopup()
        pass_popup.bind(next=partial(self._set_wallet_lock, wallet, ref_instance))
        pass_popup.open()

    def _set_wallet_lock(self, wallet, ref_instance, instance, next):
        wallet.set_k(instance.kpas.text)
        wallet.set_state_lock(1)
        wallet.set_locked(False)
        self.ctrl.wallets.save_wallet(wallet.name)
        self._lock_wallet(wallet, ref_instance)

    def build(self):
        self.sm = NarwhalletScreens()
        self.sm.program_path = _program_path
        self.sm.setup(self.ctrl.user_path)
        Window.bind(on_request_close=self.on_request_close)
        self.auto_lock_thread.start()
        
        return self.sm

if __name__ == '__main__':
    kivy.resources.resource_add_path(resourcePath())
    MainApp().run()
