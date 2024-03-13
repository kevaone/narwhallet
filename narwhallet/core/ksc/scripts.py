from enum import Enum
from io import BytesIO
from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Encoder
from narwhallet.core.kcl.bip_utils.conf.bip49_coin_conf import Bip49KevacoinMainNet
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.ksc.op_codes import OpCodes as _o
from narwhallet.core.ksc.param_validators import ParamValidators as Param


class _factory(Enum):
    @staticmethod
    def compile(parms: list, to_hex: bool = False):
        _script = []

        for _, i in enumerate(parms):
            if isinstance(i, _o):
                _script.append(i.get())
            else:
                # NOTE Assumes length added during parm validation
                _script.append(i)

        _scri = b''.join([v for _, v in enumerate(_script)])

        if to_hex is True:
            return Ut.bytes_to_hex(_scri)

        return _scri

    @staticmethod
    def decompile(script: str):
        _script = BytesIO(Ut.hex_to_bytes(script))
        _script_len = len(_script.getbuffer())
        _read = 0
        _decoded_script = []

        while _read < _script_len:
            _c, _s = Ut.read_csuint(_script)
            _read += _s

            if _c >= 81 and _c <= 96:
                _decoded_script.append(_o.OpNumber(_o(_c)))
            elif _c >= 1 and _c <= 78:
                _decoded_script.append(Ut.bytes_to_hex(_script.read(_c)))
                _read += _c
            else:
                _decoded_script.append(_o(_c).name)

        return _decoded_script

    @staticmethod
    def compileToScriptHash(params: list, to_hex: bool):
        _script = _factory.compile(params, False)
        _script = Ut.sha256(_script)
        _script = Ut.reverse_bytes(_script)
        if to_hex is True:
            _script = Ut.bytes_to_hex(_script)
        return _script


class Scripts(_factory):
    @staticmethod
    def KevaKeyValueUpdate(namespace, key, value, address):
        _script = [_o.OP_KEVA_PUT, Param.namespaceSciptHash(namespace),
                   Param.key_value(key), Param.key_value(value),
                   _o.OP_2DROP, _o.OP_DROP, _o.OP_HASH160,
                   Param.base58Checkhash(address), _o.OP_EQUAL]
        return _script

    @staticmethod
    def KevaKeyValueDelete(namespace, key, address):
        _script = [_o.OP_KEVA_DELETE, Param.namespaceSciptHash(namespace),
                   Param.key_value(key), _o.OP_2DROP, _o.OP_HASH160,
                   Param.base58Checkhash(address), _o.OP_EQUAL]
        return _script

    @staticmethod
    def KevaNamespaceCreation(namespace, name, address):
        _script = [_o.OP_KEVA_NAMESPACE, Param.namespace_id(namespace),
                   Param.display_name(name), _o.OP_2DROP, _o.OP_HASH160,
                   Param.base58Checkhash(address), _o.OP_EQUAL]
        return _script

    @staticmethod
    def KevaHashtagScriptHash(hashtag, ebuf):
        _script = [_o.OP_KEVA_PUT, Param.hashtagSciptHash(hashtag),
                   Param.empty_buffer(ebuf),
                   _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
        return _script

    @staticmethod
    def KevaRootNamespaceScriptHash(namespace, ebuf):
        _script = [_o.OP_KEVA_PUT,
                   Param.rootNamespaceSciptHash(namespace),
                   Param.empty_buffer(ebuf),
                   _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
        return _script

    @staticmethod
    def KevaNamespaceScriptHash(namespace, ebuf):
        _script = [_o.OP_KEVA_PUT, Param.namespaceSciptHash(namespace),
                   Param.empty_buffer(ebuf),
                   _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
        return _script

    @staticmethod
    def KevaNamespaceKeyScriptHash(namespace_key_script, ebuf):
        _script = [_o.OP_KEVA_PUT,
                   Param.namespaceKeySciptHash(namespace_key_script),
                   Param.empty_buffer(ebuf),
                   _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
        return _script

    @staticmethod
    def AddressScriptHash(address: str):
        if address.startswith('V'):
            _script = Scripts.P2SHAddressScriptHash(address)
        else:
            _script = Scripts.P2PKHAddressScriptHash(address)
        return _script

    @staticmethod
    def P2SHAddressScriptHash(address):
        _script = [_o.OP_HASH160, Param.base58Checkhash(address),
                   _o.OP_EQUAL]
        return _script

    @staticmethod
    def P2SHMultisigScriptHash(required_sigs, public_keys):
        if required_sigs > len(public_keys):
            raise Exception('supplied public keys less than required signatres')

        if required_sigs <= 0:
            raise Exception('supplied required signatres must be greater than 0')

        _req_sigs = _o.NumberOp(required_sigs)
        _count_pub_keys = _o.NumberOp(len(public_keys))
        _pub_keys = b''
        for _pub in public_keys:
            _pub_keys = _pub_keys + Param.public_key(_pub)

        _script_multisig = [_req_sigs, _pub_keys, _count_pub_keys, _o.OP_CHECKMULTISIG]
        _witness_script = Scripts.compile(_script_multisig, True)
        _redeem_script = Scripts.compile(Scripts.P2WSHScriptSig(_witness_script))
        _hashed_redeem_script = Ut.hash160(_redeem_script)
        _address = Base58Encoder.CheckEncode(Bip49KevacoinMainNet.AddrConfKey('net_ver') + _hashed_redeem_script)
        _script = Scripts.P2SHAddressScriptHash(_address)

        return _script, _witness_script, _address

    @staticmethod
    def P2PKHAddressScriptHash(address):
        _script = [_o.OP_DUP, _o.OP_HASH160, Param.base58Checkhash(address),
                   _o.OP_EQUALVERIFY, _o.OP_CHECKSIG]
        return _script

    @staticmethod
    def P2PKHRedeemScript(address):
        _script = [_o.OP_DUP, _o.OP_HASH160, Param.public_key_hash(address),
                   _o.OP_EQUALVERIFY, _o.OP_CHECKSIG]
        return _script

    @staticmethod
    def P2WPKHScriptSig(address):
        _script = [_o.OP_0, Param.public_key_hash(address)]
        return _script

    @staticmethod
    def P2WSHScriptSig(script):
        _script = [_o.OP_0, Param.script_hash(script)]
        return _script
