import json
import os
import shutil
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.core.kcl.file_utils import ConfigLoader


class SettingsScreen(Screen):
    iserver_host = TextInput()
    iserver_port = TextInput()
    iserver_althost = TextInput()
    iserver_altport = TextInput()
    iserver_ssl_0 = ToggleButton()
    iserver_verify_0 = ToggleButton()
    iserver_altssl_0 = ToggleButton()
    iserver_altverify_0 = ToggleButton()
    iserver_ssl_1 = ToggleButton()
    iserver_verify_1 =ToggleButton()
    iserver_altssl_1 = ToggleButton()
    iserver_altverify_1 = ToggleButton()
    iserver_ipfs_0 = TextInput()
    iserver_ipfs_1 = TextInput()
    iserver_active_0 = ToggleButton()
    iserver_active_1 = ToggleButton()

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
        self.manager.kex.active_peer = self.settings.primary_peer

        for _p in self.settings.electrumx_peers:
            self.manager.kex.add_peer(_p[1], _p[2], _p[3], _p[4])

        self.iserver_host.text = self.settings.electrumx_peers[0][1]
        self.iserver_port.text = self.settings.electrumx_peers[0][2]
        self.iserver_althost.text = self.settings.electrumx_peers[1][1]
        self.iserver_altport.text = self.settings.electrumx_peers[1][2]

        if bool(self.settings.electrumx_peers[0][3]) is True:
            self.iserver_ssl_0.state = 'down'
            self.iserver_ssl_1.state = 'normal'
        else:
            self.iserver_ssl_0.state = 'normal'
            self.iserver_ssl_1.state = 'down'

        if bool(self.settings.electrumx_peers[0][4]) is True:
            self.iserver_verify_0.state = 'down'
            self.iserver_verify_1.state = 'normal'
        else:
            self.iserver_verify_0.state = 'normal'
            self.iserver_verify_1.state = 'down'

        if self.settings.primary_peer == 0:
            self.iserver_active_0.state = 'down'
            self.iserver_active_1.state = 'normal'
        else:
            self.iserver_active_0.state = 'normal'
            self.iserver_active_1.state = 'down'

        if bool(self.settings.electrumx_peers[1][3]) is True:
            self.iserver_altssl_0.state = 'down'
            self.iserver_altssl_1.state = 'normal'
        else:
            self.iserver_altssl_0.state = 'normal'
            self.iserver_altssl_1.state = 'down'

        if bool(self.settings.electrumx_peers[1][4]) is True:
            self.iserver_altverify_0.state = 'down'
            self.iserver_altverify_1.state = 'normal'
        else:
            self.iserver_altverify_0.state = 'normal'
            self.iserver_altverify_1.state = 'down'
        
        _special_keys = ConfigLoader(os.path.join(self.user_path,
                                                  'special_keys.json'))
        _special_keys.load()

    def update_host(self):
        self.settings.electrumx_peers[0][1] = self.iserver_host.text
        self.save_settings()

    def update_port(self):
        self.settings.electrumx_peers[0][2] = self.iserver_port.text
        self.save_settings()

    def update_althost(self):
        self.settings.electrumx_peers[1][1] = self.iserver_althost.text
        self.save_settings()

    def update_altport(self):
        self.settings.electrumx_peers[1][2] = self.iserver_altport.text
        self.save_settings()

    def update_ipfs(self):
        pass

    def update_altipfs(self):
        pass

    def update_active(self, value):
        self.settings.set_primary_peer(value)
        self.save_settings()

    def update_ipfa_active(self, value):
        pass

    def update_ssl_option(self, server, option, setting):
        if option not in (3, 4):
            return

        if isinstance(setting, bool) is False:
            return

        self.settings.electrumx_peers[server][option] = setting
        self.save_settings()

    def save_settings(self):
        self.set_dat.save(json.dumps(self.settings.to_dict()))
