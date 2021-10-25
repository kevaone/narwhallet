from typing import List
from core.kcl.models.transaction import MTransaction
from core.kcl.models.transaction_input import MTransactionInput
from core.kcl.models.transaction_output import MTransactionOutput
from core.kcl.models.script_sig import MScriptSig
from core.kcl.models.builder.sighash import SIGHASH_TYPE
from core.ksc import Scripts
from core.kcl.bip_utils.utils import CryptoUtils, ConvUtils


class MTransactionBuilder(MTransaction):
    def __init__(self):
        super().__init__()

        self._version: bytes = ConvUtils.IntegerToBytes(2, 4, 'little')
        self._segwit: bytes = ConvUtils.HexStringToBytes('0001')

        self._fee: int = 0
        self._target_value: int = 0
        self._inputs_to_spend: List[MTransactionInput] = []
        self._input_signatures = []

    @staticmethod
    def sort(item):
        return int(item['value'])

    @property
    def fee(self) -> int:
        return self._fee

    def set_fee(self, fee: int):
        self._fee = fee

    def get_current_values(self):
        _i = 0
        _o = 0
        _f = 0

        for vi in self.vin:
            _i += vi._tb_value

        for vo in self.vout:
            _o += vo.value

        _f = _i - _o
        return _i, _o, _f

    def add_output(self, value: int, address: str) -> str:
        _vout = MTransactionOutput()
        try:
            _sh = Scripts.P2SHAddressScriptHash.compile([address], True)
            _vout.set_value(value)
            _vout.scriptPubKey.set_hex(_sh)
            self.add_vout(_vout)
        except Exception as Ex:
            print('ex', Ex)
            _sh = None
        return _sh

    def add_input(self, value: int, address: str, txid: str, vout_index: int):
        _vin = MTransactionInput()
        _ss = MScriptSig()
        _ads = address.split(':')
        _vin._tb_address = int(_ads[0])
        _vin._tb_address_chain = int(_ads[1])
        _vin._tb_value = value
        _vin.set_sequence('ffffffff')
        _vin.set_txid(txid)
        _vin.set_vout(vout_index)
        _vin.set_scriptSig = _ss

        self.add_vin(_vin)

    def select_inputs(self):
        self._inputs_to_spend.sort(reverse=False, key=self.sort)

        for tx in self._inputs_to_spend:
            iv, ov, fv = self.get_current_values()
            # HACK Fix this
            if tx['value'] + iv > (ov + 2*(self.fee*248)):
                self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['tx_hash'], tx['tx_pos'])
                break
            else:
                self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['tx_hash'], tx['tx_pos'])
        _cv = self.get_current_values()

        if _cv[2] < 0:
            _return = False
        elif _cv[2] < 2*(self.fee*248):
            # HACK Fix this
            _return = False
        elif len(self.vin) > 25:
            # NOTE Capping number of inputs to 25, eval for good limit
            _return = False
        else:
            _return = True
        return _return

    def hash_prevouts(self, nHashType: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if (nHashType is not SIGHASH_TYPE.ALL_ANYONECANPAY
           or SIGHASH_TYPE.NONE_ANYONECANPAY
           or SIGHASH_TYPE.SINGLE_ANYONECANPAY):
            for inp in self.vin:
                _tx_id = ConvUtils.ReverseBytes(ConvUtils
                                                .HexStringToBytes(inp.txid))
                _hash_cache = _hash_cache + _tx_id + \
                    ConvUtils.IntegerToBytes(inp.vout, 4, 'little')

            _hash_cache = CryptoUtils.Sha256(CryptoUtils.Sha256(_hash_cache))

        return _hash_cache

    def hash_seqs(self, nHashType: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if nHashType == SIGHASH_TYPE.ALL:
            for inp in self.vin:
                _hash_cache = _hash_cache + \
                    ConvUtils.HexStringToBytes(inp.sequence)
            _hash_cache = CryptoUtils.Sha256(CryptoUtils.Sha256(_hash_cache))

        return _hash_cache

    def hash_outputs(self, nHashType: SIGHASH_TYPE, idx: int = None) -> bytes:
        _hash_cache = b''
        if nHashType is not SIGHASH_TYPE.NONE or SIGHASH_TYPE.SINGLE:
            for output in self.vout:
                _out_value = ConvUtils.IntegerToBytes(output.value,
                                                      8, 'little')
                _script = ConvUtils.HexStringToBytes(output.scriptPubKey.hex)
                _hash_cache = _hash_cache + _out_value + \
                    bytes([len(_script)]) + _script

            _hash_cache = CryptoUtils.Sha256(CryptoUtils.Sha256(_hash_cache))
        elif nHashType == SIGHASH_TYPE.SINGLE:
            _hash_cache = self.vout[idx]
            _hash_cache = CryptoUtils.Sha256(CryptoUtils.Sha256(_hash_cache))

        return _hash_cache

    def serialize_tx(self) -> str:
        _lock_time = 0

        _pre = []

        _pre.append(self._version)
        _pre.append(self._segwit)
        _pre.append(bytes([len(self.vin)]))

        for i in range(0, len(self.vin)):
            _tmp_len = 0
            _outpoint = ConvUtils.ReverseBytes(ConvUtils
                                               .HexStringToBytes(
                                                   self.vin[i].txid))
            _outpoint = _outpoint + ConvUtils.IntegerToBytes(self.vin[i].vout,
                                                             4, 'little')
            _pre.append(_outpoint)
            _tmp_len += len(_outpoint)
            _s = ConvUtils.HexStringToBytes(self.vin[i].scriptSig.hex)
            _scriptSig = bytes([len(_s)]) + _s
            _pre.append(bytes([len(_scriptSig)]))
            _tmp_len += len(bytes([len(_scriptSig)]))
            _pre.append(_scriptSig)
            _tmp_len += len(_scriptSig)
            _pre.append(ConvUtils.HexStringToBytes(self.vin[i].sequence))
            _tmp_len += len(ConvUtils.HexStringToBytes(self.vin[i].sequence))

        _pre.append(bytes([len(self.vout)]))

        for i in range(0, len(self.vout)):
            _pre.append(ConvUtils.IntegerToBytes(self.vout[i].value,
                                                 8, 'little'))
            _pre.append(bytes([len(ConvUtils
                                   .HexStringToBytes(
                                       self.vout[i].scriptPubKey.hex))]))
            _pre.append(ConvUtils
                        .HexStringToBytes(self.vout[i].scriptPubKey.hex))

        for i in range(0, len(self._input_signatures)):
            _pre.append(bytes([len(self._input_signatures[i])]))
            for s in self._input_signatures[i]:
                _x = ConvUtils.HexStringToBytes(s)
                _pre.append(bytes([len(_x)]))
                _pre.append(_x)
        _pre.append(ConvUtils.IntegerToBytes(_lock_time, 4, 'little'))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        _fees = (len(_spre), len(_spre)*self.fee), \
            (len(_spre+bytes(10)), len(_spre+bytes(10))*self.fee)

        return _spre, _fees

    def make_preimage(self, i: int, pk: str) -> str:
        _hash_type = SIGHASH_TYPE.ALL
        _lock_time = 0

        _pre = []
        _pre.append(self._version)
        _pre.append(self.hash_prevouts(_hash_type))
        _pre.append(self.hash_seqs(_hash_type))

        _outpoint = ConvUtils.ReverseBytes(ConvUtils
                                           .HexStringToBytes(self.vin[i].txid))
        _outpoint = _outpoint + ConvUtils.IntegerToBytes(self.vin[i].vout,
                                                         4, 'little')
        _pre.append(_outpoint)

        _s3 = Scripts.P2PKHRedeemScript.compile([pk])
        _pre.append(bytes([len(_s3)]) + _s3)

        _pre.append(ConvUtils.IntegerToBytes(self.vin[i]._tb_value,
                                             8, 'little'))
        _pre.append(ConvUtils.HexStringToBytes(self.vin[i].sequence))

        _pre.append(self.hash_outputs(_hash_type))
        _pre.append(ConvUtils.IntegerToBytes(_lock_time, 4, 'little'))
        _pre.append(ConvUtils.IntegerToBytes(_hash_type.value, 4, 'little'))

        _spre = b''
        for p in _pre:
            _spre = _spre + p

        _sighash = ConvUtils.BytesToHexString(CryptoUtils
                                              .Sha256(CryptoUtils
                                                      .Sha256(_spre)))

        return _sighash

    def toDict(self) -> dict:
        return {'fee': self._fee, 'vin': self.toDictList(self.vin),
                'vout': self.toDictList(self.vout), 'txid': self.txid,
                'version': self.version, 'size': self.size,
                'locktime': self.locktime}
