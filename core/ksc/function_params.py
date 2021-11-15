from enum import Enum
from core.ksc.param_validators import ParamValidators


class Params(Enum):
    def resolve(self, param):
        self.test_input_type(param)
        _param = self.value[1](param)
        return _param

    def test_input_type(self, param):
        if type(param) not in self.value[0]:
            raise Exception('invalid input type', param,
                            type(param), self.value[0])

    def describe(self) -> dict:
        _d = {
            'parm': self.name,
            'type': self.value[0],
            'name': self.value[1]
        }
        return _d

    BadScript = ()
    namespaceToHex = ([str], ParamValidators.namespaceSciptHash,
                      'KVA Namespace in Hex')
    rootNamespace = ([str], ParamValidators.rootNamespaceSciptHash,
                     'KVA NamespaceId')
    namespace = ([str], ParamValidators.namespaceSciptHash,
                 'KVA NamespaceId')
    namespaceKey = ([list], ParamValidators.namespaceKeySciptHash,
                    'KVA NamespaceId')
    publicKeyHash = ([str], ParamValidators.public_key_hash,
                     'Public Key hash')
    publicKey = ([str], ParamValidators.public_key,
                 'Public Key')
    namespaceId = ([str], ParamValidators.namespace_id,
                   'KVA NamespaceId')
    displayName = ([str], ParamValidators.display_name,
                   'KVA Displayname')
    hashtag = ([bytes, str], 'KVA Hashtag', 'utf-8', 'toLower')
    Base58Check_address_hash = ([bytes, str], ParamValidators.base58Checkhash,
                                'Base58 Check Addr Hash')
    keyBuf = ([str, bytes], ParamValidators.key_value,
              'KVA Key Buffer')
    valueBuf = ([str, bytes], ParamValidators.key_value,
                'KVA Value Buffer')
    eBuf = ([bytes], ParamValidators.empty_buffer,
            'Empty Buffer')
    tBuf = ([bytes], 'Total Buffer')
