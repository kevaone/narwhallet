import os
import shutil
from kivy.utils import platform
from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.control.shared import MShared
from narwhallet.core.kcl.file_utils.io import ConfigLoader
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kcl.wallet.wallets import MWallets
from narwhallet.core.kex.KEXc import KEXclient


class Controller():
    def __init__(self, _program_path):
        self.user_path = self.set_paths(_program_path)
        _translations = os.path.join(self.user_path, 'translations.json')
        self.lang_dat = ConfigLoader(_translations)
        self.lang_dat.load()

        self.settings: MNarwhalletSettings = MNarwhalletSettings()
        self.set_dat = ConfigLoader(os.path.join(self.user_path,
                                                 'settings.json'))
        self.set_dat.load()
        self.settings.from_dict(self.set_dat.data)
        self.kex = KEXclient()
        self.wallets = MWallets()
        self.load_wallets()

    def set_paths(self, program_path) -> str:
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

    def load_wallets(self):
        self.wallets.set_root_path(os.path.join(self.user_path, 'wallets'))

        for file in os.listdir(self.wallets.root_path):
            _tf = os.path.isdir(os.path.join(self.wallets.root_path, file))
            if _tf is False:
                self.wallets.load_wallet(file)
