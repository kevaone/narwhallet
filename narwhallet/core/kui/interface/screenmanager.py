import os
import re
import shutil
from kivy.uix.screenmanager import ScreenManager
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from narwhallet.core.kcl.enums.mediatypes import content_type
from narwhallet.core.kcl.favorites.favorites import MFavorites
from narwhallet.core.kcl.file_utils.io import _loader
from narwhallet.core.kex import KEXclient
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MWallets
from narwhallet.core.kex.cmd import _custom
from narwhallet.core.kex.peer import _peer
from narwhallet.core.kui.widgets.walletlistinfo import WalletListInfo
from narwhallet.core.kui.widgets.addresslistinfo import AddressListInfo
from narwhallet.core.kui.widgets.transactionlistinfo import TransactionListInfo
from narwhallet.core.kui.widgets.namespacelistinfo import NamespaceListInfo
from narwhallet.core.kui.widgets.namespaceinfo import NamespaceInfo
from narwhallet.core.kui.widgets.marketlistinfo import MarketListInfo
from narwhallet.core.kui.widgets.auctionlistinfo import AuctionListInfo
from narwhallet.core.kui.widgets.bidlistinfo import BidListInfo
from narwhallet.core.kui.widgets.favoritelistinfo import FavoriteListInfo
from narwhallet.core.kui.widgets.addressbooklistinfo import AddressBookListInfo
from narwhallet.core.kui.widgets.alllistinfo import AllListInfo
from narwhallet.core.kui.widgets.nftlistinfo import NftListInfo
from narwhallet.core.kui.interface.address import AddressScreen
from narwhallet.core.kui.interface.addressbook import AddressBookScreen
from narwhallet.core.kui.interface.addressbookentry import AddressBookEntryScreen
from narwhallet.core.kui.interface.addaddressbookentry import AddAddressBookEntryScreen
from narwhallet.core.kui.interface.addresses import AddressesScreen
from narwhallet.core.kui.interface.create import CreateScreen
from narwhallet.core.kui.interface.createnamespace import CreateNamespaceScreen
from narwhallet.core.kui.interface.createnamespacekey import CreateNamespaceKeyScreen
from narwhallet.core.kui.interface.content import ContentScreen
from narwhallet.core.kui.interface.market import MarketScreen
from narwhallet.core.kui.interface.auctionnamespace import AuctionNamespaceScreen
from narwhallet.core.kui.interface.bidnamespace import BidNamespaceScreen
from narwhallet.core.kui.interface.namespace import NamespaceScreen
from narwhallet.core.kui.interface.namespacealt import NamespaceAltScreen
from narwhallet.core.kui.interface.namespaces import NamespacesScreen
from narwhallet.core.kui.interface.auctions import AuctionsScreen
from narwhallet.core.kui.interface.bids import BidsScreen
from narwhallet.core.kui.interface.block import BlockScreen
from narwhallet.core.kui.interface.home import HomeScreen
from narwhallet.core.kui.interface.wallet import WalletScreen
from narwhallet.core.kui.interface.walletinfo import WalletInfoScreen
from narwhallet.core.kui.interface.restore import RestoreScreen
from narwhallet.core.kui.interface.receive import ReceiveScreen
from narwhallet.core.kui.interface.scriptbuilder import ScriptBuilderScreen
from narwhallet.core.kui.interface.send import SendScreen
from narwhallet.core.kui.interface.settings import SettingsScreen
from narwhallet.core.kui.interface.transaction import TransactionScreen
from narwhallet.core.kui.interface.transactions import TransactionsScreen
from narwhallet.core.kui.interface.transfernamespace import TransferNamespaceScreen
from narwhallet.core.kui.interface.utils import UtilsScreen
from narwhallet.core.kcl.addr_book import MBookAddresses
from narwhallet.core.kui.interface.favorites import FavoritesScreen
from narwhallet.core.kui.interface.favorite import FavoriteScreen
from narwhallet.core.kui.interface.about import AboutScreen
from narwhallet.core.kui.interface.auctiondetail import AuctionDetailScreen
from narwhallet.core.kui.interface.biddetail import BidDetailScreen
from narwhallet.core.kui.interface.acceptnamespacebid import AcceptNamespaceBidScreen
from narwhallet.core.kui.interface.all import AllScreen
from narwhallet.core.kui.interface.alldetail import AllDetailScreen
from narwhallet.core.kui.interface.nft import NftScreen
from narwhallet.core.kui.interface.nftdetail import NftDetailScreen


