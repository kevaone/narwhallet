import os
import shutil
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from narwhallet.core.kex import KEXclient
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets
from narwhallet.core.kui.widgets.walletlistinfo import WalletListInfo
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo
from narwhallet.core.kui.widgets.namespacelistinfo import NamespaceListInfo
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.interface.address import AddressScreen
from narwhallet.core.kui.interface.addresses import AddressesScreen
from narwhallet.core.kui.interface.create import CreateScreen
from narwhallet.core.kui.interface.content import ContentScreen
from narwhallet.core.kui.interface.market import MarketScreen
from narwhallet.core.kui.interface.namespace import NamespaceScreen
from narwhallet.core.kui.interface.namespaces import NamespacesScreen
from narwhallet.core.kui.interface.offers import OffersScreen
from narwhallet.core.kui.interface.pending import PendingScreen
from narwhallet.core.kui.interface.block import BlockScreen
from narwhallet.core.kui.interface.home import HomeScreen
from narwhallet.core.kui.interface.wallet import WalletScreen
from narwhallet.core.kui.interface.walletinfo import WalletInfoScreen
from narwhallet.core.kui.interface.restore import RestoreScreen
from narwhallet.core.kui.interface.receive import ReceiveScreen

from narwhallet.core.kui.interface.send import SendScreen
from narwhallet.core.kui.interface.settings import SettingsScreen
from narwhallet.core.kui.interface.transaction import TransactionScreen
from narwhallet.core.kui.interface.transactions import TransactionsScreen


class NarwhalletScreens(ScreenManager):
    address_screen = ObjectProperty(None)
    addresses_screen = ObjectProperty(None)
    block_screen = ObjectProperty(None)
    content_screen = ObjectProperty(None)
    home_screen = ObjectProperty(None)
    market_screen = ObjectProperty(None)
    namespace_screen = ObjectProperty(None)
    namespaces_screen = ObjectProperty(None)
    offers_screen = ObjectProperty(None)
    pending_screen = ObjectProperty(None)
    send_screen = ObjectProperty(None)
    settings_screen = ObjectProperty(None)
    transaction_screen = ObjectProperty(None)
    transactions_screen = ObjectProperty(None)
    wallet_screen = ObjectProperty(None)
    walletinfo_screen = ObjectProperty(None)
    create_screen = ObjectProperty(None)
    restore_screen = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(NarwhalletScreens, self).__init__(**kwargs)

        self.wallets = MWallets()
        self.user_path = self.set_paths()
        self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')
        self.cache = MCache(self.cache_path)
        self.kex = KEXclient()

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

    def load_wallets(self):
        self.wallets.set_root_path(os.path.join(self.user_path, 'wallets'))

        for file in os.listdir(self.wallets.root_path):
            _tf = os.path.isdir(os.path.join(self.wallets.root_path, file))
            if _tf is False:
                self.wallets.load_wallet(file)

    def setup(self):
        self.cache.interface.setup_tables()
        self.settings_screen.load_settings()
        self.kex.peers[self.kex.active_peer].connect()
        
        self.load_wallets()
        self.home_screen.populate()
