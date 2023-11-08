import json
from typing import Dict, List, Optional
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.kcl.wallet_utils import _wallet_utils as WalletUtils


class MWallets():
    def __init__(self):
        self._root_path = None
        self._names: Dict[str, int] = {}
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

    def get_wallet_by_name(self, name: str) -> Optional[MWallet]:
        if name in self._names:
            _return = self._wallets[self._names[name]]
        else:
            _return = None
        return _return

    def from_mwallet(self, wallet: MWallet):
        self._wallets.append(wallet)
        self._names[wallet.name] = len(self._wallets) - 1

    def save_wallet(self, name: str):
        _error = False
        _wallet = self.get_wallet_by_name(name)
        try:
            if _wallet is not None:
                _dump = json.dumps(_wallet.to_dict(), indent=4).encode()
        except Exception:
            _error = True

        if _error is not True:
            if _wallet is not None:
                if _wallet.state_lock in (1, 3):
                    WalletUtils.save_wallet(_wallet.name, self.root_path,
                                            _dump, _wallet.k)
                else:
                    WalletUtils.save_wallet(_wallet.name, self.root_path,
                                            _dump)

    def _load_wallet(self, _wm_dat: dict, _wallet: MWallet) -> MWallet:
        _wallet.set_name(_wm_dat['name'])
        _wallet.set_coin(_wm_dat['coin'])
        _wallet.set_bip(_wm_dat['bip'])
        _wallet.set_mnemonic(_wm_dat['mnemonic'])
        _wallet.set_seed(_wm_dat['seed'])
        _wallet.set_extended_prv(_wm_dat['extended_prv'])
        _wallet.set_extended_pub(_wm_dat['extended_pub'])
        _wallet.set_kind(_wm_dat['kind'])
        if 'bid_balance' in _wm_dat:
            _wallet.set_bid_balance(_wm_dat['bid_balance'])
        _wallet.set_locked(_wm_dat['locked'])
        _wallet.set_last_updated(_wm_dat['last_updated'])
        if 'last_updated_block' in _wm_dat:
            _wallet.set_last_updated_block(_wm_dat['last_updated_block'])
        if 'state_lock' in _wm_dat:
            _wallet.set_state_lock(_wm_dat['state_lock'])

        for addr in _wm_dat['addresses']:
            _wallet.addresses.from_json(addr)

        for addr in _wm_dat['change_addresses']:
            _wallet.change_addresses.from_json(addr)

        if 'change_index' in _wm_dat:
            if _wm_dat['change_index'] != -1:
                _wallet.set_change_index(_wm_dat['change_index'])
            else:
                _wallet.set_change_index(0)
        else:
            _wallet.set_change_index(0)

        if 'account_index' in _wm_dat:
            if _wm_dat['account_index'] != -1:
                _wallet.set_account_index(_wm_dat['account_index'])
            else:
                _wallet.set_account_index(0)
        else:
            _wallet.set_account_index(0)

        self._fill_address_indexes(_wallet)

        return _wallet

    def _fill_address_indexes(self, wallet: MWallet):
        while wallet.addresses.count < wallet.account_index:
            wallet.get_address_by_index(wallet.addresses.count, True, False)

        while wallet.change_addresses.count < wallet.change_index:
            _change_count = wallet.change_addresses.count
            wallet.get_change_address_by_index(_change_count, True, False)

    def relock_wallet(self, name: str) -> bool:
        if (self._wallets[self._names[name]].locked is False
           and self._wallets[self._names[name]].k != b''
           and self._wallets[self._names[name]].updating is False):

            self.load_wallet(name)
            _return = True
        else:
            _return = False
        return _return

    def load_wallet(self, name: str, wallet: Optional[MWallet] = None):
        if wallet is not None:
            _wallet = wallet
            if _wallet.k != b'':
                _dat = WalletUtils.load_wallet(name, self.root_path,
                                               _wallet.k)
                if _dat != b'InvalidTag':
                    _wm_dat = json.loads(_dat)
                    _wallet = self._load_wallet(_wm_dat, _wallet)
                else:
                    raise Exception('InvalidTag')
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
