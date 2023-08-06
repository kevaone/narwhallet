from typing import List


class MNarwhalletSettings():
    def __init__(self):
        self._auto_lock_timer: int = 60
        self._electrumx_auto_connect: bool = False
        self._electrumx_peers: List[list] = []
        self._enabled_coins: list = ['KEVACOIN']
        self._primary_peer: int = -1
        self._show_change: bool = False
        self._sync: dict = {}
        self._ipfs_providers: List[str] = []
        self._primary_ipfs_provider: int = -1
        self._content_providers: List[list] = []

    @property
    def auto_lock_timer(self) -> int:
        return self._auto_lock_timer

    @property
    def content_providers(self) -> List[list]:
        return self._content_providers

    @property
    def electrumx_auto_connect(self) -> bool:
        return self._electrumx_auto_connect

    @property
    def electrumx_peers(self) -> List[list]:
        return self._electrumx_peers

    @property
    def enabled_coins(self) -> list:
        return self._enabled_coins

    @property
    def ipfs_providers(self) -> List[str]:
        return self._ipfs_providers

    @property
    def primary_ipfs_provider(self) -> int:
        return self._primary_ipfs_provider

    @property
    def primary_peer(self) -> int:
        return self._primary_peer

    @property
    def show_change(self) -> bool:
        return self._show_change

    @property
    def sync(self) -> dict:
        return self._sync

    def add_content_provider(self, provider: list) -> None:
        self._content_providers.append(provider)

    def add_electrumx_peer(self, peer: list) -> None:
        self._electrumx_peers.append(peer)

    def add_enabled_coin(self, name: str) -> None:
        # TODO Check vaild support in bip_utils...
        self._enabled_coins.append(name)

    def add_ipfs_provider(self, provider: str) -> None:
        self._ipfs_providers.append(provider)

    def set_auto_lock_timer(self, interval: int) -> None:
        self._auto_lock_timer = interval

    def set_electrumx_auto_connect(self, auto_connect: bool) -> None:
        self._electrumx_auto_connect = auto_connect

    def set_content_providers(self, providers: List[list]) -> None:
        self._content_providers = providers
    
    def set_electrumx_peers(self, peers: List[list]) -> None:
        self._electrumx_peers = peers

    def set_enabled_coins(self, enabled_coins: list) -> None:
        self._enabled_coins = enabled_coins

    def set_ipfs_providers(self, providers: List[str]) -> None:
        self._ipfs_providers = providers

    def set_primary_peer(self, peer: int) -> None:
        self._primary_peer = peer

    def set_primary_ipfs_provider(self, provider: int) -> None:
        self._primary_ipfs_provider = provider

    def set_show_change(self, show_change: bool) -> None:
        self._show_change = show_change

    def set_sync(self, sync: dict) -> None:
        self._sync = sync

    def set_sync_by_name(self, name: str, sync: bool) -> None:
        self._sync[name] = sync

    def from_dict(self, _d: dict) -> None:
        if 'auto_lock_timer' in _d:
            self.set_auto_lock_timer(_d['auto_lock_timer'])
        if 'content_providers' in _d:
            if len(_d['content_providers']) == 0:
                self.set_content_providers([['', '', '', False, False]])
            else:
                self.set_content_providers(_d['content_providers'])
        else:
            self.set_content_providers([['', '', '', False, False]])
        self.set_electrumx_auto_connect(_d['electrumx_auto_connect'])
        self.set_electrumx_peers(_d['electrumx_peers'])
        if 'ipfs_providers' in _d:
            if len(_d['ipfs_providers']) == 0:
                self.set_ipfs_providers(['', ''])
            else:
                self.set_ipfs_providers(_d['ipfs_providers'])
        else:
            self.set_ipfs_providers(['', ''])
        if 'enabled_coins' in _d:
            self.set_enabled_coins(_d['enabled_coins'])
        # TEMP Check to prevent error, remove after participients have update
        if 'primary_peer' in _d:
            self.set_primary_peer(_d['primary_peer'])
        else:
            self.set_primary_peer(0)

        if 'primary_ipfs_provider' in _d:
            self.set_primary_ipfs_provider(_d['primary_ipfs_provider'])
        else:
            self.set_primary_ipfs_provider(0)

        if 'show_change' in _d:
            self.set_show_change(_d['show_change'])
        self.set_sync(_d['sync'])

    def to_dict(self) -> dict:
        _d = {}
        _d['auto_lock_timer'] = self.auto_lock_timer
        _d['content_providers'] = self.content_providers
        _d['electrumx_auto_connect'] = self.electrumx_auto_connect
        _d['electrumx_peers'] = self.electrumx_peers
        _d['ipfs_providers'] = self.ipfs_providers
        _d['enabled_coins'] = self.enabled_coins
        _d['primary_peer'] = self.primary_peer
        _d['primary_ipfs_provider'] = self.primary_ipfs_provider
        _d['show_change'] = self.show_change
        _d['sync'] = self.sync

        return _d
