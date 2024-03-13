import binascii
from typing import Union
import ecdsa
from ecdsa import util as ecdsautil
from hashlib import sha256
from narwhallet.core.kcl.bip_utils import (Bip39MnemonicGenerator,
                                           Bip39WordsNum,
                                           Bip39MnemonicValidator,
                                           Bip39SeedGenerator,
                                           Bip32Secp256k1, Bip44Changes,
                                           Bip44Coins, Bip44, Bip49)
from narwhallet.core.kcl.bip_utils.bip39.bip39_mnemonic import Bip39Languages
from narwhallet.core.kcl.bip_utils.conf import Bip49KevacoinMainNet
from narwhallet.core.kcl.bip_utils.addr.P2SH_addr import P2SHAddr
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.file_utils.io import WalletLoader


class _wallet_utils():
    @staticmethod
    def save_wallet(name: str, path: str, data, k=None):
        WalletLoader(path, name).save(data, k)

    @staticmethod
    def load_wallet(name: str, path: str, k=None):
        _data = WalletLoader(path, name).load(k)
        return _data

    @staticmethod
    def sign_message(pk: bytes, message) -> str:
        sk = ecdsa.SigningKey.from_string(pk, ecdsa.SECP256k1, sha256)
        vk = sk.get_verifying_key()

        if not isinstance(message, bytes):
            try:
                message = Ut.hex_to_bytes(message)
            except Exception:
                if isinstance(message, str):
                    message = message.encode()

        sig = sk.sign_digest_deterministic(message, None,
                                           ecdsautil.sigencode_der_canonize)
        vsig = vk.verify_digest(sig, message, ecdsautil.sigdecode_der)

        if vsig is False:
            return 'Validation Error!'
        sig = Ut.bytes_to_hex(sig)
        return sig

    @staticmethod
    def verify_message(sig: str, pk: str, message):
        try:
            _pk = Ut.hex_to_bytes(pk)
            vk = ecdsa.VerifyingKey.from_string(_pk, curve=ecdsa.SECP256k1,
                                                hashfunc=sha256)
            _sig = Ut.hex_to_bytes(sig)

            if not isinstance(message, bytes):
                try:
                    message = Ut.hex_to_bytes(message)
                except Exception:
                    if isinstance(message, str):
                        message = message.encode()

            vsig = vk.verify_digest(_sig, message, ecdsautil.sigdecode_der)
            if vsig is True:
                _return = 'Signature verification succeded.'
            else:
                _return = 'Signature verification failed.'
        except ecdsa.keys.BadSignatureError:
            return 'Signature verification failed.'
        except Exception:
            return 'Verification error.'
        return _return

    @staticmethod
    def get_public_key_raw(seed, coin: str, bip: str, index: int, chain: int):
        if bip == 'bip49':
            _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)
            bip49_acc = _master.Purpose().Coin().Account(0)
            if chain == 0:
                bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_INT)
            else:
                bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_EXT)

            bip49_addr = bip49_change.AddressIndex(index)
            _return = bip49_addr.PublicKey().RawCompressed().ToHex()
        elif bip == 'bip32':
            bip32_ctx = Bip32Secp256k1.FromExtendedKey(seed)
            if chain == 0:
                _derive_path = '0\'/1\'/' + str(index) + '\''
            else:
                _derive_path = '0\'/0\'/' + str(index) + '\''
            bip32_ctx = bip32_ctx.DerivePath(_derive_path)
            _return = bip32_ctx.PublicKey().RawCompressed().ToHex()
        return _return

    @staticmethod
    def get_next_change_address(seed, coin: str, bip: str, index: int):
        _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)

        bip49_acc = _master.Purpose().Coin().Account(0)
        bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_INT)
        bip49_addr = bip49_change.AddressIndex(index)

        return bip49_addr.PublicKey().ToAddress()

    @staticmethod
    def get_next_account_address(seed, coin: str, bip: str, index: int):
        _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)

        bip49_acc = _master.Purpose().Coin().Account(0)
        bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_EXT)
        bip49_addr = bip49_change.AddressIndex(index)

        return bip49_addr.PublicKey().ToAddress()

    @staticmethod
    def get_account_address_index(seed, coin: str, bip: str, public_key: str):
        _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)

        bip49_acc = _master.Purpose().Coin().Account(0)
        bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_EXT)

        for _index in range(0, 1000):
            bip49_addr = bip49_change.AddressIndex(_index)
            if public_key == bip49_addr.PublicKey().RawCompressed().ToHex():
                return _index
        return -1

    @staticmethod
    def get_account_extended_pub(seed, coin: str, bip: str):
        _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)
        bip49_acc = _master.Purpose().Coin().Account(0)

        return bip49_acc.PublicKey().ToExtended()

    @staticmethod
    def get_account_address_private(seed, coin: str, bip: str,
                                    index: int, chain: int) -> bytes:
        _master = _wallet_utils.generate_master_from_seed(seed, coin, bip)

        bip49_acc = _master.Purpose().Coin().Account(0)
        if chain == 0:
            bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_INT)
        elif chain == 1:
            bip49_change = bip49_acc.Change(Bip44Changes.CHAIN_EXT)
        bip49_addr = bip49_change.AddressIndex(index)

        return bip49_addr.PrivateKey().Raw().ToBytes()

    @staticmethod
    def get_next_change_address_from_pub(extended: str, coin: str, bip: str,
                                         index: int) -> str:
        _master = _wallet_utils.generate_master_from_extended(extended,
                                                              coin, bip)
        _master = _master.Change(Bip44Changes.CHAIN_INT).AddressIndex(index)
        return _master.PublicKey().ToAddress()

    @staticmethod
    def get_next_account_address_from_pub(extended: str, coin: str, bip: str,
                                          index: int) -> str:
        _master = _wallet_utils.generate_master_from_extended(extended,
                                                              coin, bip)
        _master = _master.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
        return _master.PublicKey().ToAddress()

    @staticmethod
    def get_account_address_private_from_prv(extended: str, coin: str,
                                             bip: str, index: int) -> str:
        _master = _wallet_utils.generate_master_from_extended(extended,
                                                              coin, bip)
        _master = _master.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)
        return _master.PrivateKey().Raw().ToBytes()

    @staticmethod
    def generate_mnemonic(lang: Bip39Languages):
        _word_num = Bip39WordsNum.WORDS_NUM_24
        return Bip39MnemonicGenerator(lang).FromWordsNumber(_word_num)

    @staticmethod
    def generate_entropy(mnemonic: str):
        return Bip39MnemonicValidator(mnemonic).GetEntropy()

    @staticmethod
    def generate_seed(mnemonic: str, password: str = '',
                      toHex=False) -> Union[str, bytes]:
        if password != '':
            _seed = Bip39SeedGenerator(mnemonic).Generate(password)
        else:
            _seed = Bip39SeedGenerator(mnemonic).Generate()

        if toHex is True:
            return binascii.hexlify(_seed).decode()

        return _seed

    @staticmethod
    def generate_master_from_seed(seed, coin: str, bip: str):
        _seed = binascii.unhexlify(seed.encode())
        if bip == 'bip49':
            _return = Bip49.FromSeed(_seed, Bip44Coins[coin])
        elif bip == 'bip44':
            _return = Bip44.FromSeed(_seed, Bip44Coins[coin])
        return _return

    @staticmethod
    def generate_master_from_extended(extended: str, coin: str, bip: str):
        if bip == 'bip49':
            _return = Bip49.FromExtendedKey(extended, Bip44Coins[coin])
        elif bip == 'bip44':
            _return = Bip44.FromExtendedKey(extended, Bip44Coins[coin])
        return _return

    @staticmethod
    def gen_bip32_address_from_extended(extended_key: str, idx: int):
        _ctx = Bip32Secp256k1.FromExtendedKey(extended_key)
        _derive_path = '0\'/0\'/' + str(idx) + '\''
        _ctx = _ctx.DerivePath(_derive_path)
        cc = P2SHAddr.EncodeKey(_ctx.PublicKey().RawCompressed().ToBytes(),
                                Bip49KevacoinMainNet.AddrConfKey('net_ver'))

        return cc

    @staticmethod
    def get_bip32_address_private(extended_key: str, idx: int, chain: int):
        bip32_ctx = Bip32Secp256k1.FromExtendedKey(extended_key)
        if chain == 0:
            _derive_path = '0\'/1\'/' + str(idx) + '\''
        else:
            _derive_path = '0\'/0\'/' + str(idx) + '\''
        bip32_ctx = bip32_ctx.DerivePath(_derive_path)
        cc = bip32_ctx.PrivateKey().Raw().ToBytes()

        return cc

    @staticmethod
    def gen_bip32_change_from_extended(extended_key: str, idx: int):
        _ctx = Bip32Secp256k1.FromExtendedKey(extended_key)
        _derive_path = '0\'/1\'/' + str(idx) + '\''
        _ctx = _ctx.DerivePath(_derive_path)
        cc = P2SHAddr.EncodeKey(_ctx.PublicKey().RawCompressed().ToBytes(),
                                Bip49KevacoinMainNet.AddrConfKey('net_ver'))

        return cc
