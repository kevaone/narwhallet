from enum import Enum

from core.ksc.utils import Ut
from core.ksc.op_codes import OpCodes as _o
from core.ksc.function_params import Params as _p


class _factory(Enum):
    def compile(self, parms: list, toHex: bool = False):
        _script = []
        _parm_indexes = [i for i, v in enumerate(self.value) if isinstance(v, _p)]

        if len(_parm_indexes) != len(parms):
            raise Exception('supplied parm count mismatch')

        q = 0
        for i in range(0, len(self.value)):
            if isinstance(self.value[i], _p):
                # NOTE Assumes length added during parm validation
                _script.append(self.value[i].resolve(parms[q]))
                q += 1
            else:
                _script.append(self.value[i].get())

        _scri = b''.join([v for i, v in enumerate(_script)])

        if toHex is True:
            _scri = Ut.bytes_to_hex(_scri)

        return _scri

    def compileToScriptHash(self, params: list, toHex: bool):
        _script = self.compile(params, False)
        _script = Ut.sha256(_script)
        _script = Ut.reverse_bytes(_script)
        if toHex is True:
            _script = Ut.bytes_to_hex(_script)
        return _script

    def describe_types(self) -> list:
        _types = [type(v) for i, v in enumerate(self.value)]
        return _types

    def describe_names(self) -> list:
        _names = [v.name for i, v in enumerate(self.value)]
        return _names

    def describe_raw_values(self) -> list:
        _values = [v.value for i, v in enumerate(self.value)]
        return _values


class Scripts(_factory):
    KevaKeyValueUpdate = [_o.OP_KEVA_PUT, _p.namespaceToHex, _p.keyBuf,
                          _p.valueBuf, _o.OP_2DROP, _o.OP_DROP, _o.OP_HASH160,
                          _p.Base58Check_address_hash, _o.OP_EQUAL]
    KevaKeyValueDelete = [_o.OP_KEVA_DELETE, _p.namespaceToHex, _p.keyBuf,
                          _o.OP_2DROP, _o.OP_HASH160,
                          _p.Base58Check_address_hash, _o.OP_EQUAL]
    KevaNamespaceCreation = [_o.OP_KEVA_NAMESPACE, _p.namespaceId,
                             _p.displayName, _o.OP_2DROP, _o.OP_HASH160,
                             _p.Base58Check_address_hash, _o.OP_EQUAL]
    KevaHashtagScriptHash = [_o.OP_KEVA_PUT, _p.hashtag, _p.eBuf,
                             _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]

    KevaRootNamespaceScriptHash = [_o.OP_KEVA_PUT, _p.rootNamespace, _p.eBuf,
                                   _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
    KevaNamespaceScriptHash = [_o.OP_KEVA_PUT, _p.namespace, _p.eBuf,
                               _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]
    KevaNamespaceKeyScriptHash = [_o.OP_KEVA_PUT, _p.namespaceKey, _p.eBuf,
                                  _o.OP_2DROP, _o.OP_DROP, _o.OP_RETURN]

    P2SHAddressScriptHash = [_o.OP_HASH160, _p.Base58Check_address_hash,
                             _o.OP_EQUAL]
    P2PKHRedeemScript = [_o.OP_DUP, _o.OP_HASH160, _p.publicKeyHash,
                         _o.OP_EQUALVERIFY, _o.OP_CHECKSIG]
    P2WPKHScriptSig = [_o.OP_0, _p.publicKeyHash]
