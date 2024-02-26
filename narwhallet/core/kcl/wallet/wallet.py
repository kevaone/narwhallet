from narwhallet.core.kcl.bip_utils.bip39.bip39_mnemonic import Bip39Languages
from narwhallet.core.kcl.wallet.addresses import MAddresses
from narwhallet.core.kcl.wallet.wallet_kind import EWalletKind
from narwhallet.core.kcl.wallet_utils import _wallet_utils as WalletUtils
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder, Base58Encoder
from narwhallet.core.ksc.utils import Ut


class MWallet():
    def __init__(self):
        self._name: str = ''
        self._state_lock: int = 0
        self._mnemonic: str = ''
        self._seed: str = ''
        self._extended_prv: str = ''
        self._extended_pub: str = ''
        self._i_extended_pub: str = ''
        self._coin: str = ''
        self._bip: str = ''
        self._kind: EWalletKind = EWalletKind.NORMAL
        self._k: bytes = b''
        self._bid_balance: float = 0.0
        self._bid_tx: list = []
        self._locked: bool = False
        self._unlocked: float = 0.0
        self._updating: bool = False
        self._last_updated: float = 0.0
        self._last_updated_block: int = 0
        self._account_index: int = 0
        self._change_index: int = 0
        self._addresses = MAddresses()
        self._change_addresses = MAddresses()
        self._active_bids: list = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def state_lock(self) -> int:
        return self._state_lock

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def seed(self) -> str:
        return self._seed

    @property
    def extended_prv(self) -> str:
        return self._extended_prv

    @property
    def extended_pub(self) -> str:
        return self._extended_pub

    @property
    def coin(self) -> str:
        return self._coin

    @property
    def bip(self) -> str:
        return self._bip

    @property
    def kind(self) -> EWalletKind:
        return self._kind

    @property
    def k(self) -> bytes:
        return self._k

    @property
    def balance(self) -> float:
        _balance = 0.0
        for _a in self.addresses.addresses:
            _balance = _balance + _a.balance

        for _a in self.change_addresses.addresses:
            _balance = _balance + _a.balance
        return _balance

    @property
    def sent(self) -> float:
        _sent = 0.0
        for _a in self.addresses.addresses:
            _sent = _sent + _a.sent

        for _a in self.change_addresses.addresses:
            _sent = _sent + _a.sent
        return _sent

    @property
    def received(self) -> float:
        _received = 0.0
        for _a in self.addresses.addresses:
            _received = _received + _a.received

        for _a in self.change_addresses.addresses:
            _received = _received + _a.received
        return _received

    @property
    def unconfirmed_balance(self) -> tuple:
        _unconfirmed_receive_balance = 0.0
        _unconfirmed_send_balance = 0.0
        for _a in self.addresses.addresses:
            _unconfirmed_receive_balance = _unconfirmed_receive_balance + _a.unconfirmed_receive_balance
            _unconfirmed_send_balance = _unconfirmed_send_balance + _a.unconfirmed_send_balance

        for _a in self.change_addresses.addresses:
            _unconfirmed_receive_balance = _unconfirmed_receive_balance + _a.unconfirmed_receive_balance
            _unconfirmed_send_balance = _unconfirmed_send_balance + _a.unconfirmed_send_balance
        return (_unconfirmed_receive_balance, _unconfirmed_send_balance)

    @property
    def bid_balance(self) -> float:
        return self._bid_balance

    @property
    def bid_tx(self) -> list:
        return self.bid_tx

    @property
    def locked(self) -> bool:
        return self._locked

    @property
    def unlocked(self) -> float:
        return self._unlocked

    @property
    def updating(self) -> bool:
        return self._updating

    @property
    def last_updated(self) -> float:
        return self._last_updated

    @property
    def last_updated_block(self) -> int:
        return self._last_updated_block

    @property
    def addresses(self) -> MAddresses:
        return self._addresses

    @property
    def change_addresses(self) -> MAddresses:
        return self._change_addresses

    @property
    def account_index(self) -> int:
        return self._account_index

    @property
    def change_index(self) -> int:
        return self._change_index

    @property
    def history(self) -> list:
        _history: list = []
        for _a in self.addresses.addresses:
            _history = _history + _a.history

        for _a in self.change_addresses.addresses:
            _history = _history + _a.history
        return _history

    @property
    def unspent_tx(self) -> list:
        _unspent_tx: list = []
        for _a in self.addresses.addresses:
            _unspent_tx = _unspent_tx + _a.unspent_tx

        for _a in self.change_addresses.addresses:
            _unspent_tx = _unspent_tx + _a.unspent_tx
        return _unspent_tx

    @property
    def namespaces(self) -> list:
        _namespaces: list = []
        for _a in self.addresses.addresses:
            _namespaces = _namespaces + _a.namespaces

        for _a in self.change_addresses.addresses:
            _namespaces = _namespaces + _a.namespaces
        return _namespaces

    def set_name(self, name: str) -> None:
        self._name = name

    def set_state_lock(self, state_lock: int) -> None:
        # 0-unlocked, 1-fe, 2-me, 3-fe:me
        self._state_lock = state_lock

    def set_mnemonic(self, mnemonic: str) -> None:
        self._mnemonic = mnemonic

    def set_seed(self, seed: str) -> None:
        self._seed = seed

    def set_extended_prv(self, extended_prv: str):
        self._extended_prv = extended_prv

    def set_extended_pub(self, extended_pub: str, version: str = '0488b21e'):
        if extended_pub != '':
            try:
                _data = Base58Decoder.CheckDecode(extended_pub)
                _data = _data[4:]
                lll = Ut.hex_to_bytes(version)
                _data = lll + _data
                _pub = Base58Encoder.CheckEncode(_data)

                if version == '0488b21e':
                    self._extended_pub = extended_pub
                    self._i_extended_pub = _pub
                else:
                    self._extended_pub = _pub
            except Exception:
                self._extended_pub = ''
        else:
            self._extended_pub = ''

    def set_coin(self, coin: str) -> None:
        self._coin = coin

    def set_bip(self, bip: str) -> None:
        self._bip = bip

    def set_kind(self, kind: int) -> None:
        self._kind = EWalletKind(kind)

    def set_k(self, k: str):
        self._k = Ut.sha256(Ut.reverse_bytes(Ut.sha256(k)))

    def set_bid_tx(self, bid_tx: list) -> None:
        self._bid_tx = bid_tx

    def add_bid_tx(self, bid_tx: list) -> None:
        self._bid_tx.append(bid_tx)

    def set_bid_balance(self, bid_balance: float) -> None:
        self._bid_balance = bid_balance

    def set_locked(self, locked: bool) -> None:
        self._locked = locked

    def set_unlocked(self, unlocked: float) -> None:
        self._unlocked = unlocked

    def set_updating(self, updating: bool) -> None:
        self._updating = updating

    def set_last_updated(self, last_updated: float) -> None:
        self._last_updated = last_updated

    def set_last_updated_block(self, last_updated_block: int) -> None:
        self._last_updated_block = last_updated_block

    def set_account_index(self, account_index: int) -> None:
        self._account_index = account_index

    def set_change_index(self, change_index: int) -> None:
        self._change_index = change_index

    def incriment_account_index(self) -> None:
        self._account_index = self.account_index + 1

    def incriment_change_index(self) -> None:
        self._change_index = self.change_index + 1

    def generate_mnemonic(self, lang: Bip39Languages) -> None:
        if self.seed == '':
            self.set_mnemonic(WalletUtils.generate_mnemonic(lang))
        else:
            raise Exception

    def generate_seed(self, password: str = '') -> None:
        if password != '':
            self.set_kind(2)

        if self.seed == '':
            self.set_seed(WalletUtils.generate_seed(self.mnemonic,
                                                    password, True))
        else:
            raise Exception

    def generate_extended_prv(self):
        pass

    def generate_extended_pub(self):
        if self.bip == 'bip49' and self.kind != EWalletKind.READ_ONLY:
            if self.seed != '':
                _xpub = WalletUtils.get_account_extended_pub(self.seed,
                                                             self.coin,
                                                             self.bip)
                self.set_extended_pub(_xpub, '049d7cb2')

    def get_publickey_raw(self, index: int,  chain: int) -> str:
        if self.bip == 'bip32':
            _pk = WalletUtils.get_public_key_raw(self.extended_prv,
                                                 self.coin, self.bip,
                                                 index, chain)
        elif self.bip == 'bip49':
            _pk = WalletUtils.get_public_key_raw(self.seed, self.coin,
                                                 self.bip, index, chain)

        return _pk

    def get_unused_address(self) -> str:
        if self.bip == 'bip32':
            _a = (WalletUtils
                  .gen_bip32_address_from_extended(self.extended_prv,
                                                   self.account_index))
        elif (self.bip == 'bip49'
              and (self.extended_prv != ''
                   or self._i_extended_pub != '')):
            _a = (WalletUtils
                  .get_next_account_address_from_pub(self._i_extended_pub,
                                                     self.coin, self.bip,
                                                     self.account_index))
        else:
            _a = WalletUtils.get_next_account_address(self.seed, self.coin,
                                                      self.bip,
                                                      self.account_index)
        self.addresses.from_pool(_a)
        self.incriment_account_index()
        return _a

    def get_unused_change_address(self) -> str:
        if self.bip == 'bip32':
            _a = WalletUtils.gen_bip32_change_from_extended(self.extended_prv,
                                                            self._change_index
                                                            )
        elif (self.bip == 'bip49'
              and (self.extended_prv != ''
                   or self._i_extended_pub != '')):
            _a = (WalletUtils
                  .get_next_change_address_from_pub(self._i_extended_pub,
                                                    self.coin, self.bip,
                                                    self._change_index))
        else:
            _a = WalletUtils.get_next_change_address(self.seed, self.coin,
                                                     self.bip,
                                                     self.change_index)
        self.change_addresses.from_pool(_a)
        self.incriment_change_index()
        return _a

    def get_address_by_index(self, index: int,
                             incriment: bool = False,
                             incriment_idx: bool = True) -> str:
        if self.bip == 'bip32':
            _a = (WalletUtils
                  .gen_bip32_address_from_extended(self.extended_prv, index))
        elif (self.bip == 'bip49'
              and (self.extended_prv != ''
                   or self._i_extended_pub != '')):
            _a = (WalletUtils
                  .get_next_account_address_from_pub(self._i_extended_pub,
                                                     self.coin, self.bip,
                                                     index))
        else:
            _a = WalletUtils.get_next_account_address(self.seed, self.coin,
                                                      self.bip, index)

        if incriment:
            self.addresses.from_pool(_a)
            if incriment_idx:
                self.incriment_account_index()
        return _a

    def get_change_address_by_index(self, index: int,
                                    incriment: bool = False,
                                    incriment_idx: bool = True) -> str:
        if self.bip == 'bip32':
            _a = WalletUtils.gen_bip32_change_from_extended(self.extended_prv,
                                                            index)
        elif (self.bip == 'bip49'
              and (self.extended_prv != ''
                   or self._i_extended_pub != '')):
            _a = (WalletUtils
                  .get_next_change_address_from_pub(self._i_extended_pub,
                                                    self.coin, self.bip,
                                                    index))
        else:
            _a = WalletUtils.get_next_change_address(self.seed, self.coin,
                                                     self.bip, index)

        if incriment:
            self.change_addresses.from_pool(_a)
            if incriment_idx:
                self.incriment_change_index()
        return _a

    def get_usxos(self) -> list:
        _usxo = []
        for _a in self.addresses.addresses:
            for _x in _a.unspent_tx:
                _ai = self.addresses.get_address_index_by_name(_a.address)
                _x['a_idx'] = _ai
                _x['a'] = _a.address
                _x['ch'] = 1
                _usxo.append(_x)
        for _a in self.change_addresses.addresses:
            for _x in _a.unspent_tx:
                _ai = (self.change_addresses
                       .get_address_index_by_name(_a.address))
                _x['a_idx'] = _ai
                _x['a'] = _a.address
                _x['ch'] = 0
                _usxo.append(_x)
        return _usxo

    def sign_message(self, address_index: int,
                     message: str, chain: int) -> str:
        if self.bip == 'bip32':
            _a_p = WalletUtils.get_bip32_address_private(self.extended_prv,
                                                         address_index, chain)
        elif self.bip == 'bip49' and self.extended_prv != '':
            _a_p = (WalletUtils
                    .get_account_address_private_from_prv(self.extended_prv,
                                                          self.coin,
                                                          self.bip,
                                                          address_index))
        else:
            _a_p = WalletUtils.get_account_address_private(self.seed,
                                                           self.coin, self.bip,
                                                           address_index,
                                                           chain)

        sig = WalletUtils.sign_message(_a_p, message)

        return sig

    def to_list(self) -> list:
        return [self.name, self.mnemonic, self.seed, self.coin, self.bip,
                self.kind, self.balance, self.locked, self.last_updated,
                self.addresses.to_list(), self.change_addresses.to_list()]

    def to_dict(self) -> dict:
        return {'name': self.name, 'mnemonic': self.mnemonic,
                'seed': self.seed, 'extended_prv': self.extended_prv,
                'extended_pub': self.extended_pub, 'coin': self.coin,
                'bip': self.bip, 'kind': self.kind, 'balance': self.balance,
                'bid_balance': self.bid_balance, 'locked': self.locked,
                'state_lock': self.state_lock,
                'last_updated': self.last_updated,
                'last_updated_block': self.last_updated_block,
                'account_index': self.account_index,
                'change_index': self.change_index,
                'addresses': self.addresses.to_dict_list(),
                'change_addresses': self.change_addresses.to_dict_list()}
