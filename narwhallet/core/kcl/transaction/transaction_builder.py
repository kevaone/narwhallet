from narwhallet.core.kcl.bip_utils.base58.base58 import Base58Encoder
from narwhallet.core.kcl.bip_utils.conf.bip49_coin_conf import Bip49KevacoinMainNet
from narwhallet.core.kcl.transaction.transaction import MTransaction
from narwhallet.core.kcl.transaction.input import MTransactionInput
from narwhallet.core.kcl.transaction.output import MTransactionOutput
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.witness import MTransactionWitness
from narwhallet.core.kcl.wallet.wallet import MWallet
from narwhallet.core.ksc import Scripts
from narwhallet.core.ksc.op_codes import OpCodes
from narwhallet.core.ksc.utils import Ut

ZHASH = '0000000000000000000000000000000000000000000000000000000000000000'


class TransactionBuilderError(Exception):
    pass

class MTransactionBuilder(MTransaction):
    def __init__(self):
        super().__init__()

        self._fee_rate: int = 0
        self._target_value: int = 0
        self.inputs_to_spend: list = []

    @staticmethod
    def sort(item):
        return int(item['value'])

    @property
    def fee_rate(self) -> int:
        # enable ability to control Child Pays For Parent (CPFP) by bumping fee if parents still in mempool
        return self._fee_rate

    def set_fee_rate(self, fee_rate: int) -> None:
        self._fee_rate = fee_rate

    def get_current_values(self):
        _input_value = 0
        _output_value = 0
        _to_fee = 0

        for vi in self.vin:
            _input_value += vi.tb_value

        for vo in self.vout:
            _output_value += Ut.bytes_to_int(vo.amount, 'little')

        _to_fee = _input_value - _output_value
        return _input_value, _output_value, _to_fee

    def add_output(self, value: int, address: str) -> None:
        _vout = MTransactionOutput()
        try:
            _sh = Scripts.AddressScriptHash(address)
            _sh = Scripts.compile(_sh)
            _vout.set_amount(value)
            _vout.set_scriptpubkey(_sh)
            self.add_vout(_vout)
        except Exception as Ex:
            _sh = None
            raise TransactionBuilderError(f'Failed to add transaction output: {Ex}')

    def add_input(self, value: int, address: str, txid: str, vout_index: int):
        _vin = MTransactionInput()
        _ads = address.split(':')
        _vin.tb_address = int(_ads[0])
        _vin.tb_address_chain = int(_ads[1])
        _vin.tb_value = value
        # _vin.set_sequence('ffffffff')
        _vin.set_txid(txid)
        _vin.set_vout(vout_index)

        self.add_vin(_vin)

    def select_inputs(self):
        _est_fee = 0
        self.inputs_to_spend.sort(reverse=False, key=self.sort)
        _enough_inputs = False
        _change_flag = False
        for tx in self.inputs_to_spend:
            _, _, _to_fee = self.get_current_values()
            _size, _vsize = self.calc_size(len(self.vin) + 1, len(self.vout))
            _est_fee = self.fee_rate * _vsize
            # print('est_fee', _est_fee)
            if (tx['value'] + _to_fee) == _est_fee:
                # print('Worlds align, no change')
                self.add_input(tx['value'],
                               str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['txid'], tx['n'])
                _enough_inputs = True
            elif (tx['value'] + _to_fee) < _est_fee:
                # print('Need more inputs')
                self.add_input(tx['value'],
                               str(tx['a_idx'])+':'+str(tx['ch']),
                               tx['txid'], tx['n'])
            elif (tx['value'] + _to_fee) > _est_fee:
                _size, _vsize = (self.calc_size(
                    len(self.vin) + 1, len(self.vout) + 1))
                _est_fee = self.fee_rate * _vsize
                # print('change test est_fee', _est_fee)
                if (tx['value'] + _to_fee) > _est_fee:
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
                _tx_id = Ut.reverse_bytes(inp.txid)
                _hash_cache = _hash_cache + _tx_id + inp.vout

            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        else:
            _hash_cache = Ut.hex_to_bytes(ZHASH)

        return _hash_cache

    def hash_seqs(self, hash_type: SIGHASH_TYPE) -> bytes:
        _hash_cache = b''
        if hash_type == SIGHASH_TYPE.ALL:
            for inp in self.vin:
                _hash_cache = _hash_cache + inp.sequence
            _hash_cache = Ut.sha256(Ut.sha256(_hash_cache))
        else:
            _hash_cache = Ut.hex_to_bytes(ZHASH)

        return _hash_cache

    def hash_outputs(self, hash_type: SIGHASH_TYPE, idx: int = -1) -> bytes:
        _hash_cache = b''
        if hash_type is not SIGHASH_TYPE.NONE and SIGHASH_TYPE.SINGLE:
            for output in self.vout:
                _out_value = output.amount
                _script = output.scriptpubkey.script

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
        _pre: list[bytes] = []

        _pre.append(self.version)
        if for_psbt is False:
            _pre.append(self.marker)
            _pre.append(self.flag)
        _pre.append(Ut.to_cuint(len(self.vin)))

        for _vin in self.vin:
            _outpoint = Ut.reverse_bytes(_vin.txid)
            _outpoint = _outpoint + _vin.vout
            _pre.append(_outpoint)
            if for_psbt is False:
                _s = _vin.scriptsig.script
                _script_sig = Ut.to_cuint(len(_s)) + _s
                _pre.append(Ut.to_cuint(len(_script_sig)))
                _pre.append(_script_sig)
            else:
                _pre.append(Ut.to_cuint(0))

            _pre.append(_vin.sequence)

        _pre.append(Ut.to_cuint(len(self.vout)))

        for _vout in self.vout:
            _pre.append(_vout.amount)
            _pre.append(Ut.to_cuint(len(_vout.scriptpubkey.script)))
            _pre.append(_vout.scriptpubkey.script)

        if for_psbt is False:
            if len(self.witnesses) != len(self.vin):
                raise TransactionBuilderError(f'Failed to serialize transaction output. Witness count does not equal input count.')

            for _witness in self.witnesses:
                _pre.append(Ut.to_cuint(len(_witness.stack)))
                for _stack_item in _witness.stack:
                    _pre.append(Ut.to_cuint(len(_stack_item)))
                    _pre.append(_stack_item)

        _pre.append(self.locktime)

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre

    def txb_preimage(self, wallet: MWallet, hash_type: SIGHASH_TYPE,
                     ovr: bool = False, redeem_script: str | None = None):
        if ovr is False:
            self.set_witnesses([])

        for idx, _vin in enumerate(self.vin):
            if ovr is True and idx != len(self.vin) - 1:
                continue

            input_sigs = {}

            if redeem_script is not None:
                _sighash = self.make_preimage(idx, '', hash_type, redeem_script)
                _public_keys = []

                _decoded_script = Scripts.decompile(redeem_script)
                _pubk = _decoded_script[-2]
                for _p in range(1, _pubk + 1):
                    try:
                        _ = Ut.hex_to_bytes(_decoded_script[_p])
                    except:
                        return

                    if len(_decoded_script[_p]) != 66:
                        return

                    _address_index = wallet.get_account_address_index(_decoded_script[_p])

                    if _address_index != -1:
                        _public_keys.append(_address_index)

                for pk in _public_keys:
                    _sig = wallet.sign_message(pk, _sighash, 0)
                    # input_sigs[pk] = _sig + Ut.bytes_to_hex(Ut.to_cuint(hash_type.value))

                # input_sigs['redeem_script'] = redeem_script

                _script = Scripts.compile(Scripts.P2WSHScriptSig(redeem_script), True)
                _vin.set_scriptsig(_script)

                _hashed_redeem_script = Ut.hash160(Ut.hex_to_bytes(redeem_script))
                _address = Base58Encoder.CheckEncode(Bip49KevacoinMainNet.AddrConfKey('net_ver') + _hashed_redeem_script)
                _r = Scripts.compile(Scripts.P2SHAddressScriptHash(_address), False)
                _ref = Ut.int_to_bytes(_vin.tb_value, 8, 'little')
                _ref = _ref + Ut.to_cuint(len(_r)) + _r
                input_sigs['_PSBT_IN_WITNESS_UTXO'] = Ut.bytes_to_hex(_ref)

                # self.input_signatures.append(input_sigs)
            else:
                _npk = _vin.tb_address
                _npkc = _vin.tb_address_chain
                _pk = wallet.get_publickey_raw(_npk, _npkc)
                _sighash = self.make_preimage(idx, _pk, hash_type)
                _sig = wallet.sign_message(_npk, _sighash, _npkc)
                _script = Scripts.compile(Scripts.P2WPKHScriptSig(_pk))
                _vin.set_scriptsig(_script)

                # input_sigs[_pk] = _signature + Ut.bytes_to_hex(Ut.to_cuint(hash_type.value))
                _signature = Ut.hex_to_bytes(_sig) + Ut.to_cuint(hash_type.value)
                _witness = self.add_witness([_signature, Ut.hex_to_bytes(_pk),])

                _addr = wallet.get_address_by_index(_npk, False)
                _r = Scripts.compile(Scripts.AddressScriptHash(_addr), False)
                _ref = Ut.int_to_bytes(_vin.tb_value, 8, 'little')
                _ref = _ref + Ut.to_cuint(len(_r)) + _r
                # input_sigs['_PSBT_IN_WITNESS_UTXO'] = Ut.bytes_to_hex(_ref)
                _witness.set_PSBT_IN_WITNESS_UTXO(_ref)

                # self.input_signatures.append(input_sigs)

    def make_preimage(self, idx: int, pk: str, hash_type: SIGHASH_TYPE,
                      redeem_script: str | None = None) -> str:
        _hash_type = hash_type

        _pre = []
        _pre.append(self.version)
        _pre.append(self.hash_prevouts(_hash_type))
        _pre.append(self.hash_seqs(_hash_type))

        _outpoint = Ut.reverse_bytes(self.vin[idx].txid)
        _outpoint = _outpoint + self.vin[idx].vout
        _pre.append(_outpoint)

        if redeem_script is not None:
            _redeem_script_bytes = Ut.hex_to_bytes(redeem_script)
            _pre.append(Ut.to_cuint(len(_redeem_script_bytes)))
            _pre.append(_redeem_script_bytes)
        else:
            _s3 = Scripts.P2PKHRedeemScript(pk)
            _s3 = Scripts.compile(_s3, False)
            _pre.append(Ut.to_cuint(len(_s3)) + _s3)

        _pre.append(Ut.int_to_bytes(self.vin[idx].tb_value, 8, 'little'))
        _pre.append(self.vin[idx].sequence)

        _pre.append(self.hash_outputs(_hash_type))
        _pre.append(self.locktime)
        _pre.append(Ut.int_to_bytes(_hash_type.value, 4, 'little'))

        _spre = b''
        for p in _pre:
            _spre = _spre + p

        _sighash = Ut.bytes_to_hex(Ut.sha256(Ut.sha256(_spre)))

        return _sighash

    def to_psbt(self, sighash_type: SIGHASH_TYPE) -> bytes:
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

        for idx, _sig_data in enumerate(self.witnesses):
            _pre.append(Ut.to_cuint(0))
            # _PSBT_IN_WITNESS_UTXO '01'
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(len(Ut.to_cuint(len(_sig_data.PSBT_IN_WITNESS_UTXO)))))
            _pre.append(Ut.to_cuint(len(_sig_data.PSBT_IN_WITNESS_UTXO)))
            _pre.append(_sig_data.PSBT_IN_WITNESS_UTXO)
            # _PSBT_IN_PARTIAL_SIG '02'
            # TODO: Find better way to handle the sort
            if len(_sig_data.stack) == 2:
                # _sig_data.stack.reverse()
                _x = Ut.to_cuint(2) + _sig_data.stack[1]
                _pre.append(Ut.to_cuint(len(_x)))
                _pre.append(_x)
                _sig_bytes = _sig_data.stack[0]
                _pre.append(Ut.to_cuint(len(_sig_bytes)))
                _pre.append(_sig_bytes)
            else:
                for _stack_item in _sig_data.stack:
                    _pre.append(Ut.to_cuint(len(_stack_item)))
                    _pre.append(_stack_item)
            # _PSBT_IN_SIGHASH_TYPE '03'
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(3))
            _shl = (len(Ut.int_to_bytes(
                    sighash_type.value, 4, 'little')))
            _pre.append(Ut.to_cuint(_shl))
            _pre.append(Ut.int_to_bytes(sighash_type.value,
                                        4, 'little'))
            # _PSBT_IN_REDEEM_SCRIPT '04'
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(4))
            _s = self.vin[idx].scriptsig.script
            _pre.append(Ut.to_cuint(len(_s)) + _s)
        _pre.append(Ut.to_cuint(0))
        for i in self.vout:
            _pre.append(Ut.to_cuint(0))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre

    # def to_dict(self) -> dict:
    #     return {'fee_rate': self.fee_rate, 'vin': self.to_dict_list(self.vin),
    #             'vout': self.to_dict_list(self.vout), 'txid': self.txid,
    #             'version': self.version, 'size': self.size,
    #             'locktime': self.locktime}
