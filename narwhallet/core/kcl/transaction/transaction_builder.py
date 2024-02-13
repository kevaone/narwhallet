import math
from typing import List
from narwhallet.core.kcl.transaction.transaction import MTransaction
from narwhallet.core.kcl.transaction.input import MTransactionInput
from narwhallet.core.kcl.transaction.output import MTransactionOutput
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.utils import Ut

ZHASH = '0000000000000000000000000000000000000000000000000000000000000000'


class MTransactionBuilder(MTransaction):
    def __init__(self):
        super().__init__()

        self._version: bytes = Ut.int_to_bytes(2, 4, 'little')
        self._segwit: bytes = Ut.hex_to_bytes('0001')

        self._fee: int = 0
        self._target_value: int = 0
        self.inputs_to_spend: List[MTransactionInput] = []
        self.input_ref_scripts = []
        self.input_signatures = []
        self.bid_tx: MTransactionBuilder = None

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

        return _total_size, _vsize

    def get_current_values(self):
        _i = 0
        _o = 0
        _f = 0

        for vi in self.vin:
            _i += vi.tb_value

        for vo in self.vout:
            _o += vo.value

        _f = _i - _o
        return _i, _o, _f

    def add_output(self, value: int, address: str) -> str:
        _vout = MTransactionOutput()
        try:
            _sh = Scripts.AddressScriptHash(address)
            _sh = Scripts.compile(_sh, True)
            _vout.set_value(value)
            _vout.scriptPubKey.set_hex(_sh)
            self.add_vout(_vout)
        except Exception as ex:
            # print('ex', ex)
            _sh = None
        return _sh

    def add_input(self, value: int, address: str, txid: str, vout_index: int):
        _vin = MTransactionInput()
        _ads = address.split(':')
        _vin.tb_address = int(_ads[0])
        _vin.tb_address_chain = int(_ads[1])
        _vin.tb_value = value
        _vin.set_sequence('ffffffff')
        _vin.set_txid(txid)
        _vin.set_vout(vout_index)

        self.add_vin(_vin)

    def select_inputs(self):
        _est_fee = 0
        self.inputs_to_spend.sort(reverse=False, key=self.sort)
        _enough_inputs = False
        _change_flag = False
        for tx in self.inputs_to_spend:
            _, _, fv = self.get_current_values()
            _size, _vsize = self.get_size(len(self.vin) + 1, len(self.vout))
            _est_fee = self.fee * _vsize
            # print('est_fee', _est_fee)
            if (tx['value'] + fv) == _est_fee:
                # print('Worlds align, no change')
                self.add_input(tx['value'],
                               str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['txid'], tx['n'])
                _enough_inputs = True
            elif (tx['value'] + fv) < _est_fee:
                # print('Need more inputs')
                self.add_input(tx['value'],
                               str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['txid'], tx['n'])
            elif (tx['value'] + fv) > _est_fee:
                _size, _vsize = (self.get_size(
                    len(self.vin) + 1, len(self.vout) + 1))
                _est_fee = self.fee * _vsize
                # print('change test est_fee', _est_fee)
                if (tx['value'] + fv) > (_est_fee + 500000):
                    # print('Need chage')
                    self.add_input(tx['value'],
                                   str(tx['a_idx'])+':'+str(tx['ch']),
                                   tx['txid'], tx['n'])
                    _enough_inputs = True
                    _change_flag = True
                else:
                    self.add_input(tx['value'],
                                   str(tx['a_idx'])+':'+str(tx['ch']),
                                   tx['txid'], tx['n'])
                    # print('Need more inputs, cant do change')
            if _enough_inputs is True:
                break

        if _enough_inputs is False:
            _return = False
        elif len(self.vin) > 50:
            # NOTE Capping number of inputs to 50, eval for good limit
            _return = False
        else:
            _return = True

        return _return, _change_flag, _est_fee

    def hash_prevouts(self, hash_type: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if (hash_type is not SIGHASH_TYPE.ALL_ANYONECANPAY
           and SIGHASH_TYPE.NONE_ANYONECANPAY
           and SIGHASH_TYPE.SINGLE_ANYONECANPAY):
            for inp in self.vin:
                _tx_id = Ut.reverse_bytes(Ut.hex_to_bytes(inp.txid))
                _hash_cache = _hash_cache + _tx_id + \
                    Ut.int_to_bytes(inp.vout, 4, 'little')

            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        else:
            _hash_cache = Ut.hex_to_bytes(ZHASH)

        return _hash_cache

    def hash_seqs(self, hash_type: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if hash_type == SIGHASH_TYPE.ALL:
            for inp in self.vin:
                _hash_cache = _hash_cache + \
                    Ut.hex_to_bytes(inp.sequence)
            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        else:
            _hash_cache = Ut.hex_to_bytes(ZHASH)

        return _hash_cache

    def hash_outputs(self, hash_type: SIGHASH_TYPE, idx: int = None) -> bytes:
        _hash_cache = b''
        if hash_type is not SIGHASH_TYPE.NONE and SIGHASH_TYPE.SINGLE:
            for output in self.vout:
                _out_value = Ut.int_to_bytes(output.value, 8, 'little')
                _script = Ut.hex_to_bytes(output.scriptPubKey.hex)

                _hash_cache = _hash_cache + _out_value + \
                    Ut.to_cuint(len(_script)) + _script

            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        elif hash_type == SIGHASH_TYPE.SINGLE:
            _hash_cache = self.vout[idx]
            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        else:
            _hash_cache = Ut.hex_to_bytes(ZHASH)

        return _hash_cache

    def serialize_tx(self, for_psbt: bool = False) -> bytes:
        _lock_time = 0

        _pre = []

        _pre.append(self._version)
        if for_psbt is False:
            _pre.append(self._segwit)
        _pre.append(Ut.to_cuint(len(self.vin)))

        for i in self.vin:
            _outpoint = Ut.reverse_bytes(Ut.hex_to_bytes(i.txid))
            _outpoint = _outpoint + Ut.int_to_bytes(i.vout, 4, 'little')
            _pre.append(_outpoint)
            if for_psbt is False:
                _s = Ut.hex_to_bytes(i.scriptSig.hex)
                _script_sig = Ut.to_cuint(len(_s)) + _s
                _pre.append(Ut.to_cuint(len(_script_sig)))
                _pre.append(_script_sig)
            else:
                _pre.append(Ut.to_cuint(0))

            _pre.append(Ut.hex_to_bytes(i.sequence))

        _pre.append(Ut.to_cuint(len(self.vout)))

        for o in self.vout:
            _pre.append(Ut.int_to_bytes(o.value, 8, 'little'))
            _pre.append(Ut.to_cuint(len(Ut.hex_to_bytes(o.scriptPubKey.hex))))
            _pre.append(Ut.hex_to_bytes(o.scriptPubKey.hex))

        for sg in self.input_signatures:
            if for_psbt is True:
                break

            _pre.append(Ut.to_cuint(len(sg)))
            for s in sg:
                _x = Ut.hex_to_bytes(s)
                _pre.append(Ut.to_cuint(len(_x)))
                _pre.append(_x)
        _pre.append(Ut.int_to_bytes(_lock_time, 4, 'little'))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre

    def txb_preimage(self, wallet: MWallet, hash_type: SIGHASH_TYPE,
                     ovr: bool = False):
        if ovr is False:
            self.input_signatures = []

        for c, _vin_idx in enumerate(self.vin):
            if ovr is True and c != len(self.vin) - 1:
                continue
            _npk = _vin_idx.tb_address
            _npkc = _vin_idx.tb_address_chain
            _pk = wallet.get_publickey_raw(_npk, _npkc)
            _sighash = self.make_preimage(c, _pk, hash_type)
            _sig = wallet.sign_message(_npk, _sighash, _npkc)
            _script = Scripts.P2WPKHScriptSig(_pk)
            _script = Scripts.compile(_script, True)
            _vin_idx.scriptSig.set_hex(_script)
            (self.input_signatures.append(
                [_sig+Ut.bytes_to_hex(Ut.to_cuint(hash_type.value)), _pk]))

            _addr = wallet.get_address_by_index(_npk, False)
            _r = Scripts.AddressScriptHash(_addr)
            _r = Scripts.compile(_r, False)
            _ref = Ut.int_to_bytes(_vin_idx.tb_value, 8, 'little')
            _ref = _ref + Ut.to_cuint(len(_r)) + _r
            self.input_ref_scripts.append(_ref)

    def make_preimage(self, i: int, pk: str, hash_type: SIGHASH_TYPE) -> str:
        _hash_type = hash_type
        _lock_time = 0

        _pre = []
        _pre.append(self._version)
        _pre.append(self.hash_prevouts(_hash_type))
        _pre.append(self.hash_seqs(_hash_type))

        _outpoint = Ut.reverse_bytes(Ut.hex_to_bytes(self.vin[i].txid))
        _outpoint = _outpoint + Ut.int_to_bytes(self.vin[i].vout, 4, 'little')
        _pre.append(_outpoint)
        _s3 = Scripts.P2PKHRedeemScript(pk)
        _s3 = Scripts.compile(_s3, False)
        _pre.append(Ut.to_cuint(len(_s3)) + _s3)

        _pre.append(Ut.int_to_bytes(self.vin[i].tb_value, 8, 'little'))
        _pre.append(Ut.hex_to_bytes(self.vin[i].sequence))

        _pre.append(self.hash_outputs(_hash_type))
        _pre.append(Ut.int_to_bytes(_lock_time, 4, 'little'))
        _pre.append(Ut.int_to_bytes(_hash_type.value, 4, 'little'))

        _spre = b''
        for p in _pre:
            _spre = _spre + p

        _sighash = Ut.bytes_to_hex(Ut.sha256(Ut.sha256(_spre)))

        return _sighash

    def to_psbt(self) -> str:
        _pre = []
        _magic = '70736274'
        _seperator = 'ff'
        _pre.append(Ut.hex_to_bytes(_magic))
        _pre.append(Ut.hex_to_bytes(_seperator))

        # _PSBT_GLOBAL_UNSIGNED_TX '00'
        _pre.append(Ut.to_cuint(1))
        _pre.append(Ut.to_cuint(0))
        _tx = self.serialize_tx(True)
        _pre.append(Ut.to_cuint(len(_tx)))
        _pre.append(_tx)

        for c, i in enumerate(self.input_signatures):
            _pre.append(Ut.to_cuint(0))
            # _PSBT_IN_WITNESS_UTXO '01'
            _pre.append(Ut.to_cuint(1))
            _sp = self.input_ref_scripts[c]
            _pre.append(Ut.to_cuint(len(Ut.to_cuint(len(_sp)))))
            _pre.append(Ut.to_cuint(len(_sp)))
            _pre.append(_sp)
            # _PSBT_IN_PARTIAL_SIG '02'
            _x = Ut.to_cuint(2) + Ut.hex_to_bytes(i[1])
            _pre.append(Ut.to_cuint(len(_x)))
            _pre.append(_x)
            _pre.append(Ut.to_cuint(len(Ut.hex_to_bytes(i[0]))))
            _pre.append(Ut.hex_to_bytes(i[0]))
            # _PSBT_IN_SIGHASH_TYPE '03'
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(3))
            _shl = (len(Ut.int_to_bytes(
                    SIGHASH_TYPE.ALL_ANYONECANPAY.value, 4, 'little')))
            _pre.append(Ut.to_cuint(_shl))
            _pre.append(Ut.int_to_bytes(SIGHASH_TYPE.ALL_ANYONECANPAY.value,
                                        4, 'little'))
            # _PSBT_IN_REDEEM_SCRIPT '04'
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(4))
            _s = Ut.hex_to_bytes(self.vin[c].scriptSig.hex)
            _pre.append(Ut.to_cuint(len(_s)) + _s)
        _pre.append(Ut.to_cuint(0))
        for i in self.vout:
            _pre.append(Ut.to_cuint(0))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre

    def to_dict(self) -> dict:
        return {'fee': self._fee, 'vin': self.to_dict_list(self.vin),
                'vout': self.to_dict_list(self.vout), 'txid': self.txid,
                'version': self.version, 'size': self.size,
                'locktime': self.locktime}