class NarwhalletScreens(ScreenManager):
    address_screen = AddressScreen()
    addressbook_screen = AddressBookScreen()
    addressbookentry_screen = AddressBookEntryScreen()
    addaddressbookentry_screen = AddAddressBookEntryScreen()
    addresses_screen = AddressesScreen()
    block_screen = BlockScreen()
    content_screen = ContentScreen()
    home_screen = HomeScreen()
    market_screen = MarketScreen()
    namespace_screen = NamespaceScreen()
    namespacealt_screen = NamespaceAltScreen()
    namespaces_screen = NamespacesScreen()
    auctionnamespace_screen = AuctionNamespaceScreen()
    auctiondetail_screen = AuctionDetailScreen()
    biddetail_screen = BidDetailScreen()
    auctions_screen = AuctionsScreen()
    bids_screen = BidsScreen()
    bidnamespace_screen = BidNamespaceScreen()
    scriptbuilder_screen = ScriptBuilderScreen()
    send_screen = SendScreen()
    receive_screen = ReceiveScreen()
    settings_screen = SettingsScreen()
    transaction_screen = TransactionScreen()
    transactions_screen = TransactionsScreen()
    wallet_screen = WalletScreen()
    walletinfo_screen = WalletInfoScreen()
    create_screen = CreateScreen()
    createnamespace_screen = CreateNamespaceScreen()
    createnamespacekey_screen = CreateNamespaceKeyScreen()
    restore_screen = RestoreScreen()
    transfernamespaces_screen = TransferNamespaceScreen()
    utils_screen = UtilsScreen()
    favorites_screen = FavoritesScreen()
    favorite_screen = FavoriteScreen()
    about_screen = AboutScreen()
    acceptnamespacebid_screen = AcceptNamespaceBidScreen()
    all_screen = AllScreen()
    alldetail_screen = AllDetailScreen()
    nft_screen = NftScreen()
    nftdetail_screen = NftDetailScreen()
    
    def __init__(self, **kwargs):
        super(NarwhalletScreens, self).__init__(**kwargs)

        self.wallets = MWallets()
        self.address_book: MBookAddresses = MBookAddresses()
        self.favorites: MFavorites = MFavorites()
        self.program_path = ''
        # self.user_path = '' #self.set_paths()
        # self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')
        # self.cache = MCache(self.cache_path)
        # self.kex = KEXclient()

    def set_paths(self) -> str:
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
            shutil.copy(os.path.join(self.program_path,
                                     'config/settings.json'), _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'narwhallet.addressbook')) is False:
            print('narwhallet.addressbook created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/narwhallet.addressbook'),
                        _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'narwhallet.favorites')) is False:
            print('narwhallet.favorites created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/narwhallet.favorites'),
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
        self.user_path = self.set_paths()
        self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')
        self.ipfs_cache_path = os.path.join(self.user_path, 'tmp_ipfs')
        self.cache = MCache(self.cache_path)
        self.kex = KEXclient()
        self.cache.interface.setup_tables()
        self.settings_screen.load_settings()
        self.address_book.load_address_book(self.user_path)
        self.favorites.load_favorites(self.user_path)
        _connection_status = self.kex.peers[self.kex.active_peer].connect()
        self.settings_screen.connection_status = _connection_status
        
        self.load_wallets()
        self.home_screen.populate()

    def copy_to_clipboard(self, data):
        Clipboard.copy(data)

    def paste_from_clipboard(self):
        self.text = Clipboard.paste()

    def cache_IPFS(self, _item):
        _ipfs_images = re.findall(r'\{\{[^|image(|/png|/jpeg|/jpg|/gif)\}\}].*|image|image/png|image/jpeg|image/jpg|image/gif\}\}', _item)
        _data_peer = _peer('gateway.ipfs.io', 443, True, True)
        _images = []
        # https://gateway.ipfs.io/ipfs/
        # https://ipfs.sloppyta.co/ipfs/
        for _image in _ipfs_images:
            _image = _image.replace('{{', '')
            _image = _image.replace('}}', '')
            _image = _image.split('|')
            if len(_image) == 2:
                for _c in content_type:
                    if _image[1] == _c.value:
                        _extension = _c.name
                        break

                    if _image[1] == 'image':
                        _extension = 'jpg'
                        break

                if os.path.isfile(os.path.join(self.ipfs_cache_path,
                                        _image[0] + '.' + _extension)) is False:
                    _data_peer.connect()
                    _data_test = _data_peer.comm(_custom.get_web_content('gateway.ipfs.io', '/ipfs/' + _image[0], 1))
                    _tt = _data_test.split(b'\r\n\r\n')

                    if _tt != [b'']:
                        _ = _loader._save(os.path.join(self.ipfs_cache_path, _image[0] + '.' + _extension), _tt[1])
                _images.append(os.path.join(self.ipfs_cache_path,
                                        _image[0] + '.' + _extension))
        return _images
