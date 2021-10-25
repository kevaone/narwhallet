from enum import Enum
from core.kcl.bip_utils.base58 import Base58Decoder, Base58Encoder
from core.kcl.bip_utils.utils import CryptoUtils, ConvUtils


class keva_const(Enum):
    KEVA_NS_BUF = b'\x01_KEVA_NS_'
    KEVA_OP_NAMESPACE = 0xd0
    KEVA_OP_PUT = 0xd1
    KEVA_OP_DELETE = 0xd2


class ParamValidators():
    def empty_buffer(buffer: bytes) -> bytes:
        if buffer != b'':
            raise Exception('buffer not empty')

        return bytes([len(buffer)]) + buffer

    def public_key_hash(address: str) -> bytes:
        _pkh = CryptoUtils.Hash160(ConvUtils.HexStringToBytes(address))
        return bytes([len(_pkh)]) + _pkh

    def public_key(pk: str) -> bytes:
        _pk = ConvUtils.HexStringToBytes(pk)
        return bytes([len(_pk)]) + _pk

    def namespace_id(nsid: str) -> bytes:
        _id = ConvUtils.HexStringToBytes(nsid)
        return bytes([len(_id)]) + _id

    def display_name(name: str) -> bytes:
        try:
            _name = bytes([ord(name)])
        except Exception:
            _name = name.encode()
        return bytes([len(_name)]) + _name

    def key_value(value: str) -> bytes:
        try:
            _value = bytes([ord(value)])
        except Exception:
            _value = value.encode()
        return bytes([len(_value)]) + _value

    def base58Checkhash(address: str) -> bytes:
        try:
            _address_hash = Base58Decoder.CheckDecode(address)[1:]
            _address_hash = bytes([len(_address_hash)]) + _address_hash

        except Exception:
            raise Exception('supplied address failed base58 decode check')

        return _address_hash

    def rootNamespaceSciptHash(namespace: str):
        try:
            _namespace = Base58Decoder.CheckDecode(namespace)
            _namespace = _namespace + keva_const.KEVA_NS_BUF.value
            _namespace = bytes([len(_namespace)]) + _namespace
        except Exception:
            try:
                _namespace = ConvUtils.HexStringToBytes(namespace)
                _ = Base58Encoder.CheckEncode(_namespace)
                _namespace = _namespace + keva_const.KEVA_NS_BUF.value
                _namespace = bytes([len(_namespace)]) + _namespace
            except Exception:
                raise Exception('supplied namespace invailid')

        return _namespace

    def namespaceSciptHash(namespace: str):
        try:
            _namespace = Base58Decoder.CheckDecode(namespace)
            _namespace = bytes([len(_namespace)]) + _namespace
        except Exception:
            try:
                _namespace = ConvUtils.HexStringToBytes(namespace)
                _ = Base58Encoder.CheckEncode(_namespace)
                _namespace = bytes([len(_namespace)]) + _namespace
            except Exception:
                raise Exception('supplied namespace invailid')

        return _namespace

    def namespaceKeySciptHash(nskey: list):
        if isinstance(nskey[1], str):
            nskey[1] = nskey[1].encode()

        try:
            _namespace_key = Base58Decoder.CheckDecode(nskey[0])
            _namespace_key = _namespace_key + nskey[1]
            _namespace_key = bytes([len(_namespace_key)]) + _namespace_key
        except Exception:
            try:
                _namespace_key = ConvUtils.HexStringToBytes(nskey[0])
                _ = Base58Encoder.CheckEncode(_namespace_key)
                _namespace_key = _namespace_key + nskey[1]
                _namespace_key = bytes([len(_namespace_key)]) + _namespace_key
            except Exception:
                raise Exception('supplied namespace invailid')

        return _namespace_key

    def hashtagSciptHash(hashtag: str):
        try:
            _hashtag = hashtag.lower()
            if _hashtag.startswith('#'):
                _hashtag = _hashtag[1:]
            _hashtag = _hashtag.encode()
            _hashtag = bytes([len(_hashtag)]) + _hashtag
        except Exception:
            raise Exception('hashtag script error')

        return _hashtag
