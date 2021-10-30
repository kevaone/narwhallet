import os
from control.narwhallet_settings import MNarwhalletSettings
from control.narwhallet_web_settings import MNarwhalletWebSettings
from core.kex import KEXclient
from core.kcl.file_utils import ConfigLoader


class NarwhalletWebController():
    def __init__(self):
        # HACK
        _user_home = os.path.expanduser('~')
        self.user_path = os.path.join(_user_home, '.narwhallet')
        self.settings = MNarwhalletSettings()
        self.strap = MNarwhalletWebSettings()
        _settings_file = os.path.join(self.user_path, 'settings.json')
        self.set_dat = ConfigLoader(_settings_file)
        self.set_dat.load()
        self.settings.fromDict(self.set_dat.data)
        self.KEX = KEXclient()
        self.DF_KEX: KEXclient = KEXclient()
        _user_home = os.path.expanduser('~')
        _narwhallet_path = os.path.join(_user_home, '.narwhallet')
        _themes_dir = os.path.join(_narwhallet_path, 'narwhallet_web/themes')
        self.db_file = os.path.join(_narwhallet_path, 'narwhallet_cache.db')
        self.strapf = ConfigLoader(os.path.join(self.user_path, 'strap.json'))
        self.strapf.load()
        self.strap.fromDict(self.strapf.data)
        self.theme_path = os.path.join(_themes_dir, self.strap.theme)
        self.who = 'http://localhost:' + str(self.strap.port)

        for peer in self.settings.electrumx_peers:
            _ = self.KEX.add_peer(peer[1], int(peer[2]),
                                  peer[3] == 'True', peer[4] == 'True')

        self.KEX.active_peer = self.settings.primary_peer
        if self.settings.electrumx_auto_connect:
            self.KEX.peers[self.settings.primary_peer].connect()

        self.DF_KEX.active_peer = 0
        # TODO Refine settings config; hardcoded from default for now
        _ = self.DF_KEX.add_peer('keva.one', 443, True, True)
