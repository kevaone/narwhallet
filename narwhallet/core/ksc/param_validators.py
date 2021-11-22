from enum import Enum
from narwhallet.core.kcl.bip_utils.base58 import Base58Decoder, Base58Encoder
from narwhallet.core.ksc.utils import Ut


class keva_const(Enum):
    KEVA_NS_BUF = b'\x01_KEVA_NS_'
    KEVA_OP_NAMESPACE = 0xd0
    KEVA_OP_PUT = 0xd1
    KEVA_OP_DELETE = 0xd2


class ParamValidators():
    @staticmethod
    def empty_buffer(buffer: bytes) -> bytes:
        if buffer != b'':
            raise Exception('buffer not empty')

        return Ut.to_cuint(len(buffer)) + buffer

    @staticmethod
    def public_key_hash(address: str) -> bytes:
        _pkh = Ut.hash160(Ut.hex_to_bytes(address))
        return Ut.to_cuint(len(_pkh)) + _pkh

    @staticmethod
    def public_key(pk: str) -> bytes:
        _pk = Ut.hex_to_bytes(pk)
        return Ut.to_cuint(len(_pk)) + _pk

    @staticmethod
    def namespace_id(nsid: str) -> bytes:
        _id = Ut.hex_to_bytes(nsid)
        return Ut.to_cuint(len(_id)) + _id

    @staticmethod
    def display_name(name: str) -> bytes:
        try:
            _name = bytes([ord(name)])
        except Exception:
            _name = name.encode()
        return Ut.to_cuint(len(_name)) + _name

    @staticmethod
    def key_value(value: str or bytes) -> bytes:
        if isinstance(value, bytes) is False:
            try:
                _value = bytes([ord(value)])
            except Exception:
                _value = value.encode()
        else:
            _value = value
        return Ut.encode_pushdata(_value)

    @staticmethod
    def base58Checkhash(address: str) -> bytes:
        try:
            _address_hash = Base58Decoder.CheckDecode(address)[1:]
            _address_hash = Ut.to_cuint(len(_address_hash)) + _address_hash

        except Exception:
            return Exception('supplied address failed base58 decode check')

        return _address_hash

    @staticmethod
    def rootNamespaceSciptHash(namespace: str):
        try:
            _namespace = Base58Decoder.CheckDecode(namespace)
            _namespace = _namespace + keva_const.KEVA_NS_BUF.value
            _namespace = Ut.to_cuint(len(_namespace)) + _namespace
        except Exception:
            try:
                _namespace = Ut.hex_to_bytes(namespace)
                _ = Base58Encoder.CheckEncode(_namespace)
                _namespace = _namespace + keva_const.KEVA_NS_BUF.value
                _namespace = Ut.to_cuint(len(_namespace)) + _namespace
            except Exception:
                return Exception('supplied namespace invailid')

        return _namespace

    @staticmethod
    def namespaceSciptHash(namespace: str):
        try:
            _namespace = Base58Decoder.CheckDecode(namespace)
            _namespace = Ut.to_cuint(len(_namespace)) + _namespace
        except Exception:
            try:
                _namespace = Ut.hex_to_bytes(namespace)
                _ = Base58Encoder.CheckEncode(_namespace)
                _namespace = Ut.to_cuint(len(_namespace)) + _namespace
            except Exception:
                return Exception('supplied namespace invailid')

        return _namespace

    @staticmethod
    def namespaceKeySciptHash(nskey: list):
        if isinstance(nskey[1], str):
            nskey[1] = nskey[1].encode()

        try:
            _ns_key = Base58Decoder.CheckDecode(nskey[0])
            _ns_key = _ns_key + nskey[1]
            _ns_key = Ut.to_cuint(len(_ns_key)) + _ns_key
        except Exception:
            try:
                _ns_key = Ut.hex_to_bytes(nskey[0])
                _ = Base58Encoder.CheckEncode(_ns_key)
                _ns_key = _ns_key + nskey[1]
                _ns_key = Ut.to_cuint(len(_ns_key)) + _ns_key
            except Exception:
                return Exception('supplied namespace invailid')

        return _ns_key

    @staticmethod
    def hashtagSciptHash(hashtag: str):
        try:
            _hashtag = hashtag.lower()
            if _hashtag.startswith('#'):
                _hashtag = _hashtag[1:]
            _hashtag = _hashtag.encode()
            _hashtag = Ut.to_cuint(len(_hashtag)) + _hashtag
        except Exception:
            return Exception('hashtag script error')

        return _hashtag
