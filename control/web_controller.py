import os
from control.narwhallet_settings import MNarwhalletSettings
from control.narwhallet_web_settings import MNarwhalletWebSettings

from core.kcl.models.transactions import MTransactions
from core.kcl.models.namespaces import MNamespaces
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
        self.tx_cache = MTransactions()
        self.ns_cache = MNamespaces()
        # self.address_book = MBookAddresses()
        # self._db_cache = _db_cache
        self.KEX = KEXclient()

        _user_home = os.path.expanduser('~')
        _narwhallet_path = os.path.join(_user_home, '.narwhallet')
        _themes_dir = os.path.join(_narwhallet_path, 'narwhallet_web/themes')
        strap_file = os.path.join(_narwhallet_path, 'strap.json')
        self.db_file = os.path.join(_narwhallet_path, 'narwhallet_cache.db')
        self.strap.load(strap_file)
        self.theme_path = os.path.join(_themes_dir, self.strap.theme)
        self.who = 'http://localhost:' + str(self.strap.port)

        for peer in self.settings.electrumx_peers:
            _ = self.KEX.add_peer(peer[1], int(peer[2]),
                                  peer[3] == 'True', peer[4] == 'True')

        self.KEX.active_peer = self.settings.primary_peer
        if self.settings.electrumx_auto_connect:
            self.KEX.peers[self.settings.primary_peer].connect()
