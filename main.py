import os
import shutil
import sys
import kivy
from kivy.app import App
from kivy.config import Config
from kivy.utils import platform
from kivy.properties import NumericProperty
from narwhallet import _version
from narwhallet.core.kcl.file_utils.io import ConfigLoader
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

def set_paths(program_path) -> str:
    if platform != 'android':
        _user_home = os.path.expanduser('~')
    else:
        _user_home = '/data/user/0/one.keva.narwhallet/files/'

    _narwhallet_path = os.path.join(_user_home, '.narwhallet')

    if os.path.isdir(_narwhallet_path) is False:
        # TODO Add error handling
        os.mkdir(_narwhallet_path)
        os.mkdir(os.path.join(_narwhallet_path, 'wallets'))

    if os.path.isdir(os.path.join(_narwhallet_path, 'tmp_ipfs')) is False:
        # TODO Add error handling
        os.mkdir(os.path.join(_narwhallet_path, 'tmp_ipfs'))

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'settings.json')) is False:
        print('settings.json created.')
        shutil.copy(os.path.join(program_path,
                                    'config/settings.json'), _narwhallet_path)

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'narwhallet.addressbook')) is False:
        print('narwhallet.addressbook created.')
        shutil.copy(os.path.join(program_path,
                                    'config/narwhallet.addressbook'),
                    _narwhallet_path)

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'narwhallet.favorites')) is False:
        print('narwhallet.favorites created.')
        shutil.copy(os.path.join(program_path,
                                    'config/narwhallet.favorites'),
                    _narwhallet_path)

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'narwhallet.mymedia')) is False:
        print('narwhallet.mymedia created.')
        shutil.copy(os.path.join(program_path,
                                    'config/narwhallet.mymedia'),
                    _narwhallet_path)

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'special_keys.json')) is False:
        print('special_keys.json created.')
        shutil.copy(os.path.join(program_path,
                                    'config/special_keys.json'),
                    _narwhallet_path)

    if os.path.isfile(os.path.join(_narwhallet_path,
                                    'translations.json')) is False:
        print('translations.json created.')
        shutil.copy(os.path.join(program_path,
                                    'config/translations.json'), _narwhallet_path)

    return _narwhallet_path

_program_path = os.path.dirname(__file__)
_user_path = set_paths(_program_path)


from narwhallet.core.kui.interface.screenmanager import NarwhalletScreens


class MainApp(App):
    lang = NumericProperty(0)
    icon = 'narwhallet/core/kui/assets/narwhal.png'
    title = 'Narwhallet v.' + str(_version.__version__)

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        _translations = os.path.join(_user_path, 'translations.json')
        self.lang_dat = ConfigLoader(_translations)
        self.lang_dat.load()
        self.lang = self.lang_dat.data['active']

    def translate_text(self, text):
        _lang = self.lang_dat.data['available'][self.lang][1]

        try:
            _t = self.lang_dat.data['strings'][text][_lang]
        except:
            _t = text
        
        return _t

    def build(self):
        self.sm = NarwhalletScreens()
        self.sm.program_path = _program_path
        self.sm.setup(_user_path)
        
        return self.sm

if __name__ == '__main__':
    kivy.resources.resource_add_path(resourcePath())
    MainApp().run()
