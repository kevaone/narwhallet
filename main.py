import os
import sys
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.utils import platform
from kivy.properties import NumericProperty
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

    def translate_text(self, text):
        _lang = self.ctrl.lang_dat.data['available'][self.lang][1]

        try:
            _t = self.ctrl.lang_dat.data['strings'][text][_lang]
        except:
            _t = text
        
        return _t

    def build(self):
        self.sm = NarwhalletScreens()
        self.sm.program_path = _program_path
        self.sm.setup(self.ctrl.user_path)
        
        return self.sm

if __name__ == '__main__':
    kivy.resources.resource_add_path(resourcePath())
    MainApp().run()
