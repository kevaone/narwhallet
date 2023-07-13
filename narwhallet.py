import os
import sys
import kivy
from kivy.app import App
from kivy.config import Config
from narwhallet.core.kui.interface.screenmanager import NarwhalletScreens
# Config.set('graphics', 'width', '500')
# Config.set('graphics', 'height', '700')

def resourcePath():
    '''Returns path containing content - either locally or in pyinstaller tmp file'''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)

    return os.path.join(os.path.abspath("."))

class NarwhalletApp(App):
    icon = 'narwhallet/core/kui/assets/narwhal.png'

    def build(self):
        _program_path = os.path.dirname(__file__)
        self.sm = NarwhalletScreens()
        self.sm.program_path = _program_path
        self.sm.setup()
        
        return self.sm

if __name__ == '__main__':
    kivy.resources.resource_add_path(resourcePath())
    NarwhalletApp().run()