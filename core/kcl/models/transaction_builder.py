import math
from typing import List
from core.kcl.models.transaction import MTransaction
from core.kcl.models.transaction_input import MTransactionInput
from core.kcl.models.transaction_output import MTransactionOutput
from core.kcl.models.script_sig import MScriptSig
from core.kcl.models.builder.sighash import SIGHASH_TYPE
from core.ksc import Scripts
from core.ksc.utils import Ut


class MTransactionBuilder(MTransaction):
    def __init__(self):
        super().__init__()

        self._version: bytes = Ut.int_to_bytes(2, 4, 'little')
        self._segwit: bytes = Ut.hex_to_bytes('0001')

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

    def get_size(self, in_count, out_count):
        _out_size = 0
        for _out in self.vout:
            _out_size += 1 + 8 + len(Ut.hex_to_bytes(_out.scriptPubKey.hex))

        if len(self.vout) + 1 == out_count:
            _out_size += 32

        _base = (64 * in_count) + _out_size + 10
        _size = _base + (107 * in_count) + in_count
        _total_size = _size + 2
        _vsize = math.ceil((_base * 3 + _total_size) / 4)
        # print('in_count', in_count, 'out_count', out_count)
        # print('base', _base, 'size', _size, '_total_size', _total_size, 'vsize', _vsize)
        return _total_size, _vsize

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
        _enough_inputs = False
        _change_flag = False
        for tx in self._inputs_to_spend:
            iv, ov, fv = self.get_current_values()
            # print('iv', iv, 'ov', ov, 'fv', fv)
            _size, _vsize = self.get_size(len(self.vin) + 1, len(self.vout))
            _est_fee = self.fee * _vsize
            # print('est_fee', _est_fee)
            if (tx['value'] + fv) == _est_fee:
                # print('Worlds align, no change')
                self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']), tx['tx_hash'], tx['tx_pos'])
                _enough_inputs = True
                break
            elif (tx['value'] + fv) < _est_fee:
                # print('Need more inputs')
                self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']), tx['tx_hash'], tx['tx_pos'])
            elif (tx['value'] + fv) > (_est_fee + 500000):
                _size, _vsize = self.get_size(len(self.vin) + 1, len(self.vout) + 1)
                _est_fee = self.fee * _vsize
                # print('change test est_fee', _est_fee)
                if (tx['value'] + fv) > (_est_fee + 500000):
                    # print('Need chage')
                    self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']), tx['tx_hash'], tx['tx_pos'])
                    _enough_inputs = True
                    _change_flag = True
                    break
                else:
                    self.add_input(tx['value'], str(tx['a_idx'])+':'+str(tx['ch']), tx['tx_hash'], tx['tx_pos'])
                    # print('Need more inputs, cant do change')

        if _enough_inputs is False:
            _return = False
        elif len(self.vin) > 25:
            # NOTE Capping number of inputs to 25, eval for good limit
            _return = False
        else:
            _return = True

        return _return, _change_flag, _est_fee

    def hash_prevouts(self, nHashType: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if (nHashType is not SIGHASH_TYPE.ALL_ANYONECANPAY
           or SIGHASH_TYPE.NONE_ANYONECANPAY
           or SIGHASH_TYPE.SINGLE_ANYONECANPAY):
            for inp in self.vin:
                _tx_id = Ut.reverse_bytes(Ut.hex_to_bytes(inp.txid))
                _hash_cache = _hash_cache + _tx_id + \
                    Ut.int_to_bytes(inp.vout, 4, 'little')

            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))

        return _hash_cache

    def hash_seqs(self, nHashType: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if nHashType == SIGHASH_TYPE.ALL:
            for inp in self.vin:
                _hash_cache = _hash_cache + \
                    Ut.hex_to_bytes(inp.sequence)
            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))

        return _hash_cache

    def hash_outputs(self, nHashType: SIGHASH_TYPE, idx: int = None) -> bytes:
        _hash_cache = b''
        if nHashType is not SIGHASH_TYPE.NONE or SIGHASH_TYPE.SINGLE:
            for output in self.vout:
                _out_value = Ut.int_to_bytes(output.value, 8, 'little')
                _script = Ut.hex_to_bytes(output.scriptPubKey.hex)

                _hash_cache = _hash_cache + _out_value + \
                    Ut.to_cuint(len(_script)) + _script

            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        elif nHashType == SIGHASH_TYPE.SINGLE:
            _hash_cache = self.vout[idx]
            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))

        return _hash_cache

    def serialize_tx(self) -> str:
        _lock_time = 0

        _pre = []

        _pre.append(self._version)
        _pre.append(self._segwit)
        _pre.append(Ut.to_cuint(len(self.vin)))

        for i in range(0, len(self.vin)):
            _outpoint = Ut.reverse_bytes(Ut.hex_to_bytes(self.vin[i].txid))
            _outpoint = _outpoint + Ut.int_to_bytes(self.vin[i].vout, 4, 'little')
            _pre.append(_outpoint)
            _s = Ut.hex_to_bytes(self.vin[i].scriptSig.hex)
            _scriptSig = Ut.to_cuint(len(_s)) + _s
            _pre.append(Ut.to_cuint(len(_scriptSig)))
            _pre.append(_scriptSig)
            _pre.append(Ut.hex_to_bytes(self.vin[i].sequence))

        _pre.append(Ut.to_cuint(len(self.vout)))

        for i in range(0, len(self.vout)):
            _pre.append(Ut.int_to_bytes(self.vout[i].value, 8, 'little'))

            _pre.append(Ut.to_cuint(len(Ut.hex_to_bytes(self.vout[i].scriptPubKey.hex))))

            _pre.append(Ut.hex_to_bytes(self.vout[i].scriptPubKey.hex))

        for i in range(0, len(self._input_signatures)):
            _pre.append(Ut.to_cuint(len(self._input_signatures[i])))
            for s in self._input_signatures[i]:
                _x = Ut.hex_to_bytes(s)
                _pre.append(Ut.to_cuint(len(_x)))
                _pre.append(_x)
        _pre.append(Ut.int_to_bytes(_lock_time, 4, 'little'))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre

    def make_preimage(self, i: int, pk: str) -> str:
        _hash_type = SIGHASH_TYPE.ALL
        _lock_time = 0

        _pre = []
        _pre.append(self._version)
        _pre.append(self.hash_prevouts(_hash_type))
        _pre.append(self.hash_seqs(_hash_type))

        _outpoint = Ut.reverse_bytes(Ut.hex_to_bytes(self.vin[i].txid))
        _outpoint = _outpoint + Ut.int_to_bytes(self.vin[i].vout, 4, 'little')
        _pre.append(_outpoint)

        _s3 = Scripts.P2PKHRedeemScript.compile([pk])
        _pre.append(Ut.to_cuint(len(_s3)) + _s3)

        _pre.append(Ut.int_to_bytes(self.vin[i]._tb_value, 8, 'little'))
        _pre.append(Ut.hex_to_bytes(self.vin[i].sequence))

        _pre.append(self.hash_outputs(_hash_type))
        _pre.append(Ut.int_to_bytes(_lock_time, 4, 'little'))
        _pre.append(Ut.int_to_bytes(_hash_type.value, 4, 'little'))

        _spre = b''
        for p in _pre:
            _spre = _spre + p

        _sighash = Ut.bytes_to_hex(Ut.sha256(Ut.sha256(_spre)))

        return _sighash

    def toDict(self) -> dict:
        return {'fee': self._fee, 'vin': self.toDictList(self.vin),
                'vout': self.toDictList(self.vout), 'txid': self.txid,
                'version': self.version, 'size': self.size,
                'locktime': self.locktime}
