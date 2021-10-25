import json
from typing import Dict, List
from core.kcl.models.wallet import MWallet
from core.kcl.wallet_utils import _wallet_utils as WalletUtils


class MWallets():
    def __init__(self):
        self._root_path = None
        self._names: Dict[int] = {}
        self._wallets: List[MWallet] = []

    @property
    def root_path(self):
        return self._root_path

    @property
    def wallets(self) -> List[MWallet]:
        return self._wallets

    def set_root_path(self, root_path):
        self._root_path = root_path

    def get_wallet_by_index(self, index: int) -> MWallet:
        return self._wallets[index]

    def get_wallet_by_name(self, name: str) -> MWallet:
        if name in self._names:
            _return = self._wallets[self._names[name]]
        else:
            _return = None
        return _return

    def _fromMWallet(self, wallet: MWallet):
        self._wallets.append(wallet)
        self._names[wallet.name] = len(self._wallets) - 1

    def save_wallet(self, name: str):
        _wallet = self.get_wallet_by_name(name)
        try:
            _dump = json.dumps(_wallet.toDict(), indent=4).encode()
        except Exception:
            _dump = None

        if _dump is not None:
            if _wallet.state_lock == 1 or _wallet.state_lock == 3:
                WalletUtils.save_wallet(_wallet.name, self.root_path, _dump,
                                        _wallet._k)
            else:
                WalletUtils.save_wallet(_wallet.name, self.root_path, _dump)

    def _load_wallet(self, _wm_dat: dict, _wallet: MWallet) -> MWallet:
        _wallet.set_name(_wm_dat['name'])
        _wallet.set_coin(_wm_dat['coin'])
        _wallet.set_bip(_wm_dat['bip'])
        _wallet.set_mnemonic(_wm_dat['mnemonic'])
        _wallet.set_seed(_wm_dat['seed'])
        _wallet.set_extended_prv(_wm_dat['extended_prv'])
        _wallet.set_extended_pub(_wm_dat['extended_pub'])
        _wallet.set_kind(_wm_dat['kind'])
        _wallet.set_balance(_wm_dat['balance'])
        _wallet.set_locked(_wm_dat['locked'])
        _wallet.set_last_updated(_wm_dat['last_updated'])
        if 'state_lock' in _wm_dat:
            _wallet.set_state_lock(_wm_dat['state_lock'])

        for addr in _wm_dat['addresses']:
            _wallet.addresses._fromJson(addr)

        for addr in _wm_dat['change_addresses']:
            _wallet.change_addresses._fromJson(addr)

        if 'change_index' in _wm_dat:
            if _wm_dat['change_index'] is not None:
                _wallet.set_change_index(_wm_dat['change_index'])
            else:
                _wallet.set_change_index(0)
        else:
            _wallet.set_change_index(0)

        if 'account_index' in _wm_dat:
            if _wm_dat['account_index'] is not None:
                _wallet.set_account_index(_wm_dat['account_index'])
            else:
                _wallet.set_account_index(0)
        else:
            _wallet.set_account_index(0)

        while _wallet.addresses.count < _wallet.account_index:
            _wallet.get_address_by_index(_wallet.addresses.count, True, False)

        while _wallet.change_addresses.count < _wallet.change_index:
            _change_count = _wallet.change_addresses.count
            _wallet.get_change_address_by_index(_change_count, True, False)

        return _wallet

    def relock_wallet(self, name: str) -> bool:
        if (self._wallets[self._names[name]].locked is False
           and self._wallets[self._names[name]]._k is not None
           and self._wallets[self._names[name]].updating is False):

            self.load_wallet(name)
            _return = True
        else:
            _return = False
        return _return

    def load_wallet(self, name: str, wallet: MWallet = None):
        if wallet is not None:
            _wallet = wallet
            if _wallet._k is not None:
                _dat = WalletUtils.load_wallet(name, self.root_path,
                                               _wallet._k)
                if _dat != b'InvalidTag':
                    _wm_dat = json.loads(_dat)
                    _wallet = self._load_wallet(_wm_dat, _wallet)
        else:
            _wallet = MWallet()
            _dat = WalletUtils.load_wallet(name, self.root_path)
            if _dat[:4] == b'narw':
                _wallet.set_name(name)
                _wallet.set_locked(True)
                _wallet.set_state_lock(1)
            else:
                _wm_dat = json.loads(_dat)
                _wallet = self._load_wallet(_wm_dat, _wallet)

        if wallet is None:
            if name in self._names:
                self._wallets[self._names[_wallet.name]] = _wallet
            else:
                self._wallets.append(_wallet)
                self._names[_wallet.name] = len(self._wallets) - 1
