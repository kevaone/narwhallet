import os
import shutil
from kivy.uix.screenmanager import Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.core.kcl.file_utils import ConfigLoader


class SettingsScreen(Screen):

    iserver_host = ObjectProperty(None)
    iserver_port = ObjectProperty(None)
    iserver_althost = ObjectProperty(None)
    iserver_altport = ObjectProperty(None)

    def set_paths(self) -> str:
        _user_home = os.path.expanduser('~')
        _narwhallet_path = os.path.join(_user_home, '.narwhallet')

        if os.path.isdir(_narwhallet_path) is False:
            # TODO Add error handling
            os.mkdir(_narwhallet_path)
            os.mkdir(os.path.join(_narwhallet_path, 'wallets'))

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'settings.json')) is False:
            print('settings.json created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/settings.json'), _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'narwhallet.addressbook')) is False:
            print('narwhallet.addressbook created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/narwhallet.addressbook'),
                        _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'special_keys.json')) is False:
            print('special_keys.json created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/special_keys.json'),
                        _narwhallet_path)

        return _narwhallet_path

    def load_settings(self):
        # TODO Clean up
        self.settings: MNarwhalletSettings = MNarwhalletSettings()
        self.user_path = self.set_paths()
        self.set_dat = ConfigLoader(os.path.join(self.user_path,
                                                 'settings.json'))
        self.set_dat.load()
        self.settings.from_dict(self.set_dat.data)

        self.iserver_host.text = self.settings.electrumx_peers[0][1]
        self.iserver_port.text = self.settings.electrumx_peers[0][2]
        self.iserver_althost.text = self.settings.electrumx_peers[1][1]
        self.iserver_altport.text = self.settings.electrumx_peers[1][2]
        
        _special_keys = ConfigLoader(os.path.join(self.user_path,
                                                  'special_keys.json'))
        _special_keys.load()
