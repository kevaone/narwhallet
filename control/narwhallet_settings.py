from typing import List


class MNarwhalletSettings():
    def __init__(self):
        self._sync: dict = None
        self._electrumx_auto_connect: bool = None
        self._primary_peer: int = None
        self._electrumx_peers: List[list] = None
        self._primary_ipfs_gateway: int = None
        self._ipfs_gateways: List[list] = None
        self._data_feeds: dict = None
        self._show_change: bool = False

    @property
    def sync(self) -> dict:
        return self._sync

    @property
    def electrumx_auto_connect(self) -> bool:
        return self._electrumx_auto_connect

    @property
    def primary_peer(self) -> int:
        return self._primary_peer

    @property
    def electrumx_peers(self) -> List[list]:
        return self._electrumx_peers

    @property
    def primary_ipfs_gateway(self) -> int:
        return self._primary_ipfs_gateway

    @property
    def ipfs_gateways(self) -> List[list]:
        return self._ipfs_gateways

    @property
    def data_feeds(self) -> dict:
        return self._data_feeds

    @property
    def show_change(self) -> bool:
        return self._show_change

    def set_sync(self, sync: dict) -> None:
        self._sync = sync

    def set_sync_by_name(self, name: str, sync: bool) -> None:
        self._sync[name] = sync

    def set_electrumx_auto_connect(self, auto_connect: bool) -> None:
        self._electrumx_auto_connect = auto_connect

    def set_electrumx_peers(self, peers: List[list]) -> None:
        self._electrumx_peers = peers

    def set_primary_peer(self, peer: int) -> None:
        self._primary_peer = peer

    def add_electrumx_peer(self, peer: list) -> None:
        self._electrumx_peers.append(peer)

    def set_primary_ipfs_gateway(self, gateway: int) -> None:
        self._primary_ipfs_gateway = gateway

    def set_ipfs_gateways(self, gateways: List[list]) -> None:
        self._ipfs_gateways = gateways

    def add_ipfs_gateway(self, gateway: list) -> None:
        self._ipfs_gateways.append(gateway)

    def set_data_feeds(self, datafeeds: dict) -> None:
        self._data_feeds = datafeeds

    def set_data_feeds_by_name(self, name: str, datafeeds: str) -> None:
        self._data_feeds[name] = datafeeds

    def set_show_change(self, show_change: bool) -> None:
        self._show_change = show_change

    def from_dict(self, _d: dict) -> None:
        self.set_sync(_d['sync'])
        self.set_electrumx_auto_connect(_d['electrumx_auto_connect'])
        # TEMP Check to prevent error, remove after participients have update
        if 'primary_peer' in _d:
            self.set_primary_peer(_d['primary_peer'])
        else:
            self.set_primary_peer(0)
        self.set_electrumx_peers(_d['electrumx_peers'])
        if not isinstance(_d['primary_ipfs_gateway'], int):
            _d['primary_ipfs_gateway'] = 0
        self.set_primary_ipfs_gateway(_d['primary_ipfs_gateway'])
        self.set_ipfs_gateways(_d['ipfs_gateways'])
        self.set_data_feeds(_d['data_feeds'])
        if 'show_change' in _d:
            self.set_show_change(_d['show_change'])

    def to_dict(self) -> dict:
        _d = {}
        _d['sync'] = self.sync
        _d['electrumx_auto_connect'] = self.electrumx_auto_connect
        _d['primary_peer'] = self.primary_peer
        _d['electrumx_peers'] = self.electrumx_peers
        _d['primary_ipfs_gateway'] = self.primary_ipfs_gateway
        _d['ipfs_gateways'] = self.ipfs_gateways
        _d['data_feeds'] = self.data_feeds

        return _d
